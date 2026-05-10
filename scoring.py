import re
from typing import Any, Dict, List

import pandas as pd


def skill_variants(skill: str) -> List[str]:
    base = skill.lower().strip()
    variants = {base}
    if base in {"system design", "systems design"}:
        variants.update([
            "distributed system", "distributed systems", "architecture", "scalable", "scalability",
            "microservices", "service orchestration", "system health", "latency", "throughput",
            "high availability", "high performance",
        ])
    if base == "python":
        variants.update(["python", "pandas", "numpy", "scikit", "py"])
    if base == "java":
        variants.update(["java", "spring", "spring boot", "jvm"])
    if base == "aws":
        variants.update(["aws", "ec2", "s3", "lambda", "cloudwatch"])
    if base == "kubernetes":
        variants.update(["kubernetes", "k8s"])
    return sorted(variants, key=len, reverse=True)

    import pandas as pd


def location_match(candidate_location: str, query_location: str) -> int:
    c = str(candidate_location or "").lower()
    q = str(query_location or "").lower()
    if not q or q == "any":
        return 1
    if q == "united states" and "united states" in c:
        return 1
    if q in c or c in q:
        return 1
    if q == "remote" and "remote" in c:
        return 1
    return 0


def experience_eligible(years: float, min_exp: float, max_exp: float) -> int:
    return 1 if min_exp <= years <= max_exp else 0


def experience_fit(years: float, min_exp: float, max_exp: float) -> float:
    if min_exp <= years <= max_exp:
        return 1.0
    if years < min_exp:
        diff = min_exp - years
        if diff <= 1:
            return 0.70
        if diff <= 2:
            return 0.40
        return 0.20
    diff = years - max_exp
    if diff <= 1:
        return 0.85
    if diff <= 3:
        return 0.60
    return 0.40


def normalize_skills(skills: List[str]) -> set:
    return {str(s).lower().strip() for s in skills if str(s).strip()}


def search_blob(row: pd.Series, profile: Dict[str, Any], exp_rows: pd.DataFrame) -> str:
    responsibilities: List[str] = []
    for items in exp_rows.get("responsibilities_list", []):
        responsibilities.extend(items)
    return " ".join([
        str(row.get("candidate_name", "")),
        str(row.get("location", "")),
    return all(t in titles for t in tokens)