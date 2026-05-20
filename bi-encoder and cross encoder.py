# Databricks notebook source
# MAGIC %pip install sentence-transformers
# MAGIC import pandas as pd
# MAGIC import numpy as np
# MAGIC from sentence_transformers import SentenceTransformer, CrossEncoder
# MAGIC from sklearn.metrics.pairwise import cosine_similarity

# COMMAND ----------

import json

# Single source of truth
dbutils.widgets.text("query_json", "{}")

query_str = dbutils.widgets.get("query_json").strip()

# Fallback only for manual testing
if not query_str:
    query_str = """
    {
        "query_id": "Q_software_engineer_usa",
        "job_title": "Software Engineer",
        "location": "United States",
        "experience_min": 5,
        "experience_max": 13,
        "must_have_skills": ["Python", "Java"],
        "domain": "Software Engineering",
        "job_description": "Looking for software engineers in the US with Python, Java, and system design."
    }
    """

# Parse once
query = json.loads(query_str)

# Extract fields
query_id = query.get("query_id")
job_title = query.get("job_title")
location = query.get("location", "Any")
min_experience = float(query.get("experience_min", 0))
max_experience = float(query.get("experience_max", 99))
skills = query.get("must_have_skills", [])
domain = query.get("domain")
job_description = query.get("job_description")

print("QUERY USED:", query)

# COMMAND ----------

candidate_match_features = spark.table("resume_ai_system.gold.candidate_match_features")

# COMMAND ----------

"""filtered_candidates = candidate_match_features[
    (candidate_match_features["experience_eligible"] == 1.0) &
    (candidate_match_features["must_have_skill_coverage"] >= 0.5)
]

print("All candidates:", candidate_match_features["resume_id"].nunique())
print("Filtered candidates:", filtered_candidates["resume_id"].nunique())"""

# COMMAND ----------

"""structured_shortlist = (
    candidate_match_features
    .sort_values("final_score", ascending=False)
    .head(100)
    .copy()
)


#Then:

shortlist_resume_ids = structured_shortlist["resume_id"].unique()


# Then filter resume_experience:

resume_experience_filtered = resume_experience[
    resume_experience["resume_id"].isin(shortlist_resume_ids)
].copy()



resume_experience_filtered.saveAsTable("resume_ai_system.gold.resume_experience_filtered")"""

# COMMAND ----------



resume_experience_filtered = spark.table("resume_ai_system.gold.resume_experience")



# COMMAND ----------

# STEP 5: Create job-level semantic text

from pyspark.sql import functions as F


experience_text_df = (
    resume_experience_filtered
    .withColumn(
        "responsibilities_text",
        F.col("responsibilities").cast("string")
    )
    .withColumn(
        "job_semantic_text",
        F.concat_ws(
            " ",
            F.col("title"),
            F.col("company"),
            F.col("location"),
            F.col("responsibilities_text")
        )
    )
    .select(
        "resume_id",
        "experience_index",
        "company",
        "title",
        "location",
        "start_date",
        "end_date",
        "job_semantic_text"
    )
)

experience_text_df.select(
    "resume_id",
    "title",
    "company",
    "job_semantic_text"
).show(5, truncate=False)

# COMMAND ----------

# STEP 8: Load embedding model

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# COMMAND ----------

# Convert to pandas for embeddings
job_pd = experience_text_df.toPandas()

job_embeddings = embedding_model.encode(
    job_pd["job_semantic_text"].fillna("").tolist(),
    normalize_embeddings=True
)

query_text = query.get("job_description", "")
query_embedding = embedding_model.encode(
    [query_text],
    normalize_embeddings=True
)

job_pd["job_relevance_score"] = cosine_similarity(
    job_embeddings,
    query_embedding
).flatten()

job_pd.sort_values(
    "job_relevance_score",
    ascending=False
).head(10)

# COMMAND ----------

# STEP 12: Job-level aggregation

job_features = (
    job_pd
    .groupby("resume_id")
    .agg(
        max_job_relevance_score=("job_relevance_score", "max"),
        avg_job_relevance_score=("job_relevance_score", "mean")
    )
    .reset_index()
)

job_features.head()

# COMMAND ----------

# STEP 13: Recent job relevance

job_pd["start_date_clean"] = pd.to_datetime(
    job_pd["start_date"],
    errors="coerce"
)

recent_job = (
    job_pd.sort_values(["resume_id", "start_date_clean"], ascending=[True, False]).groupby("resume_id").head(1)[["resume_id", "job_relevance_score"]].rename(columns={"job_relevance_score": "recent_job_relevance_score"})
)

recent_job.head()

# COMMAND ----------

# STEP 16: Select top candidates from embedding score

top_k = (
    job_pd
    .sort_values("job_relevance_score", ascending=False)
    .head(100)
    .copy()
)

top_k


candidate_evidence = (
    job_pd
    .sort_values("job_relevance_score", ascending=False)
    .groupby("resume_id")
    .head(3)
    .groupby("resume_id")["job_semantic_text"]
    .apply(lambda x: " ".join(x))
    .reset_index()
    .rename(columns={"job_semantic_text": "candidate_evidence_text"})
)

top_k = top_k.merge(candidate_evidence, on="resume_id", how="left")

# COMMAND ----------

display(top_k)

# COMMAND ----------

display(candidate_evidence)

# COMMAND ----------

# STEP 17: Apply cross-encoder

cross_encoder = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

pairs = [
    [query_text, text]
    for text in top_k["job_semantic_text"].fillna("")
]

top_k["cross_encoder_score"] = cross_encoder.predict(pairs)

top_k[[
    "resume_id",
    "job_relevance_score",
    "cross_encoder_score"
]].head()

# COMMAND ----------

# STEP 18: Normalize cross-encoder score

min_score = top_k["cross_encoder_score"].min()
max_score = top_k["cross_encoder_score"].max()

if max_score == min_score:
    top_k["cross_encoder_score_norm"] = 1.0
else:
    top_k["cross_encoder_score_norm"] = (
        (top_k["cross_encoder_score"] - min_score)
        / (max_score - min_score)
    )

top_k[[
    "resume_id",
    "cross_encoder_score",
    "cross_encoder_score_norm"
]].head()

# COMMAND ----------

# STEP 19: Final semantic rerank score

top_k["final_rerank_score"] = (
    0.40 * top_k["job_relevance_score"]
    + 0.60 * top_k["cross_encoder_score_norm"]
)

top_k = top_k.sort_values(
    "final_rerank_score",
    ascending=False
)

top_k[[
    "resume_id",
    "job_relevance_score",
    "cross_encoder_score_norm",
    "final_rerank_score"
]]

# COMMAND ----------

ranking_df = spark.table("resume_ai_system.gold.semantic_cross_results")

# Convert to Pandas (for evaluation)
ranking_df = ranking_df.toPandas()

ranking_df["resume_id"] = ranking_df["resume_id"].astype(str)