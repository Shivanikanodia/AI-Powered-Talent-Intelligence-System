import re
from typing import List, Tuple

import streamlit as st


def detect_nl_role_and_domain(text: str) -> Tuple[str, str]:
    q = text.lower()
    if "backend" in q:
        return "Backend Engineer", "Backend Engineering"
    if "data scientist" in q or "machine learning" in q or "ml engineer" in q:
        return "Data Scientist", "Data Science"
    return "Software Engineer", "Software Engineering"


def detect_nl_experience_range(text: str) -> Tuple[int, int]:
    q = text.lower()
    patterns = [
        r"(\d+)\s*(?:-|–|to)\s*(\d+)\s*(?:years|yrs|year|yr)",
        r"between\s*(\d+)\s*(?:and|to)\s*(\d+)\s*(?:years|yrs|year|yr)",
    ]
    for pattern in patterns:
        match = re.search(pattern, q)
        if match:
            a, b = int(match.group(1)), int(match.group(2))
            return min(a, b), max(a, b)
    return 5, 13


def detect_nl_skills(text: str) -> List[str]:
    q = text.lower()
    skill_map = {
        "Python": ["python", "pandas", "numpy"],
        "Java": ["java", "spring", "spring boot"],
        "System Design": ["system design", "systems design", "architecture", "scalable systems"],
        "Distributed Systems": ["distributed systems", "distributed system"],
        "AWS": ["aws", "ec2", "s3", "lambda"],
        "Kubernetes": ["kubernetes", "k8s"],
        "SQL": ["sql", "postgres", "mysql", "snowflake"],
        "Go": ["go", "golang"],
    }
    detected = []
    for skill, variants in skill_map.items():
        if any(variant in q for variant in variants):
            detected.append(skill)
    return detected or ["Python", "Java", "System Design"]


def detect_nl_location(text: str) -> str:
    q = text.lower()
    if "remote" in q:
        return "Remote"
    if "san francisco" in q:
        return "San Francisco"
