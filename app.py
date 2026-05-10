import re
from typing import Any, Dict, List, Tuple

import pandas as pd
import streamlit as st

from src.data_loader import load_data
from src.evidence import experience_profile
from src.nl_parser import apply_natural_language_search
from src.scoring import compute_match_features, role_matches, search_blob
from src.ui_components import (
    build_scorecard,
    render_candidate,
    render_hero,
    render_scorecard_table,
    render_styles,
)

st.set_page_config(
    page_title="AI Powered Intelligent Recruiter Assistant",
    layout="wide"
)

render_styles()

try:
    ui_df, exp_df = load_data()
except FileNotFoundError as exc:
    st.error(
        f"Missing file: {exc.filename}. Put recruiter_ui.csv and resume_experience.csv "
        f"in the correct data folder."
    )
    st.stop()

all_skills = sorted({
    s for skills_list in ui_df["skills_list"] for s in skills_list
})

render_hero()

st.markdown('<div class="filter-card">', unsafe_allow_html=True)

st.markdown("#### Natural-Language Candidate Search")

nl_query = st.text_area(
    "Type your hiring requirement",
    value=st.session_state.get(
        "nl_query",
        "Find software engineers in the United States with 5-13 years of experience and Python, Java, and System Design skills.",
    ),
    placeholder="Example: Find backend engineers in California with 6-10 years of experience, AWS, Kubernetes, and Java.",
    height=95,
)

use_nl = st.button("Apply Natural Language Search", type="primary")

if use_nl:
    apply_natural_language_search(nl_query)
    st.success("Natural language search applied. Filters updated below.")

st.markdown("---")

f1, f2, f3, f4, f5 = st.columns(
    [1.15, 1.05, 1.55, 1.1, 1.05],
    gap="medium"
)

with f1:
    role = st.text_input(
        "Target Role",
        value=st.session_state.get("nl_role", "Software Engineer")
    )

with f2:
    exp_range = st.slider(
        "Experience Range",
        min_value=0,
        max_value=25,
        value=st.session_state.get("nl_exp_range", (5, 13)),
        step=1,
    )

with f3:
    skill_options = sorted(
        set(
            all_skills
            + [
                "Python",
                "Java",
                "System Design",
                "Distributed Systems",
                "AWS",
                "Kubernetes",
                "SQL",
                "Go",
            ]
        )
    )

    default_skills = st.session_state.get(
        "nl_skills",
        [s for s in ["Python", "Java", "System Design"] if s in skill_options]
        or ["Python", "Java", "System Design"],
    )

    default_skills = [s for s in default_skills if s in skill_options]

    skills = st.multiselect(
        "Must-Have Skills",
        options=skill_options,
        default=default_skills
    )

with f4:
    domain_options = [
        "Software Engineering",
        "Backend Engineering",
        "Data Science",
        "Any",
    ]

    domain_default = st.session_state.get(
        "nl_domain",
        "Software Engineering"
    )

    if domain_default not in domain_options:
        domain_default = "Software Engineering"

    domain = st.selectbox(
        "Target Domain",
        domain_options,
        index=domain_options.index(domain_default)
    )

with f5:
    location_options = [
        "United States",
        "Any",
        "San Francisco",
        "California",
        "Remote",
        "McLean",
        "Chicago",
        "Arlington",
    ]

    location_default = st.session_state.get(
        "nl_location",
        "United States"
    )

    if location_default not in location_options:
        location_default = "United States"

    location_filter = st.selectbox(
        "Location",
        location_options,
        index=location_options.index(location_default)
    )

f6, f7, f8 = st.columns([1.2, 2.1, 0.9], gap="medium")

with f6:
    company_signal = st.text_input(
        "Company",
        value="",
        placeholder="Optional: Google, Capital One..."
    )

with f7:
    additional_query = st.text_input(
        "Additional Search",
        value="",
        placeholder="Optional: backend APIs, GCP, latency, leadership..."
    )

with f8:
    hard_role_filter = st.checkbox("Use title filter", value=True)

st.markdown("</div>", unsafe_allow_html=True)

query = {
    "query_id": "streamlit_query",
    "job_title": role,
    "location": location_filter,
    "experience_min": float(exp_range[0]),
    "experience_max": float(exp_range[1]),
    "must_have_skills": skills,
    "domain": domain,
    "company": company_signal,
}

profiles: Dict[str, Dict[str, Any]] = {}
rows_to_show: List[Tuple[pd.Series, Dict[str, Any]]] = []

for _, row in ui_df.iterrows():
    rid = row.get("resume_id")
    exp_rows = exp_df[exp_df["resume_id"] == rid]

    profile = experience_profile(exp_rows)
    profiles[rid] = profile

    features = compute_match_features(
        row,
        exp_rows,
        profile,
        query
    )

    if features["experience_eligible"] != 1:
        continue

    if hard_role_filter and not role_matches(profile, role):
        continue

    if company_signal and features["company_fit"] != 1:
        continue

    blob = search_blob(row, profile, exp_rows)

    if additional_query.strip():
        terms = [
            t.lower()
            for t in re.findall(r"[a-zA-Z0-9+#.]+", additional_query)
            if len(t) > 1
        ]

        if terms and not all(t in blob for t in terms):
            continue

    if skills and features["must_have_skill_coverage"] <= 0:
        continue

    rows_to_show.append((row, features))

rows_to_show.sort(
    key=lambda x: (
        x[1]["final_score"],
        x[1]["must_have_skill_coverage"],
        x[1]["experience_fit"],
    ),
    reverse=True,
)

r1, r2 = st.columns([3, 1])

with r1:
    st.markdown(f"### Ranked Candidates ({len(rows_to_show)})")

with r2:
    st.markdown(
        "<div style='text-align:right; color:#6b7280; font-weight:750; padding-top:12px;'>"
        "Sorted by calculated Final Match Score"
        "</div>",
        unsafe_allow_html=True,
    )

if not rows_to_show:
    st.markdown(
        '<div class="empty">No candidates matched these criteria. '
        "Try removing company signal, relaxing title filter, or reducing must-have skills.</div>",
        unsafe_allow_html=True,
    )
else:
    scorecard_df = build_scorecard(rows_to_show, profiles)

    with st.expander("View scorecard table", expanded=True):
        render_scorecard_table(scorecard_df)

    for row, features in rows_to_show[:25]:
        rid = row.get("resume_id")
        exp_rows = exp_df[exp_df["resume_id"] == rid]

        render_candidate(
            row,
            exp_rows,
            profiles[rid],
            features,
            query
        )