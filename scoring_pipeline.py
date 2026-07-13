"""Scoring Pipeline Integration Module

This module connects the Streamlit app to the existing Feature and Embedding Pipeline.

The actual scoring is done by the Feature and Embedding Pipeline job which:
  - Reads from: resume_ai_system.gold.candidate_features_final
  - Writes to: resume_ai_system.gold.candidate_match_features
  - Scoring weights: must_skill*0.50 + exp_fit*0.35 + loc*0.15
  - Uses sentence-transformers/all-MiniLM-L6-v2 for semantic matching
  - Adds semantic_score via job-level embeddings

The app should query the output tables directly rather than re-implement scoring.
"""

from databricks.sdk import WorkspaceClient
import json
import os

def trigger_scoring_pipeline(query: dict, job_id: str = None) -> str:
    """
    Triggers the scoring pipeline job with a query.
    
    Args:
        query: Dict with keys:
            - query_id: unique identifier
            - job_title: target role
            - location: target location
            - experience_min/max: years range
            - must_have_skills: list of required skills
            - domain: target domain
            - job_description: full description for semantic matching
        job_id: The Databricks job ID (reads from env if not provided)
    
    Returns:
        run_id: The job run ID
    """
    w = WorkspaceClient()
    
    if not job_id:
        job_id = os.getenv("SCORING_JOB_ID")
        if not job_id:
            raise ValueError("SCORING_JOB_ID must be provided or set in environment")
    
    run = w.jobs.run_now(
        job_id=int(job_id),
        notebook_params={"query_json": json.dumps(query)}
    )
    
    return run.run_id

def get_scored_candidates(query_id: str = None):
    """
    Reads scored candidates directly from the pipeline output table.
    
    The app should use this instead of re-computing scores.
    Table schema from pipeline:
      - query_id, resume_id, candidate_name, linkedin_urls, path
      - years_experience, skills  
      - location_match, experience_eligible, experience_fit
      - must_have_skill_coverage, hard_pass
      - structured_score, final_score
      - semantic_score (added by embedding pipeline)
    
    Returns:
        DataFrame with scored candidates
    """
    from pyspark.sql import functions as F
    from pyspark.sql import SparkSession
    
    spark = SparkSession.builder.getOrCreate()
    
    # Read from pipeline output
    df = spark.table("resume_ai_system.gold.candidate_match_features")
    
    if query_id:
        df = df.filter(F.col("query_id") == query_id)
    
    # Join with semantic scores if available
    try:
        semantic_df = spark.table("resume_ai_system.gold.semantic_cross_results")
        df = df.join(semantic_df, on="resume_id", how="left")
    except:
        pass
    
    return df.toPandas()