from typing import Any, Dict, List

import pandas as pd

from src.data_loader import normalize
from src.scoring import skill_variants


def experience_profile(exp_rows: pd.DataFrame) -> Dict[str, Any]:
    if exp_rows.empty:
        return {
            "current_title": "Role not available",
            "current_company": "Company not available",
            "companies": [],
            "titles": [],
            "avg_tenure_months": None,
            "employer_transitions": 0,
            "short_roles": 0,
            "trajectory": "Insufficient role history",
        }
    rows = exp_rows.sort_values("experience_index")
    current = rows.iloc[0]
    companies = [normalize(x) for x in rows["company"].tolist() if normalize(x)]
    titles = [normalize(x) for x in rows["title"].tolist() if normalize(x)]

    tenures = []
    for _, r in rows.iterrows():
        start, end = r.get("start_dt"), r.get("end_dt")
        if pd.notna(start) and pd.notna(end) and end >= start:
            tenures.append(max((end - start).days / 30.44, 0))
    avg_tenure = round(sum(tenures) / len(tenures), 1) if tenures else None
    short_roles = sum(1 for m in tenures if m < 12)
    employer_transitions = max(len([c for c in companies if c]) - 1, 0)

    title_text = " ".join(titles).lower()
    if any(w in title_text for w in ["staff", "principal", "lead", "senior", "manager", "director", "head"]):
        trajectory = "Senior technical or leadership progression"
    else:
        trajectory = "Individual contributor progression"

    return {
        "current_title": normalize(current.get("title")) or "Role not available",
        "current_company": normalize(current.get("company")) or "Company not available",
        "companies": companies,
        "titles": titles,
        "avg_tenure_months": avg_tenure,
        "employer_transitions": employer_transitions,
        "short_roles": short_roles,
        "trajectory": trajectory,
    }


def snippet(text: str, terms: List[str], max_chars: int = 165) -> str:
    clean = normalize(text)
    if len(clean) <= max_chars:
        return clean
    lower = clean.lower()
    positions = [lower.find(t.lower()) for t in terms if t and lower.find(t.lower()) >= 0]
    if positions:
        start = max(min(positions) - 42, 0)
    else:
        start = 0
    end = min(start + max_chars, len(clean))
    return ("..." if start > 0 else "") + clean[start:end].strip() + ("..." if end < len(clean) else "")


def evidence_for_terms(exp_rows: pd.DataFrame, skills: List[str], max_per_skill: int = 2) -> Dict[str, List[Dict[str, str]]]:
    evidence: Dict[str, List[Dict[str, str]]] = {}
    if exp_rows.empty:
        return evidence
    ordered = exp_rows.sort_values("experience_index")
    for skill in skills:
        found: List[Dict[str, str]] = []
        variants = skill_variants(skill)
        for _, r in ordered.iterrows():
            for responsibility in r.get("responsibilities_list", []):
                text = normalize(responsibility)
                if any(v in text.lower() for v in variants):
    return evidence