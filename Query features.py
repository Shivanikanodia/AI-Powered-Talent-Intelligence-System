# Databricks notebook source
df = spark.table("resume_ai_system.gold.candidate_features_final")

candidates = [row.asDict(recursive=True) for row in df.collect()]

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

 def location_match(candidate, query):
    candidate_location = str(candidate.get("primary_location", "")).lower()
    query_location = str(query.get("location", "")).lower()

    if not query_location:
        return 1

    if query_location in candidate_location:
        return 1

    if candidate_location in query_location:
        return 1

    if candidate.get("open_to_relocate", False) and query.get("allow_relocation", False):
        return 1

    return 0

# COMMAND ----------

from datetime import datetime

def calculate_months(job):
    start = job.get("start_date")
    end = job.get("end_date") or datetime.now()

    # assuming dates are datetime objects
    return (end.year - start.year) * 12 + (end.month - start.month)

# COMMAND ----------

def safe_num(x, default=0):
    return default if x is None else x

# COMMAND ----------

def compute_years_experience(jobs):
    total_months = 0

    for job in jobs:
        months = calculate_months(job)
        total_months += months

    return total_months / 12

# COMMAND ----------

def experience_eligible(candidate, query):
    years = safe_num(candidate.get("years_experience"))
    min_exp = query.get("experience_min", 0)
    max_exp = query.get("experience_max", 999)

    if min_exp <= years <= max_exp:
        return 1
    if years >= min_exp - 0.5 and years <= max_exp + 1:
        return 1
    return 0


def experience_fit(candidate, query):
    years = safe_num(candidate.get("years_experience"))
    min_exp = query.get("experience_min", 0)
    max_exp = query.get("experience_max", 999)

    if min_exp <= years <= max_exp:
        return 1.0

    if years < min_exp:
        diff = min_exp - years
        if diff <= 1:
            return 0.7
        elif diff <= 2:
            return 0.4
        return 0.2

    diff = years - max_exp
    if diff <= 1:
        return 0.85
    elif diff <= 3:
        return 0.6
    return 0.4

# COMMAND ----------

def skill_coverage(candidate_skills, query_skills):
    if not query_skills:
        return 1.0

    matched = sum(1 for s in query_skills if s in candidate_skills)

    return matched / len(query_skills)


# COMMAND ----------

def normalize_skills(skills):
    if not skills:
        return set()
    return set(str(s).lower().strip() for s in skills if s)

def must_have_skill_coverage(candidate, query):
    must_have = query.get("must_have_skills", [])
    candidate_skills = normalize_skills(candidate.get("skills"))

    if not must_have:
        return 1.0

    must_have_clean = [str(s).lower().strip() for s in must_have if s]
    matched = sum(1 for skill in must_have_clean if skill in candidate_skills)

    return matched / len(must_have_clean)

# COMMAND ----------

results = []

for candidate in candidates:

    # Core features
    loc = location_match(candidate, query)
    exp_elig = experience_eligible(candidate, query)
    exp_fit = experience_fit(candidate, query)
    must_skill = must_have_skill_coverage(candidate, query)

    # Hard filter
    hard_pass = 1 if exp_elig == 1 else 0

    structured_score = (
    must_skill * 0.50 +
    exp_fit * 0.35 +
    loc * 0.15
)

    # Final structured score after hard filter
    if hard_pass == 0:
        final_score = 0
    else:
        final_score = structured_score

    results.append({
        "query_id": query["query_id"],
        "resume_id": candidate.get("resume_id"),
        "candidate_name": candidate.get("candidate_name"),
        "linkedin_urls": candidate.get("linkedin_urls"),
        "path": candidate.get("path"),

        "years_experience": candidate.get("years_experience"),
        "skills": candidate.get("skills"),

        "location_match": loc,
        "experience_eligible": exp_elig,
        "experience_fit": exp_fit,
        "must_have_skill_coverage": must_skill,
        "hard_pass": hard_pass,

        "structured_score": structured_score,
        "final_score": final_score
    })

# COMMAND ----------

print(type(results))
print(len(results))
print(results[0])

# COMMAND ----------

for r in results:
    # convert VariantVal / anything unusual to string
    r["linkedin_urls"] = str(r.get("linkedin_urls", ""))

    r["location_match"] = int(r.get("location_match", 0))
    r["experience_eligible"] = int(r.get("experience_eligible", 0))
    r["hard_pass"] = int(r.get("hard_pass", 0))

    r["years_experience"] = float(r.get("years_experience") or 0)
    r["experience_fit"] = float(r.get("experience_fit") or 0)
    r["must_have_skill_coverage"] = float(r.get("must_have_skill_coverage") or 0)
    r["structured_score"] = float(r.get("structured_score") or 0)
    r["final_score"] = float(r.get("final_score") or 0)

# COMMAND ----------

from pyspark.sql.types import StructField, StringType

StructField("linkedin_urls", StringType(), True)

# COMMAND ----------

from pyspark.sql.types import (
    StructType, StructField, StringType,
    DoubleType, ArrayType, IntegerType
)

schema = StructType([
    StructField("query_id", StringType(), True),
    StructField("resume_id", StringType(), True),
    StructField("candidate_name", StringType(), True),
    StructField("linkedin_urls", StringType(), True),
    StructField("path", StringType(), True),
    StructField("years_experience", DoubleType(), True),
    StructField("skills", ArrayType(StringType()), True),

    StructField("location_match", IntegerType(), True),
    StructField("experience_eligible", IntegerType(), True),
    StructField("experience_fit", DoubleType(), True),
    StructField("must_have_skill_coverage", DoubleType(), True),
    StructField("hard_pass", IntegerType(), True),

    StructField("structured_score", DoubleType(), True),
    StructField("final_score", DoubleType(), True)
])

# COMMAND ----------

result_df = spark.createDataFrame(results, schema=schema)
display(result_df.orderBy("final_score", ascending=False))

# COMMAND ----------

result_df.write.mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("resume_ai_system.gold.candidate_match_features")

# COMMAND ----------

print(
    dbutils.notebook.entry_point.getDbutils()
    .notebook().getContext().notebookPath().get()
)