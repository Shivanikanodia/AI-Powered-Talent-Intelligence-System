"""Pipeline Trigger Script

Use this script to trigger the Feature and Embedding Pipeline
when you need to recompute features for new query criteria.

Set SCORING_JOB_ID in your environment or .env file.
"""

import json
import time
import os
from databricks.sdk import WorkspaceClient

def trigger_pipeline(query_dict, job_id=None):
    """
    Triggers the scoring pipeline with a custom query.
    
    Args:
        query_dict: Dictionary with query parameters:
            - query_id: unique identifier (e.g., "Q_20260626_software_engineer")
            - job_title: target role (e.g., "Software Engineer")
            - location: target location (e.g., "United States")
            - experience_min: minimum years (e.g., 5)
            - experience_max: maximum years (e.g., 13)
            - must_have_skills: list of required skills (e.g., ["Python", "Java"])
            - domain: target domain (e.g., "Software Engineering")
            - job_description: full description for semantic matching
        job_id: Optional job ID (reads from SCORING_JOB_ID env var if not provided)
    
    Returns:
        run_id: The job run ID for tracking
    """
    w = WorkspaceClient()
    
    if not job_id:
        job_id = os.getenv("SCORING_JOB_ID")
        if not job_id:
            raise ValueError("SCORING_JOB_ID must be set in environment or passed as argument")
    
    job_id = int(job_id)
    
    print(f"Triggering pipeline job {job_id}...")
    print(f"Query: {json.dumps(query_dict, indent=2)}")
    
    # Trigger the job with query parameters
    run = w.jobs.run_now(
        job_id=job_id,
        notebook_params={"query_json": json.dumps(query_dict)}
    )
    
    run_id = run.run_id
    print(f"\n✓ Job triggered! Run ID: {run_id}")
    print(f"Monitor in your Databricks workspace: Jobs > Job {job_id} > Run {run_id}")
    
    return run_id

def wait_for_completion(run_id, poll_interval=10, timeout=1800):
    """
    Wait for the pipeline run to complete.
    
    Args:
        run_id: The job run ID
        poll_interval: Seconds between status checks (default: 10)
        timeout: Maximum wait time in seconds (default: 30 min)
    
    Returns:
        status: Final run status (SUCCESS, FAILED, etc.)
    """
    w = WorkspaceClient()
    
    elapsed = 0
    print(f"\nWaiting for run {run_id} to complete...")
    
    while elapsed < timeout:
        run = w.jobs.get_run(run_id)
        state = run.state.life_cycle_state.value
        
        if state in ["TERMINATED", "SKIPPED"]:
            result = run.state.result_state.value if run.state.result_state else "UNKNOWN"
            print(f"\n✓ Run completed with status: {result}")
            return result
        
        print(f"  Status: {state} (waited {elapsed}s)", end="\r")
        time.sleep(poll_interval)
        elapsed += poll_interval
    
    print(f"\n⚠️ Timeout after {timeout}s")
    return "TIMEOUT"

# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    # Example: Software Engineer query
    query = {
        "query_id": "Q_20260626_software_engineer",
        "job_title": "Software Engineer",
        "location": "United States",
        "experience_min": 5,
        "experience_max": 13,
        "must_have_skills": ["Python", "Java", "System Design"],
        "domain": "Software Engineering",
        "job_description": "Looking for experienced software engineers with strong Python and Java skills, system design experience, and ability to work on distributed systems."
    }
    
    # Trigger the pipeline
    run_id = trigger_pipeline(query)
    
    # Wait for it to complete (optional)
    status = wait_for_completion(run_id)
    
    if status == "SUCCESS":
        print("\n✓ Pipeline completed successfully!")
        print("Results are now in: resume_ai_system.gold.candidate_match_features")
        print("Refresh your Streamlit app to see the updated candidates.")
    else:
        print(f"\n✗ Pipeline failed with status: {status}")

# =============================================================================
# INTEGRATION WITH STREAMLIT APP
# =============================================================================

# You can add a button in your Streamlit app to trigger pipeline on-demand:
"""
import streamlit as st
from TRIGGER_PIPELINE import trigger_pipeline

if st.button("🔄 Recompute Features with New Query"):
    query = {
        "query_id": f"Q_{int(time.time())}",
        "job_title": role,
        "location": location_filter,
        "experience_min": float(exp_range[0]),
        "experience_max": float(exp_range[1]),
        "must_have_skills": skills,
        "domain": domain,
        "job_description": nl_query
    }
    
    with st.spinner("Triggering pipeline..."):
        run_id = trigger_pipeline(query)
        st.success(f"Pipeline triggered! Run ID: {run_id}")
        st.info("Results will be available in 2-5 minutes. Refresh the app to see them.")
"""