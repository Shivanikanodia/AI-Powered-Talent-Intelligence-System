# 🧠 AI-Powered Intelligent Recruiter Assistant

An explainable AI system for semantic resume matching, hybrid candidate ranking, and recruiter-facing insights — designed to reduce manual screening effort and time-to-fill, eliminate keyword bias, and improve quality of hire.

---

## 🚀 Business Problem

Traditional Applicant Tracking Systems (ATS) often:

- Rely heavily on keyword matching, missing semantic relevance.
- Lack transparency in candidate ranking.
- Require manual resume screening, increasing recruiter effort.
- Create inconsistent definitions and alignment between hiring managers and roles.
- Provide limited support for analytics and decision insights.

---

## 💡 Solution Overview

This system converts unstructured resumes into structured, queryable data and applies hybrid retrieval + re-ranking to identify the most relevant candidates.

The solution combines semantic search, structured feature scoring, cross-encoder re-ranking, and evidence-grounded LLM summaries to help recruiters evaluate candidates transparently and consistently.

---

## 🔑 Key Capabilities

- 📄 Resume parsing using Databricks AI functions: `ai_parse_document` and `ai_extract`
- 🧮 Feature-based scoring for skills, experience, domain, seniority, education, and location
- 🔍 Semantic search using Sentence-BERT embeddings and FAISS
- 🧠 Cross-encoder re-ranking for improved precision
- ✨ LLM-generated summaries grounded in retrieved resume evidence
- 💬 Natural language querying for recruiter-friendly interaction
- 📊 Explainable ranking outputs with feature contribution, strengths, gaps, and resume evidence

---

## 💼 Business Impact

- ⏱️ Reduces resume screening time significantly
- 🎯 Improves candidate quality through context-aware matching
- 🤝 Enhances recruiter trust with explainable AI outputs
- 📊 Supports structured hiring decisions using transparent scoring and evidence

---

## 🧠 System Architecture: High-Level

The system follows a hybrid architecture:

1. Resume ingestion and parsing
2. Resume structuring and normalization
3. Feature scoring
4. Semantic embedding generation
5. FAISS-based retrieval
6. Cross-encoder re-ranking
7. Candidate-level aggregation
8. Evidence extraction
9. LLM-generated recruiter summaries
10. Streamlit-based recruiter interface

---

# 🔍 Data Pipeline

## Phase 1: Resume Processing & Structuring

The pipeline transforms unstructured resume PDFs into structured data using Databricks AI functions.

Resumes are complex because they often contain columns, tables, varied layouts, and inconsistent formatting.

### Ingestion

Resumes are read from a Unity Catalog Volume using `read_files`.

### Parsing

`ai_parse_document` converts PDFs into structured JSON while preserving layout. Each resume is broken into smaller blocks called elements.

Each element represents a piece of the resume and contains:

- Element type
- Extracted content
- Confidence score, representing reliability of extraction
- Bounding box, representing the position of the element on the page
- Additional layout metadata

The parsed JSON is flattened using `explode`, where each element becomes a row in a table.

### Structured Extraction

`ai_extract` is used with a defined schema to extract consistent candidate profile fields such as:

- Skills
- Work experience
- Education
- Projects
- Certifications
- Location
- Candidate metadata

This converts row-level parsed resume data into a structured candidate profile for querying and analysis.

### Modeling

The extracted resume data is flattened into analytical tables for efficient querying:

- `resume_core`
- `resume_skills`
- `resume_experience`
- `resume_education`

<img width="783" height="66" alt="Screenshot 2026-04-27 at 19 06 07" src="https://github.com/user-attachments/assets/62076fa3-5efe-4a1e-8983-be1e5cde47df" />

### Data Cleaning and Normalization

The system performs:

- Formatting cleanup
- Unicode handling
- Deduplication
- Skill normalization
- Synonym expansion
- Ontology-based mapping

This helps standardize variations such as `ML`, `Machine Learning`, and `machine-learning` into consistent skill representations.

---

## Phase 2: Feature Scoring

The system computes lightweight structured features to measure candidate fit against a recruiter query or job requirement.

Feature scores include:

- Skill overlap
- Experience alignment
- Domain relevance
- Seniority fit
- Education alignment
- Location match

Weights are assigned based on hiring criteria, and the system returns a final structured feature score.

Example scoring components:

- `must_have_skill_coverage`
- `experience_fitment`
- `domain_fit`
- `location_match`
- `education_relevance`

This provides interpretable signals before applying semantic ranking or LLM summarization.

---

## Phase 3: Embeddings, Retrieval & Re-Ranking

### Resume Chunking

Resume content is chunked into searchable sections.

For approximately 500 resumes:

- Around 15,000 raw chunks were generated
- Around 3,400 cleaned chunks were retained after preprocessing

### Semantic Search

The system uses section-level embeddings with Sentence-BERT.

The workflow includes:

1. Generate embeddings for cleaned resume sections
2. Store embeddings in a FAISS index
3. Convert recruiter query into an embedding
4. Retrieve top-N relevant resume sections
5. Aggregate section-level results into resume-level relevance

### Cross-Encoder Re-Ranking

A cross-encoder evaluates the recruiter query and resume section jointly.

This improves contextual understanding and ranking precision compared with embedding similarity alone.

### Hybrid Ranking

The final ranking combines:

- Structured feature score
- Semantic retrieval score
- Cross-encoder relevance score

