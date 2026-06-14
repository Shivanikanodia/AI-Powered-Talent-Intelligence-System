# 🧠 AI-Powered Talent Intelligence System

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

# Dataset

Over 2,000 resumes collected from Kaggle, LinkedIn, and X-Ray Search
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
Processed Layer - Performs schema extraction, normalization, ontology mapping, abbreviation handling, and synonym standardization
Gold Layer- Stores analytics-ready candidate entities and semantic matching outputs

This layered architecture improves scalability, modularity, and maintainability of the pipeline.

Dimensional Data Modeling:

A candidate-centric dimensional model was designed using structured entities such as:

Candidate Profile
Resume Master
Skills
Education
Experience
Embeddings
Ranking Scores

The model supports semantic retrieval, feature engineering, and explainable candidate ranking.

## Phase 2: Resume Processing & Structuring

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

- <img width="783" height="66" alt="Screenshot 2026-04-27 at 19 06 07" src="https://github.com/user-attachments/assets/62076fa3-5efe-4a1e-8983-be1e5cde47df" />

The parsed JSON is flattened using `explode`, where each element becomes a row in a table.

<img width="457" height="166" alt="Screenshot 2026-05-09 at 23 36 27" src="https://github.com/user-attachments/assets/244eb229-9476-4b30-beec-79ee7cead3ff" />


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

<img width="894" height="232" alt="Screenshot 2026-05-09 at 23 36 34" src="https://github.com/user-attachments/assets/6b581e36-04c5-417f-923c-1e3050c1c912" />


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

<img width="1244" height="848" alt="image" src="https://github.com/user-attachments/assets/e201df88-541a-4ed3-bd85-e5caacc6e367" />


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
- Semantic - job_relevance_score
- Cross-encoder - final_rerank_score

This hybrid approach balances explainability, precision, and semantic relevance.

<img width="512" height="132" alt="Screenshot 2026-05-09 at 23 36 44" src="https://github.com/user-attachments/assets/08bfd310-41f7-4dfe-91a3-f58f7f0a6bdd" />

---

# 📊 Candidate Summary & Explainability Layer

The system leverages the Genie interaction layer at resumes saved in Delta tables and LLM model to generate concise, evidence-based candidate summaries and recruiter recommendations for frond end streamlit app.

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

<img width="2726" height="1134" alt="image" src="https://github.com/user-attachments/assets/da53fe05-1544-4c0f-be79-4ce13e661286" />


> Find software engineers in USA with 5 to 13 years of experience and skills Python, Java, and system design.

The recruiter clicks **Run Search** to retrieve ranked candidates.

---

## The app displays:

#### Ranked candidate list and  Overall match score:

<img width="1409" height="481" alt="Screenshot 2026-05-09 at 23 45 35" src="https://github.com/user-attachments/assets/e94f8ac9-ce24-4c48-bfbc-f555c8cea6d1" />


#### Feature-level scorecard

  <img width="2670" height="858" alt="image" src="https://github.com/user-attachments/assets/3d26e6bb-c3de-4503-b027-daad1d553290" />

#### Resume evidence

  <img width="2728" height="1000" alt="image" src="https://github.com/user-attachments/assets/b7c5bdfd-06b7-4e5b-9a34-6bd6fab57e20" />

#### Career trajectory insights

<img width="2782" height="1114" alt="image" src="https://github.com/user-attachments/assets/d167e645-0476-4e6f-a0e5-effc87f09530" />

#### Recruiter-facing summary and  Suggested screening question

<img width="1084" height="1082" alt="image" src="https://github.com/user-attachments/assets/0cca43de-70da-46ed-bdba-aaffea8bd252" />

---

### UGenie integration to support recruiter insights and analytics-driven candidate evaluation. 


<img width="751" height="275" alt="Screenshot 2026-05-15 at 13 00 16" src="https://github.com/user-attachments/assets/554926fa-d0f5-4ed5-a085-03e9ed6c68de" />


<img width="810" height="321" alt="Screenshot 2026-05-15 at 13 00 35" src="https://github.com/user-attachments/assets/62ac8775-20e3-4bf4-a3ee-93f81e36c751" />



# 📊 Evaluation Metrics

The system is evaluated using ranking quality, latency, and factual consistency metrics.

## Metrics Used

- ⏱️ Latency for retrieval, ranking, and generation
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
git clone https://github.com/Shivanikanodia/AI-Powered-Intelligent-Recruiter-Assistant.git

cd intelligent-recruiter-ai

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
