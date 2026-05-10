import ast
import json
import re
from typing import Any, List, Tuple

import pandas as pd
import streamlit as st

from config import EXPERIENCE_PATH, RECRUITER_UI_PATH


def normalize(text: Any) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def safe_list(value: Any) -> List[str]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, list):
        return [normalize(x) for x in value if normalize(x)]
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none"}:
        return []
    for parser in (json.loads, ast.literal_eval):
        try:
            parsed = parser(text)
            if isinstance(parsed, list):
                return [normalize(x) for x in parsed if normalize(x)]
        except Exception:
            pass
    return [text]


def parse_date(value: Any) -> pd.Timestamp:
    text = normalize(value)
    if not text or text.lower() in {"nan", "none"}:
        return pd.NaT
    if text.lower() == "present":
        return pd.Timestamp.today()
    return pd.to_datetime(text, errors="coerce")


@st.cache_data(show_spinner=False)
def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    ui = pd.read_csv(RECRUITER_UI_PATH)
    exp = pd.read_csv(EXPERIENCE_PATH)

    ui["skills_list"] = ui.get("skills", "").apply(safe_list)
    ui["linkedin_list"] = ui.get("linkedin_urls", "").apply(safe_list)

    for col in [
        "years_experience",
        "location_match",
        "experience_eligible",
        "must_have_skill_coverage",
        "structured_score",
        "final_score",
    ]:
        if col in ui.columns:
            ui[col] = pd.to_numeric(ui[col], errors="coerce").fillna(0)

    ui = ui.drop_duplicates("resume_id", keep="first")

    exp["responsibilities_list"] = exp.get("responsibilities", "").apply(safe_list)
    exp["start_dt"] = exp.get("start_date", "").apply(parse_date)
    exp["end_dt"] = exp.get("end_date", "").apply(parse_date)
    exp["title"] = exp.get("title", "").fillna("")
    exp["company"] = exp.get("company", "").fillna("")
    exp["location"] = exp.get("location", "").fillna("")

    return ui, exp
    
