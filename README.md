### 🧠 AI-Powered Intelligent Recruiter Assistant:

An explainable AI system for semantic resume matching, hybrid candidate ranking, and recruiter-facing insights — designed to reduce manual screening effort and time to fill, eliminate keyword bias, and improve quality of hire. 

### 🚀 Business Problem:

Traditional Applicant Tracking Systems (ATS):

Rely heavily on keyword matching, missing semantic relevance
Lack transparency in candidate ranking
Require manual resume screening, increasing recruiter effort and inconsistent definition and alignment between HM and roles. 
Provide limited support for analytics and decision insights

### 💡 Solution Overview:

This system converts unstructured resumes into structured, queryable data and applies hybrid  retrieval + re-ranking to identify the most relevant candidates.

### Key Capabilities:

📄 Resume parsing using Databricks AI functions (ai_parse_document, ai_extract)
🔍 Semantic search using Sentence-BERT embeddings + FAISS
🧮 Feature-based scoring (skills, experience, domain, seniority)
🧠 Cross-encoder re-ranking for improved precision
✨ LLM-generated summaries grounded in retrieved evidence
💬 Natural language querying for recruiter-friendly interaction
📊 Explainable ranking outputs (feature contribution, strengths, gaps)

### 💼 Business Impact:
⏱️ Reduces resume screening time significantly
🎯 Improves candidate quality via context-aware matching
🤝 Enhances recruiter trust with explainable AI

### 🧠 System Architecture (High-Level)
Recruiter Query → Embedding → FAISS Retrieval → Aggregation  → Feature Scoring → Cross-Encoder Re-ranking → LLM Summary

### 🔍 Data Pipeline:

<img width="332" height="417" alt="Screenshot 2026-04-27 at 19 08 30" src="https://github.com/user-attachments/assets/d93af2d7-d55f-443f-8d93-fa4ee03255a5" />


#### Phase 1: Resume Processing & Structuring

The pipeline transforms unstructured resume PDFs into structured data using Databricks AI functions.

**Ingestion:** Resumes are read from a Unity Catalog Volume using read_files.
**Parsing:** ai_parse_document converts PDFs into structured JSON while preserving layout, extracting document **elements, content, bbox, type, error rate, page_id and confidence_score.** 
**Extraction:** ai_extract (2-pass approach) extracts contact details and detailed profile information (skills, experience, education).

<img width="783" height="66" alt="Screenshot 2026-04-27 at 19 06 07" src="https://github.com/user-attachments/assets/62076fa3-5efe-4a1e-8983-be1e5cde47df" />


**Modeling:** 
Data is flattened into tables (resume_core, resume_skills, resume_experience, resume_education) using explode() for efficient ** querying.

<img width="547" height="532" alt="Screenshot 2026-04-27 at 18 58 28" src="https://github.com/user-attachments/assets/a46bf4da-9bdf-4e54-8c3a-42ddd715d6b3" />

  
#### Data cleaning (formatting, normalization, Unicode handling)
- Synonym expansion + ontology-based mapping

<img width="729" height="195" alt="Screenshot 2026-04-27 at 19 07 41" src="https://github.com/user-attachments/assets/ca868aa9-845f-4b5b-aaa3-b390387b11a2" />


#### Phase 2: Embeddings & Indexing:

<img width="622" height="424" alt="Screenshot 2026-04-27 at 19 09 42" src="https://github.com/user-attachments/assets/a183d514-d183-4af1-b980-fce7f6889d37" />


- Section-level embeddings using Sentence-BERT
- Stored in FAISS for fast similarity search


#### Phase 3: Retrieval

- Convert recruiter query → embeddings
- Retrieve top N relevant resume sections
- Aggregate to compute resume-level relevance


#### Phase 4: Features Scoring 

- Skill overlap
- Experience alignment
- Domain relevance
- Education and location alignment

#### Cross-encoder re ranking:

- Joint evaluation of query + resume
- Improves contextual understanding and ranking precision

