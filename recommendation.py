from typing import Any, Dict, List

import pandas as pd
import requests

from src.config import DEFAULT_MODEL, OLLAMA_URL


def call_ollama(prompt: str) -> str:
    try:
        response = requests.post(OLLAMA_URL, json={"model": DEFAULT_MODEL, "prompt": prompt, "stream": False}, timeout=60)
        response.raise_for_status()
        return response.json().get("response", "No response returned from model.")
    except Exception as exc:
        return f"Unable to reach local model. Start Ollama with `ollama run {DEFAULT_MODEL}`. Error: {exc}"


def build_ai_prompt(row: pd.Series, profile: Dict[str, Any], features: Dict[str, Any], evidence: Dict[str, List[Dict[str, str]]], query: Dict[str, Any]) -> str:
    evidence_lines = []
    for skill, items in evidence.items():
        if not items:
            evidence_lines.append(f"- {skill}: No direct responsibility evidence found.")
        for item in items:
            evidence_lines.append(f"- {skill}: {item['title']} at {item['company']} — {item['text']}")
    return f"""
You are an experienced technical recruiter reviewing a candidate for a hiring manager.

Use ONLY the provided candidate data and resume evidence.
Do not assume missing skills.
Do not mention protected or sensitive attributes.
Do not make a final hiring decision. Provide decision-support only.

Recruiter Query:
{query}

SEARCH CRITERIA:
Target role: {query['job_title']}
Domain: {query.get('domain', 'Any')}
Company signal: {query.get('company') or 'None'}
Location: {query.get('location', 'Any')}
Experience range: {query['experience_min']} to {query['experience_max']} years
Must-have skills: {', '.join(query.get('must_have_skills', []))}

Candidate Profile:
Name: {row.get('candidate_name')}
Current title: {profile.get('current_title')}
Current company: {profile.get('current_company')}
Known companies: {', '.join(profile.get('companies', [])[:8])}
Location: {row.get('location')}
Highest degree: {row.get('highest_degree')}
Years experience: {float(row.get('years_experience', 0)):.1f}
Final match score: {features['final_score']:.2f}
Must-have skill coverage: {features['must_have_skill_coverage']:.2f}
Experience fit: {features['experience_fit']:.2f}
Domain fit: {features['domain_fit']:.2f}
Location alignment: {features['location_match']}
Company alignment: {features['company_fit']}
Average tenure: {profile.get('avg_tenure_months')} months
Employer transitions: {profile.get('employer_transitions')}
Career trajectory: {profile.get('trajectory')}

Task:
Write a concise recruiter recommendation with these sections:

1. Recommendation:
Choose one: Strong shortlist, Shortlist with review, Keep as backup, Not recommended
""".strip()