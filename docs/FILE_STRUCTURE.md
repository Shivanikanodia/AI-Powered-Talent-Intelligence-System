# 📁 Repository Structure

This document explains the enterprise-level organization of the AI-Powered Talent Intelligence System repository.

## Directory Layout

```
AI-Powered-Talent-Intelligence-System/
│
├── 📄 Root Level Files
├── 📁 src/                  # Core application modules
├── 📁 notebooks/            # Data pipeline notebooks
├── 📁 config/               # Configuration templates
├── 📁 scripts/              # Utility scripts
└── 📁 docs/                 # Documentation
```

---

## 📄 Root Level Files

### `README.md`
**Purpose**: Main project overview, quick start guide, and feature highlights  
**Audience**: External users, stakeholders, new team members  
**Contains**: Project goals, architecture overview, setup instructions, tech stack

### `app.py`
**Purpose**: Main Streamlit application entry point  
**Why here**: Standard practice - main executable at repo root for easy discovery  
**Usage**: Run with `streamlit run app.py`

### `app.yaml`
**Purpose**: Databricks App deployment configuration  
**Why here**: Deployment configs stay at root for CI/CD pipelines  
**Contains**: Streamlit server settings, port configuration, environment setup

### `requirements.txt`
**Purpose**: Python package dependencies  
**Why here**: Standard Python convention for dependency management  
**Usage**: Install with `pip install -r requirements.txt`

### `.gitignore`
**Purpose**: Git exclusion rules to prevent committing secrets and temporary files  
**Why here**: Git convention - must be at repository root  
**Protects**: .env files, secrets, databases, backup files, IDE configs

---

## 📁 src/ - Core Application Modules

**Purpose**: Houses all reusable Python modules that power the application  
**Why separated**: Keeps business logic organized, testable, and maintainable

### `src/config.py`
**Purpose**: Centralized configuration and environment variable management  
**Why needed**: Single source of truth for all app settings  
**Contains**:  
- Unity Catalog table paths  
- Databricks warehouse HTTP paths  
- Pipeline job IDs  
- Genie Space IDs  
- Model configuration defaults

**Key functions**:  
- Reads from environment variables  
- Provides fallback defaults  
- Validates configuration on startup

---

### `src/data_loader.py`
**Purpose**: Data loading and Unity Catalog integration  
**Why needed**: Abstracts complex data access logic  
**Contains**:  
- Functions to load candidate profiles  
- Resume experience data fetching  
- Unity Catalog table readers  
- Data preprocessing utilities

**Key functions**:  
- `load_recruiter_ui()` - Load candidate match features  
- `load_resume_experience()` - Load job history data  
- `filter_candidates()` - Apply query filters

---

### `src/evidence.py`
**Purpose**: Resume evidence extraction and grounding  
**Why needed**: Ensures LLM responses are factually grounded in resume data  
**Contains**:  
- Evidence extraction from resume sections  
- Semantic search for relevant experience  
- Skill and project validation  
- Citation generation

**Key functions**:  
- `extract_evidence()` - Find supporting resume text  
- `validate_claims()` - Verify LLM statements against data  
- `generate_citations()` - Create traceable references

---

### `src/recommendation.py`
**Purpose**: LLM-powered candidate recommendation engine  
**Why needed**: Generates recruiter-friendly summaries and insights  
**Contains**:  
- LLM prompt engineering  
- Candidate strength/weakness analysis  
- Screening question generation  
- Career trajectory insights

**Key functions**:  
- `generate_recommendation()` - Create recruiter summary  
- `suggest_screening_questions()` - Generate interview questions  
- `analyze_career_trajectory()` - Assess stability and growth

---

### `src/scoring_pipeline.py`
**Purpose**: Integration with Feature and Embedding Pipeline  
**Why needed**: Connects Streamlit app to backend scoring job  
**Contains**:  
- Pipeline job trigger functions  
- Scored candidate retrieval  
- Feature score aggregation  
- Semantic score integration

**Key functions**:  
- `trigger_scoring_pipeline()` - Start pipeline job with query  
- `get_scored_candidates()` - Fetch results from Unity Catalog  
- `monitor_job_status()` - Track pipeline execution

---

### `src/ui_components.py`
**Purpose**: Reusable Streamlit UI components  
**Why needed**: Maintains consistent styling and DRY principles  
**Contains**:  
- Candidate card layouts  
- Scorecard tables  
- Hero banners  
- Custom CSS styling  
- Metric displays

**Key functions**:  
- `render_candidate()` - Display candidate card  
- `render_scorecard_table()` - Show ranking table  
- `render_hero()` - Display app header  
- `render_styles()` - Inject custom CSS

---

## 📁 notebooks/ - Data Pipeline Notebooks

**Purpose**: Databricks notebooks for ETL, feature engineering, and model training  
**Why separated**: Keeps analysis and pipeline code organized

### `notebooks/01_resume_parsing.ipynb`
**Purpose**: Resume ingestion and parsing  
**Pipeline stage**: Raw → Bronze layer  
**Contains**:  
- `ai_parse_document()` usage  
- PDF text extraction  
- Layout preservation  
- Element parsing

---

### `notebooks/02_feature_engineering.ipynb`
**Purpose**: Feature extraction and scoring  
**Pipeline stage**: Bronze → Silver layer  
**Contains**:  
- Experience fit calculation  
- Skill matching logic  
- Location alignment  
- Seniority assessment  
- Feature weight tuning