#### 📊 Candidate Summary & Explainability Layer

The system leverages the Genie Interaction Layer to generate concise, evidence-based candidate summaries. These summaries are strictly grounded in retrieved resume sections, ensuring high factual accuracy and minimizing hallucinations.

##### 🔎 How it Works
Context-Grounded Summarization
Summaries are generated using only the most relevant retrieved resume segments (via semantic search + ranking), ensuring every statement is traceable to source data.
Evidence Attribution
Each summary is backed by explicit references to resume sections (experience, skills, projects), enabling transparency and trust.

#### Feature-Level Explainability
Candidate ranking is decomposed into interpretable components such as:

Skill match score
Experience relevance
Domain alignment
Seniority fit
Education relevance

This allows recruiters to clearly understand why a candidate is ranked higher or lower.

#### ✨ Key Output Highlights

Each candidate profile includes:

Strengths - Key areas where the candidate strongly aligns with job requirements (e.g., high-demand skills, relevant experience, domain expertise)
Gaps - Missing or weaker areas compared to the job description (e.g., skill gaps, insufficient experience in specific domains)
Matching Evidence - Direct excerpts or references from the resume that justify the identified strengths and gaps

<img width="449" height="403" alt="Screenshot 2026-04-27 at 19 14 54" src="https://github.com/user-attachments/assets/78df1738-62fe-42d7-92a8-1d7fcc183132" />


#### 📊 Evaluation Metrics:

- ⏱️ Latency (retrieval, ranking, generation)
- 🎯 Precision@K / Recall@K
- 🔁 Consistency & hallucination checks
- ⚖️ Scoring Approaches Compared

Built 5 benchmarking label queries to evaluate model performance based on relevance.  


ground_truth_df = pd.DataFrame([
    {"query_id": "q1", "resume_id": "44", "relevance": 2},
    {"query_id": "q1", "resume_id": "52", "relevance": 2},
    {"query_id": "q1", "resume_id": "49", "relevance": 1},
    {"query_id": "q1", "resume_id": "61", "relevance": 1},
    {"query_id": "q1", "resume_id": "68", "relevance": 1},
    {"query_id": "q1", "resume_id": "57", "relevance": 0},
])

- RAG-only (semantic similarity)
 
- Cross-encoder
  
- Hybrid (Feature scoring + Cross-encoder + RAG) ✅


<img width="478" height="378" alt="Screenshot 2026-04-27 at 19 11 50" src="https://github.com/user-attachments/assets/517cf875-1622-4416-a2ec-7e2ffae1d89f" />


- Cross-encoder achieves highest precision and ranking quality
  
- Hybrid model improves over semantic retrieval significantly
  
-  Feature-only model performs weakest (no semantic understanding)
  
-  Semantic-only has good recall but lower ranking precision


#### 🛠️ Tech Stack
Python 3.10
FAISS
Sentence-Transformers
Cross-Encoder (MiniLM)
Streamlit
Ollama (Llama 3)
Databricks (Delta Lake, AI Functions)
SQL + Semantic Data Models

#### 📁 Project Structure

app.py              # Streamlit UI for querying and results
preprocessing.py    # Resume parsing, cleaning, metadata extraction
build_index.py      # Embedding generation and FAISS indexing
config.py           # Configurations and scoring weights
resume_index/       # Stored FAISS index + metadata
data/resumes/       # Sample anonymized resumes

#### 🧪 Prototype Status

⚠️ This is a working prototype, not a fully productionized system.

#### Implemented:

Resume preprocessing
Semantic retrieval (FAISS)
Feature-based scoring
Hybrid ranking
Explainability outputs

### 🔮 Future Work
 Benchmark RAG vs Cross-Encoder vs Hybrid approaches  
- MLflow-based evaluation and experiment tracking  
- Role-specific prompt templates  
- Responsible AI safeguards (bias checks, prompt injection handling)  

#### 📜 License

This project is intended for educational and internal enterprise use.
