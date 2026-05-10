import os

DATA_DIR = os.getenv("DATA_DIR", ".")

SCORING_JOB_ID = os.getenv("SCORING_JOB_ID", "")

GENIE_SPACE_ID = os.getenv("GENIE_SPACE_ID", "")

DATABRICKS_HTTP_PATH = os.getenv("DATABRICKS_HTTP_PATH", "")

RECRUITER_UI_PATH = os.getenv(
    "RECRUITER_UI_PATH",
    os.path.join(DATA_DIR, "recruiter_ui.csv"),
)

EXPERIENCE_PATH = os.getenv(
    "EXPERIENCE_PATH",
    os.path.join(DATA_DIR, "resume_experience.csv"),
)

DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)