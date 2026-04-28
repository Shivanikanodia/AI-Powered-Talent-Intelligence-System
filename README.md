### 🧠 AI-Powered Intelligent Recruiter Assistant:

An explainable AI system for semantic resume matching, hybrid candidate ranking, and recruiter-facing insights — designed to reduce manual screening effort, eliminate keyword bias, and improve candidate discovery.

### 🚀 Business Problem:

Traditional Applicant Tracking Systems (ATS):

Rely heavily on keyword matching, missing semantic relevance
Lack transparency in candidate ranking
Require manual resume screening, increasing recruiter effort
Provide limited support for analytics and decision insights

### 💡 Solution Overview:

This system converts unstructured resumes into structured, queryable data and applies hybrid retrieval + ranking to identify the most relevant candidates.

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
📈 Scales across large candidate datasets
🤝 Enhances recruiter trust with explainable AI

### 🧠 System Architecture (High-Level)
Recruiter Query → Embedding → FAISS Retrieval → Aggregation  
→ Feature Scoring → Cross-Encoder Re-ranking → LLM Summary

### 🔍 Data Pipeline

#### Phase 1: Resume Processing & Structuring
Ingestion from Unity Catalog volumes
Parsing PDFs → structured JSON (ai_parse_document)
Information extraction (ai_extract, 2-pass approach)

#### Data modeling into structured tables:

- resume_core
- resume_skills
- resume_experience
- resume_education
- Data cleaning (formatting, normalization, Unicode handling)
- Synonym expansion + ontology-based mapping

#### Phase 2: Embeddings & Indexing:

- Section-level embeddings using Sentence-BERT
- Stored in FAISS for fast similarity search

#### Phase 3: Retrieval

- Convert recruiter query → embeddings
- Retrieve top-N relevant resume sections
- Aggregate to compute resume-level relevance

#### Phase 4: Scoring & Re-Ranking

- Feature-based scoring:
- Skill overlap
- Experience alignment
- Domain relevance
- Seniority fit
- Gap analysis

#### Cross-encoder re-ranking:

- Joint evaluation of query + resume
- Improves contextual understanding and ranking precision

#### Phase 5: Summary Generation

- Controlled LLM (Llama 3 via Ollama)
- Generates concise, evidence-based summaries
- Grounded in retrieved resume sections (reduces hallucination

#### 🔎 Explainability & Transparency

- Feature-level contribution to ranking
- Clear reasoning behind candidate ordering

#### Highlights:

- Strengths
- Gaps
- Matching evidence

#### 📊 Evaluation Metrics:

- ⏱️ Latency (retrieval, ranking, generation)
- 🎯 Precision@K / Recall@K
- 📈 Relevance score (semantic similarity)
- 🔁 Consistency & hallucination checks
- ⚖️ Scoring Approaches Compared

- RAG-only (semantic similarity)
 
- Cross-encoder + RAG
  
- Hybrid (Feature scoring + Cross-encoder + RAG) ✅

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
