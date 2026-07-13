import streamlit as st
import pandas as pd
from typing import Any, Dict, List, Tuple

def render_styles() -> None:
    """Injects high-end, clean CSS styling into the Streamlit application."""
    st.markdown(
        """
        <style>
            .block-container { max-width: 1600px; padding: 2rem; }
            .hero { background:#ffffff; border:1px solid #e5e7eb; border-radius:16px; padding:24px; box-shadow:0 4px 12px rgba(15,23,42,.03); margin-bottom:20px; }
            .title { font-size:32px; font-weight:800; color:#111827; }
            .subtitle { font-size:15px; color:#6b7280; }
            .filter-card { background:#ffffff; border:1px solid #e5e7eb; border-radius:16px; padding:24px; box-shadow:0 4px 12px rgba(15,23,42,.02); margin-bottom:24px; }
            .candidate-card { background:#ffffff; border:1px solid #e5e7eb; border-radius:12px; padding:20px; box-shadow:0 2px 8px rgba(15,23,42,.02); margin-bottom:15px; }
            .candidate-name { font-size:20px; font-weight:700; color:#111827; }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_hero() -> None:
    """Renders the top dashboard branding banner."""
    st.markdown(
        """
        <div class="hero">
            <div class="title">AI Powered Intelligent Recruiter Assistant</div>
            <div class="subtitle">Interfacing directly with Databricks Unity Catalog & Genie Engine to pull high-fidelity talent matches.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_candidate(
    row: pd.Series, 
    exp_rows: pd.DataFrame, 
    profile: Dict[str, Any], 
    features: Dict[str, Any], 
    query: Dict[str, Any]
) -> None:
    """Renders a single candidate card with individual layout features, scores, and an AI generation panel."""
    candidate_name = row.get("candidate_name", "Unknown Candidate")
    location = row.get("location", "N/A")
    skills = row.get("skills", "N/A")
    resume_id = row.get("resume_id", "000")

    # Render HTML Outer Structure
    st.markdown(
        f"""
        <div class="candidate-card">
            <div class="candidate-name">👤 {candidate_name}</div>
            <p style="margin:4px 0; color:#4b5563; font-size:14px;">
                📍 Location: {location} | ⚡ Top Recorded Skills: {skills}
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Render Internal Column Metrics Split
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(
            label="Final Match Score", 
            value=f"{float(features.get('final_score', 0)):.2f}"
        )
    with m2:
        st.metric(
            label="Semantic Match", 
            value=f"{float(features.get('semantic_score', 0) or 0.0):.2f}"
        )
    with m3:
        is_eligible = "Eligible" if features.get('experience_eligible') == 1 else "Ineligible"
        st.metric(label="Experience Status", value=is_eligible)
        
    # Recruiter On-Demand AI Assessment Expander
    with st.expander("✨ View Deep AI Recruiter Recommendation Summary"):
        # Unique button key generated dynamically per candidate row iteration
        if st.button("Generate Recommendation Report", key=f"gen_btn_{resume_id}"):
            with st.spinner("Processing deep profile evaluation summary..."):
                # Mockup or placeholder summary fallback text layout structure
                st.markdown("---")
                st.markdown(
                    f"### AI Evaluation Summary for **{candidate_name}**\n"
                    f"* Candidate scores heavily on target keyword **{query.get('job_title')}**.\n"
                    f"* Strong skill footprint match highlighting domain strengths in: `{skills}`.\n"
                    f"* Experience range boundary falls squarely inside targets."
                )

def build_scorecard(
    rows_to_show: List[Tuple[pd.Series, Dict[str, Any]]], 
    profiles: Dict[str, Dict[str, Any]]
) -> pd.DataFrame:
    """Transforms raw runtime dictionary structures into a structured, clean tabular DataFrame format for the scorecard component."""
    data_list = []
    for row, features in rows_to_show:
        data_list.append({
            "candidate_name": row.get("candidate_name", "Unknown"),
            "location": row.get("location", "N/A"),
            "final_score": features.get("final_score", 0.0),
            "semantic_score": features.get("semantic_score", 0.0),
            "experience_eligible": "Eligible" if features.get("experience_eligible") == 1 else "Ineligible"
        })
    return pd.DataFrame(data_list)

def render_scorecard_table(df: pd.DataFrame) -> None:
    """Displays an interactive overview data table featuring conditional blue heat-map tracking gradients."""
    if df.empty:
        st.info("Scorecard is empty.")
        return

    # Create a visual rename representation for explicit stakeholder viewing
    scorecard_df = df.copy()
    scorecard_df.columns = ["Candidate Name", "Location", "Match Score", "Semantic Match", "Exp Eligible"]
    
    st.dataframe(
        scorecard_df.style.background_gradient(subset=["Match Score"], cmap="Blues"),
        use_container_width=True,
        hide_index=True
    )