This hybrid approach balances explainability, precision, and semantic relevance.

---

# 📊 Candidate Summary & Explainability Layer

The system leverages the Genie interaction layer and an LLM model to generate concise, evidence-based candidate summaries and recruiter recommendations.

The LLM is used only after scoring and evidence extraction. It does not decide the score.

The summaries are strictly grounded in retrieved resume sections, ensuring high factual accuracy and minimizing hallucinations.

---

## Explainable Ranking Outputs

Candidate ranking is decomposed into interpretable components such as:

- Must-have skill coverage
- Experience fitment
- Domain fit
- Location match
- Education relevance
- Career trajectory
- Resume evidence

This allows recruiters to clearly understand why a candidate is ranked higher or lower.

---

## Resume Evidence

Evidence of skills and experience is generated using only the most relevant retrieved resume segments through semantic search and cross-encoder re-ranking.

Every statement is traceable to source data.

Evidence is backed by explicit references to resume sections such as:

- Experience
- Skills
- Projects
- Education
- Certifications

This improves transparency and trust in the recommendation.

---

## Hiring Signals & Career Trajectory

Recruiters also care about stability and growth.

The system calculates hiring signals from work history rather than generating them through the LLM.

Examples include:

- Average tenure
- Employer transitions
- Career progression
- Role growth
- Stability indicators

---

## Recruiter Summaries

The LLM generates recruiter-friendly summaries that highlight:

- Candidate strengths
- Candidate gaps
- Evidence-backed fit assessment
- Suggested screening questions

Instead of keyword filtering, this system enables transparent, evidence-based candidate evaluation.

---

# 💻 Streamlit App

The project includes a Streamlit application for recruiter interaction.

## Natural Language Search Interface

Recruiters can enter natural language queries such as:

> Find software engineers in USA with 5 to 13 years of experience and skills Python, Java, and system design.

The recruiter clicks **Run Search** to retrieve ranked candidates.

---

## Candidate List + Scorecard

The app displays:

- Ranked candidate list
- Overall match score
- Feature-level scorecard
- Strengths and gaps
- Resume evidence
- Career trajectory insights
- Recruiter-facing summary
- Suggested screening question

---

# 📊 Evaluation Metrics

The system is evaluated using ranking quality, latency, and factual consistency metrics.

## Metrics Used

- ⏱️ Latency for retrieval, ranking, and generation
- 🎯 Precision@K
- 🎯 Recall@K
- 📈 NDCG@K
- 🥇 MRR@K
- 🔁 Consistency checks
- ⚠️ Hallucination checks

---

## Benchmarking Setup

Five benchmarking label queries were created to evaluate model performance based on relevance.

Example ground truth labels:

```python
ground_truth_df = pd.DataFrame([
    {"query_id": "q1", "resume_id": "44", "relevance": 2},
    {"query_id": "q1", "resume_id": "52", "relevance": 2},
    {"query_id": "q1", "resume_id": "49", "relevance": 1},
    {"query_id": "q1", "resume_id": "61", "relevance": 1},
    {"query_id": "q1", "resume_id": "68", "relevance": 1},
    {"query_id": "q1", "resume_id": "57", "relevance": 0},
])
```

---

## Scoring Approaches Compared

The following ranking approaches were benchmarked:

1. **RAG-only**
   - Uses semantic similarity from embeddings

2. **Cross-encoder**
   - Re-ranks candidates using joint query-resume evaluation

3. **Hybrid model** ✅
   - Combines feature scoring, cross-encoder ranking, and RAG-based retrieval

---

## Evaluation Results Summary

The cross-encoder achieved the strongest ranking quality, with the highest NDCG and MRR values.

An MRR of 1 indicates that the best candidate was ranked first.

The hybrid model improved over semantic search by combining multiple ranking signals, including structured candidate features, semantic relevance, and cross-encoder precision.

---

# 🛠️ Tech Stack

- Python 3.10
- FAISS
- Sentence-Transformers
- Cross-Encoder MiniLM
- Databricks
- Delta Lake
- Databricks AI Functions
- SQL
- Semantic Data Models
- Streamlit
- Pandas
- NumPy

---

# 📁 Project Structure

```text
.
├── app.py                 # Streamlit UI for querying and results
├── preprocessing.py       # Resume parsing, cleaning, and metadata extraction
├── build_index.py         # Embedding generation and FAISS indexing
├── config.py              # Configuration values and scoring weights
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── data/                  # Resume data or sample input files
```

---

# ✅ Implemented

- Resume preprocessing
- Databricks-based parsing and extraction
- Structured resume tables
- Skill normalization and ontology mapping
- Semantic retrieval using FAISS
- Feature-based scoring
- Cross-encoder re-ranking
- Hybrid ranking
- Explainability outputs
- Evidence-grounded recruiter summaries
- Streamlit recruiter interface
- Benchmarking of RAG-only, cross-encoder, and hybrid approaches

---

# 🔮 Future Work

- MLflow-based evaluation and experiment tracking
- Responsible AI safeguards
- Bias checks
- Prompt injection handling
- Expanded benchmarking dataset
- Additional recruiter analytics dashboards
- Improved skill ontology and taxonomy mapping

---

# 📜 License

This project is intended for educational and internal enterprise use.

---

# 🙋‍♀️ Author

**Shivani Kanodia**

Master's in Business Analytics  
AI, Analytics, and Talent Intelligence Enthusiast
