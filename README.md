# 🧠 AI-Powered Talent Intelligence System

To design and deploy an explainable, semantic AI resume search and talent analytics platform powered by a unified data lakehouse. The system replaces rigid keyword matching with contextual relevance scoring, maps temporal workforce trends, and enables hiring stakeholders to seamlessly build balanced talent pipelines.

### Project Goals:

Efficiency: Drastically reduce manual screening effort and minimize candidate sourcing time.

Quality & Diversity: Eliminate keyword-based bias to improve diverse candidate discovery and surface higher-quality hires.

Retention: Identify early-stage talent acquisition indicators that correlate with future retention or attrition.

Strategic Insights: Deliver proactive, real-time retention and compensation insights directly to hiring managers to optimize offer competitiveness and workforce stability.

---

## 🚀 Business Problem

Traditional Applicant Tracking Systems (ATS) often:

- Rely heavily on keyword matching and missing semantic relevance.
- Lack transparency in candidate ranking and why someone sits at position 1
- Require manual resume screening and increase in recruiter effort.
- Inconsistent alignment between hiring managers expectations and roles.
- Provide limited support for talent analytics and decision insights.

---

## 💡 Solution Overview

This system converts unstructured resumes into structured, queryable data and applies hybrid retrieval + re-ranking to identify the most relevant profiles in position first, second and third. 
The solution combines semantic search, structured feature scoring, cross-encoder re-ranking, evidence grounded LLM summaries and self-service insights to help recruiters evaluate candidates transparently and much faster.

---

## 🔑 Key Capabilities

- 📄 Resume parsing using Databricks AI functions: `ai_parse_document` and `ai_extract`
- 🧮 Feature based scoring for skills match, experience fit, domain alignment, seniority fit, and location. 
- 🔍 Semantic search using Sentence BERT embeddings and FAISS VectorDB
- 🧠 Cross-encoder re-ranking for improved precision and contextual relevance
- ✨ LLM generated summaries grounded in resume data 
- 💬 Natural language querying for recruiter friendly interaction with streamlit interface and Genie
- 📊 Explainable ranking outputs with feature contribution, strengths, gaps and resume evidence

---

## 💼 Business Impact

- ⏱️ Reduces resume screening time significantly
- 🎯 Improves candidate quality and discovery through context aware matching
- 🤝 Enhances recruiter trust with explainable retention and career progression outputs
- 📊 Supports structured hiring decisions using evidences and compensation benchmarking 

---

## 🧠 System Architecture: High-Level

The system follows a hybrid architecture:

1. Resume ingestion and parsing
2. Resume structuring and normalization
3. Feature engineering
4. Semantic embedding generation
5. FAISS based retrieval
6. Cross encoder re-ranking
8. Evidence extraction (skills, responsbililities, domain, experience, location and salary)
9. LLM generated recruiter summaries
10. Streamlit based recruiter interface

---

# Dataset

Over 2,000 resumes collected from Kaggle, LinkedIn, and X-Ray Search.

Roles included:
Data Scientist
Data Analyst
Software Engineer

Profiles across multiple experience levels and countries including the USA, UK, Australia, and India
Resume formats included highly unstructured layouts with tables, columns, and varying section structures

--- 

# 🔍 Data Pipeline

## Phase 1: System Architecture and Data Modeling

The data pipeline follows a Medallion Architecture consisting of:

Raw Layer- Stores parsed resume documents extracted from PDFs using AI_PARSE_DOCUMENT
Processed Layer - Performs schema extraction, text normalization and cleaning, data standardisation, abbreviation handling, and ontology mapping. 
Gold Layer- Stores analytics ready candidate entities and semantic matching outputs. 

This layered architecture improves scalability, lineage, auditing, and maintainability of the pipeline.

Dimensional Data Modeling:

A candidate-centric dimensional model was designed using structured entities such as:

Candidate Profile
Resume Master
Skills
Education
Experience
Embeddings
Ranking Scores

## Phase 2: Resume Processing & Structuring

The pipeline transforms unstructured resume PDFs into structured data using Databricks AI functions.

Resumes are complex because they often contain columns, tables, varied layouts, and inconsistent formatting.

### Ingestion

Resumes are read from a Unity Catalog Volume using `read_files`.

### Parsing

`ai_parse_document` converts PDFs into un-structured Semi-JSON while preserving layout. Each resume is broken into smaller blocks called elements.

Each element represents a piece of the resume and contains:

- Element type
- Extracted content
- Confidence score, representing reliability of extraction
- Bounding box, representing the position of the element on the page
- Additional layout metadata

- <img width="783" height="66" alt="Screenshot 2026-04-27 at 19 06 07" src="https://github.com/user-attachments/assets/62076fa3-5efe-4a1e-8983-be1e5cde47df" />

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

- `resume_core`
- `resume_skills`
- `resume_experience`
- `resume_education`


### Data Cleaning and Normalization:

The system performs:

- Formatting cleanup
- Unicode handling
- Deduplication
- Skill normalization
- Synonym expansion
- Ontology-based mapping

This helps standardize variations such as `ML`, `Machine Learning`, and `machine-learning` into consistent skill representations.

