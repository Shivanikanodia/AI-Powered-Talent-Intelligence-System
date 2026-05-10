### 🧠 AI-Powered Intelligent Recruiter Assistant:

An explainable AI system for semantic resume matching, hybrid candidate ranking, and recruiter-facing insights — designed to reduce manual screening effort and time to fill, eliminate keyword bias, and improve quality of hire. 

### 🚀 Business Problem:

Traditional Applicant Tracking Systems (ATS):

Rely heavily on keyword matching, missing semantic relevance. 

Lack transparency in candidate ranking.

Require manual resume screening, increasing recruiter effort and inconsistent definition and alignment between HM and roles. 

Provide limited support for analytics and decision insights.

### 💡 Solution Overview:

This system converts unstructured resumes into structured, queryable data and applies hybrid  retrieval + re-ranking to identify the most relevant candidates.

### Key Capabilities:

📄 Resume parsing using Databricks AI functions (ai_parse_document, ai_extract)


🧮 Feature-based scoring (skills, experience, domain, seniority)

🔍 Semantic search using Sentence-BERT embeddings + FAISS

🧠 Cross-encoder re-ranking for improved precision

✨ LLM-generated summaries grounded in retrieved evidence

💬 Natural language querying for recruiter-friendly interaction

📊 Explainable ranking outputs (feature contribution, strengths, gaps)

### 💼 Business Impact:
⏱️ Reduces resume screening time significantly
🎯 Improves candidate quality via context aware matching
🤝 Enhances recruiter trust with explainable AI

### 🧠 System Architecture (High-Level)





### 🔍 Data Pipeline:



#### Phase 1: Resume Processing & Structuring

The pipeline transforms unstructured resume PDFs into structured data using Databricks AI functions.

Resumes are complex, they contain columns, tables, and variation in layouts.”


**Ingestion:** Resumes are read from a Unity Catalog Volume using read_files.
**Parsing:** ai_parse_document converts PDFs into structured JSON while preserving layout, Then, ai_parse_document converts each resume into unstructured JSON, breaking it into small blocks called elements.
Each element represents a piece of the resume and contains:
Metadata like type, content, confidence score (reliability of extraction ) and bounding box (position on page)

Finally, I flatten the JSON using explode, where each element becomes a row in a table.
Here, I used ai_extract with a defined schema field like skills, experience, and education, ensuring consistency and instructions to convert the row level parsed resume data into a structured candidate profile for querying and analysis.

<img width="783" height="66" alt="Screenshot 2026-04-27 at 19 06 07" src="https://github.com/user-attachments/assets/62076fa3-5efe-4a1e-8983-be1e5cde47df" />


**Modeling:** 
Data is flattened into tables (resume_core, resume_skills, resume_experience, resume_education) for efficient ** querying.

<img width="547" height="532" alt="Screenshot 2026-04-27 at 18 58 28" src="https://github.com/user-attachments/assets/a46bf4da-9bdf-4e54-8c3a-42ddd715d6b3" />


  
**Data cleaning (formatting, normalization, Unicode handling)**
- Synonym expansion + ontology-based mapping

<img width="729" height="195" alt="Screenshot 2026-04-27 at 19 07 41" src="https://github.com/user-attachments/assets/ca868aa9-845f-4b5b-aaa3-b390387b11a2" />

#### Phase 2: Features Scoring 

I compute lightweight structured features like skill match, experience fit, and location match.

I assigned weights based on their importance towards hiring criteria. and returned  a final features score.

- Skill overlap
- Experience alignment
- Domain relevance
- Education and location alignment


#### Phase 2: Embeddings & Retrieval:

Resume Chunking - For 500 resumes nearly ~15,000 raw chunks and ~3,400 cleaned chunks.

<img width="622" height="424" alt="Screenshot 2026-04-27 at 19 09 42" src="https://github.com/user-attachments/assets/a183d514-d183-4af1-b980-fce7f6889d37" />

- Section-level embeddings using Sentence-BERT
- Stored in FAISS for fast similarity search
- Convert recruiter query → embeddings
- Retrieve top N relevant resume sections
- Aggregate to compute resume-level relevance


- Joint evaluation of query + resume
- Improves contextual understanding and ranking precision

### 📊 Candidate Summary & Explainability Layer

The system leverages the Genie Interaction Layer and LLM Model to to generate concise, evidence-based candidate summaries and recruiter recommendations. These summaries are strictly grounded in retrieved resume sections, ensuring high factual accuracy and minimizing hallucinations.

###  PHASE 4: STREAMLIT APP:


Natural lanuage search interface:
Example query: Find software engineers in USA with 5 to 13 years of experience and skills Python, Java, and system design
Click Run Search.



####  Candidate List + Scorecard: 

#### Fit Assesment
Candidate ranking is decomposed into interpretable components such as:

must_have_skill_coverage
Experience_fitment
Domain_fit
location_match
Education relevance

This allows recruiters to clearly understand why a candidate is ranked higher or lower.


##### Resume Evidnece
Evidnece of skills are generated using only the most relevant retrieved resume segments (via semantic search + cross encoder), ensuring every statement is traceable to source data.
Each evidence is backed by explicit references to resume sections (experience, skills, projects), enabling transparency and trust.


### Hiring Signals/Career Trajectory: 

Recruiters also care about stability and growth. Here I show average tenure, employer transitions and progression.
These are calculated from work history rather than generated by the model


### Recruiter summaries:

The LLM is used only after scoring and evidence extraction. It does not decide the score. It summarizes the candidate for recruiter review, highlights strengths, gaps, and suggests a screening question.
So instead of keyword filtering, this system enables transparent, evidence-based candidate evaluation.



### PHASE 4: 📊 Evaluation Metrics:

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


I evaluated model performance using metrics like precision@k, NDCG@K and MRR@K against ground truth labels. 

The cross-encoder gives the best ranking quality, achieving highest NDCG and MRRof 1 meaning the best candidate is ranked first.  
The hybrid model improves over semantic search by combining multiple signals.




#### 🛠️ Tech Stack
Python 3.10
FAISS
Sentence-Transformers
Cross-Encoder (MiniLM)
Databricks (Delta Lake, AI Functions)
SQL + Semantic Data Models

#### 📁 Project Structure

app.py         
     # Streamlit UI for querying and results

preprocessing.py   
     # Resume parsing, cleaning, metadata extraction

build_index.py      
 
    # Embedding generation and FAISS indexing

config.py         

    # Configurations and scoring weights


#### Implemented:
Resume preprocessing
Semantic retrieval (FAISS)
Feature-based scoring
Hybrid ranking
Explainability outputs
Benchmark RAG vs Cross-Encoder vs Hybrid approaches  

### 🔮 Future Work
- MLflow-based evaluation and experiment tracking  
- Responsible AI safeguards (bias checks, prompt injection handling)  

#### 📜 License

This project is intended for educational and internal enterprise use.