---

### `notebooks/03_embeddings_and_reranking.ipynb`
**Purpose**: Semantic search and cross-encoder reranking  
**Pipeline stage**: Silver → Gold layer  
**Contains**:  
- Sentence BERT embedding generation  
- FAISS index creation  
- Cross-encoder model usage  
- Hybrid score combination

---

### `notebooks/04_evaluation.ipynb`
**Purpose**: Model evaluation and benchmarking  
**Pipeline stage**: Gold layer validation  
**Contains**:  
- NDCG@K calculation  
- MRR@K metrics  
- Precision@K analysis  
- A/B test results  
- Performance comparisons

---

## 📁 config/ - Configuration Templates

**Purpose**: Environment variable templates and configuration examples  
**Why separated**: Keeps secrets out of code, provides setup guidance

### `config/env.example.py`
**Purpose**: Template showing required environment variables  
**Why needed**: Helps new developers set up their environment  
**Usage**: Copy to `.env` and fill in actual values  
**Contains**:  
- Unity Catalog table paths (with examples)  
- Databricks warehouse IDs (placeholder)  
- Job IDs (placeholder)  
- Genie Space IDs (placeholder)  
- Model configuration options

**Security**: Does NOT contain real secrets - safe to commit

---

## 📁 scripts/ - Utility Scripts

**Purpose**: Standalone scripts for operations and automation  
**Why separated**: Distinguishes operational scripts from core application code

### `scripts/trigger_pipeline.py`
**Purpose**: Manual pipeline triggering and monitoring  
**Why needed**: Allows on-demand recomputation without opening notebooks  
**Usage**: Run as `python scripts/trigger_pipeline.py`  
**Contains**:  
- Pipeline job execution  
- Run status monitoring  
- Query parameter formatting  
- Completion waiting logic

**When to use**:  
- New query criteria  
- Resume data updates  
- Model retraining  
- Debugging pipeline issues

---

## 📁 docs/ - Documentation

**Purpose**: Comprehensive project documentation beyond the README  
**Why separated**: Keeps README concise, provides deep-dive references

### `docs/FILE_STRUCTURE.md` (this file)
**Purpose**: Explains repository organization  
**Audience**: Developers, maintainers, auditors

### `docs/ARCHITECTURE.md`
**Purpose**: System architecture and design decisions  
**Contains**:  
- Medallion architecture details  
- Data flow diagrams  
- Component interactions  
- Technology choices and rationale

### `docs/DEPLOYMENT.md`
**Purpose**: Deployment instructions for production  
**Contains**:  
- Databricks App deployment steps  
- Secret management setup  
- CI/CD pipeline configuration  
- Environment setup guides

### `docs/PIPELINE.md`
**Purpose**: Data pipeline documentation  
**Contains**:  
- Pipeline schedule and triggers  
- Table schemas  
- Data lineage  
- Troubleshooting guides

### `docs/API_REFERENCE.md`
**Purpose**: Module and function API documentation  
**Contains**:  
- Function signatures  
- Parameter descriptions  
- Return types  
- Usage examples

---

## Design Principles

### 1. **Separation of Concerns**
Each directory has a single, clear purpose. Application code (`src/`) is separate from notebooks, configs, and scripts.

### 2. **Standard Conventions**
Follows Python and Git best practices:  
- Requirements at root  
- Source code in `src/`  
- Documentation in `docs/`  
- Scripts in `scripts/`

### 3. **Security First**
Configuration templates in `config/` directory, real secrets in `.env` (gitignored). No hardcoded credentials.

### 4. **Discoverability**
Main executable (`app.py`) at root for immediate visibility. Clear naming conventions (`02_feature_engineering` vs generic "notebook2").

### 5. **Maintainability**
Modular structure allows independent testing and updates. Clear file purposes reduce cognitive load.

---

## File Naming Conventions

### Notebooks
- Prefix with numbers for execution order: `01_`, `02_`, `03_`  
- Use descriptive names: `resume_parsing`, `feature_engineering`  
- Lowercase with underscores

### Python Modules
- Lowercase with underscores: `data_loader.py`, `scoring_pipeline.py`  
- Avoid abbreviations unless standard: `config.py` ✅, `cfg.py` ❌

### Documentation
- All caps for top-level docs: `README.md`, `LICENSE`  
- All caps for important guides: `ARCHITECTURE.md`, `DEPLOYMENT.md`  
- Descriptive names: `FILE_STRUCTURE.md` not `STRUCTURE.md`

---

## Quick Reference

**I want to...**

- **Run the app locally** → `streamlit run app.py`  
- **Deploy to Databricks** → See `app.yaml` and `docs/DEPLOYMENT.md`  
- **Understand the architecture** → Read `docs/ARCHITECTURE.md`  
- **Set up my environment** → Copy `config/env.example.py` to `.env`  
- **Trigger the pipeline** → Run `python scripts/trigger_pipeline.py`  
- **Modify UI components** → Edit `src/ui_components.py`  
- **Change scoring logic** → Edit notebooks in `notebooks/`  
- **Add new features** → Create module in `src/`, update `requirements.txt`

---

**Last updated**: 2026-07-13  
**Maintained by**: Shivani Kanodia