<img width="729" height="195" alt="Screenshot 2026-04-27 at 19 07 41" src="https://github.com/user-attachments/assets/ca868aa9-845f-4b5b-aaa3-b390387b11a2" />

---

## Phase 2: Feature Scoring

The system computes lightweight structured features to measure candidate against a recruiter query.

Feature scores include:

- Experience alignment
- Skills match
- Seniority fit
- Education alignment
- Location match

Weights are assigned based on hiring criteria for different requirements, and the system returns a final structured feature score. This provides interpretable signals before applying semantic ranking or LLM summarization.

---

## Phase 3: Embeddings, Retrieval & Re-Ranking

### Resume Chunking

Resume content is chunked into searchable sections.

For approximately 500 resumes:

- Around 15,000 raw chunks were generated
- Around 3,400 cleaned chunks were retained after preprocessing

### Semantic Search

The system uses section-level embeddings with Sentence BERT.

The workflow includes:

1. Generate embeddings for resume sections
2. Store embeddings in a FAISS index
3. Convert recruiter query into an embedding
4. Retrieve top-N relevant resume sections
5. Aggregate section level results into resume level relevance and generates job_relevance_score

### Cross-Encoder Re-Ranking

A cross-encoder evaluates the recruiter query and resume section jointly on TOP 100 Chunks for semantic matching step.
This improves contextual understanding and ranking precision compared with embedding similarity alone and returns fina_rerank_score.

### Hybrid Ranking

The final ranking combines:

- Structured feature score
- Semantic - job_relevance_score
- Cross-encoder - final_rerank_score

This hybrid approach balances explainability, precision, and semantic relevance.

<img width="512" height="132" alt="Screenshot 2026-05-09 at 23 36 44" src="https://github.com/user-attachments/assets/08bfd310-41f7-4dfe-91a3-f58f7f0a6bdd" />

---

# 📊 Candidate Summary & Explainability Layer

The system leverages the Genie interaction layer for resumes saved in Delta tables and use LLM model with controlled prompt engineering to generate concise, evidence based candidate summaries and recruiter recommendations for frond end streamlit app.

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
- Career trajectory signals

This allows to clearly understand why a candidate is ranked higher or lower.

---

## Resume Evidence

Evidence of skills and experience is generated using only the most relevant retrieved resume segments through semantic search and cross-encoder re-ranking at fingerprint.
Every statement is traceable to source data.
Evidence is backed by explicit references to resume sections such as:

- Experience
- Skills
- Projects
- Education
- Certifications

This improves transparency, reduce time in evaluating 1000+ resumes and trust in the recommendation.

---

## Hiring Signals & Career Trajectory

Recruiters also care about stability and growth.
The system calculates hiring signals from work history rather than generating them through the LLM.

Examples include:

- Average tenure per employee
- Total Employer transitions in entire career trajectory
- Career progression and promotions
- Stability indicators

These metric offers insights into a candidate's job stability and can be an important factor in evaluating their career consistency and loyalty to employers. Understanding job tenure can help organizations predict future employee retention and assess how reliable a candidate might be in long-term roles.

---

## Recruiter Summaries

The LLM generates recruiter-friendly summaries that highlight:

- Candidate strengths and career progression insights
- Suggess screening questions

Instead of keyword filtering, this system enables transparent, evidence based candidate evaluation.

---


## The app displays:

###### Ranked candidate list and  Overall match score:

###### Feature-level scorecard

###### Resume evidence

###### Career trajectory insights

###### Recruiter-facing summary and  Suggested screening question
---

# 📊 Evaluation Metrics

The system is evaluated using ranking quality, latency, and factual consistency metrics.

## Metrics Used

- 🎯 Precision@K
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

## Evaluation Results Summary:


<img width="478" height="378" alt="Screenshot 2026-04-27 at 19 11 50" src="https://github.com/user-attachments/assets/517cf875-1622-4416-a2ec-7e2ffae1d89f" />

The cross-encoder achieved the strongest ranking quality, with the highest NDCG and MRR values.

An MRR of 1 indicates that the best candidate was ranked first.

The hybrid model improved over semantic search by combining multiple ranking signals, including structured candidate features, semantic relevance, and cross-encoder precision.

---

# 📁 Project Structure

```text
├── app.py
├── requirements.txt
├── README.md

├── data/
│   ├── recruiter_ui.csv
│   └── resume_experience.csv

├── src/
│   ├── config.py
│   ├── data_loader.py
│   ├── parse.py
│   ├── scoring.py
│   ├── evidence.py
│   ├── recommendation.py
│   └── ui_components.py

```
---

## Run instructions :
git clone https://github.com/Shivanikanodia/AI-Powered-Talent-Intelligence-System.git

cd AI-Powered-Talent-Intelligence-System

pip install -r requirements.txt

streamlit run app.py

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

### For AI recommendation:
ollama run llama3

# 🔮 Future Work

- MLflow-based evaluation and experiment tracking
- Responsible AI safeguards
- Prompt injection handling
- Expanded benchmarking dataset
- Improved skill ontology and taxonomy mapping

---

# 📜 License

This project is intended for educational and internal enterprise use.

---

# 🙋‍♀️ Author

**Shivani Kanodia**

Master's in Business Analytics  
AI, Analytics, and Talent Intelligence Enthusiast
