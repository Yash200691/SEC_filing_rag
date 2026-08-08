# 📊 Production-Grade Financial RAG

A production-oriented **Retrieval-Augmented Generation (RAG)** system for querying financial documents using semantic search, vector retrieval, context construction, prompt engineering, and an LLM served through **Groq**.

The current implementation uses:

- **Python 3.11**
- **BAAI/bge-base-en-v1.5** for embeddings
- **Qdrant** for vector storage and similarity search
- **Groq** for LLM inference through an OpenAI-compatible API
- **Pydantic Settings** for configuration management
- **Docker** for running Qdrant locally

The project is designed to make the complete RAG pipeline understandable and modular while keeping the architecture suitable for further production improvements.

---

## 🚀 Project Overview

Traditional LLM applications have one major limitation: the model only knows the information available in its training/context window.

A RAG system solves this by retrieving relevant information from an external knowledge base before asking the LLM to generate an answer.

This project follows the pipeline:

```text
                    User Question
                         │
                         ▼
                ┌─────────────────┐
                │  Search Engine  │
                └────────┬────────┘
                         │
                  Query Embedding
                         │
                         ▼
                ┌─────────────────┐
                │     Qdrant      │
                │ Vector Database │
                └────────┬────────┘
                         │
                  Relevant Chunks
                         │
                         ▼
              ┌─────────────────────┐
              │  Context Builder    │
              └──────────┬──────────┘
                         │
                      Context
                         │
                         ▼
              ┌─────────────────────┐
              │   Prompt Builder    │
              └──────────┬──────────┘
                         │
                       Prompt
                         │
                         ▼
              ┌─────────────────────┐
              │    Groq LLM         │
              └──────────┬──────────┘
                         │
                      Answer
                         │
                         ▼
                    User Response
```

---

# ✨ Features

- 📄 Financial document ingestion pipeline
- 🧹 Document cleaning and preprocessing
- ✂️ Document chunking
- 🧠 Semantic embeddings using `BAAI/bge-base-en-v1.5`
- 🔎 Vector similarity search with Qdrant
- 🧩 Optional metadata filtering
- 📝 Context construction from retrieved chunks
- 💬 Dedicated prompt-building layer
- ⚡ Fast LLM inference through Groq
- ⚙️ Centralized configuration using Pydantic Settings
- 🐳 Dockerized Qdrant
- 🔐 Environment-variable based API key management
- 🧱 Modular architecture
- 🧪 Easy CLI-based testing
- 🔍 Retrieval debugging through scores and retrieved payloads

---

# 🏗️ Architecture

The project is intentionally divided into small components.

```text
RAG/
│
├── data/
│   ├── raw/
│   ├── cleaned/
│   ├── html/
│   ├── metadata/
│   ├── sections/
│   └── chunks/
│
├── retriever/
│   ├── __init__.py
│   ├── context_builder.py
│   ├── embedding.py
│   ├── formatter.py
│   ├── LLM.py
│   ├── prompt_builder.py
│   ├── qdrant_client.py
│   ├── RAGPipeline.py
│   ├── search.py
│   ├── tokenizer.py
│   └── utils.py
│
├── scripts/
│   └── ...
│
├── config.py
├── main.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

---

# 🧩 Core Components

## 1. `embedding.py`

Responsible for converting text into numerical vectors.

```text
Text
 ↓
BGE Embedding Model
 ↓
768-dimensional vector
```

The project currently uses:

```text
BAAI/bge-base-en-v1.5
```

The same embedding model should be used during both:

- document indexing
- user-query retrieval

This is important because the vectors need to exist in the same embedding space.

---

## 2. `qdrant_client.py`

Provides the application-level interface to Qdrant.

Responsibilities include:

- connecting to Qdrant
- checking collections
- retrieving collection information
- constructing metadata filters
- performing vector searches
- formatting retrieved points

The application connects to:

```text
http://localhost:6333
```

during local development.

---

## 3. `search.py`

`SearchEngine` connects the embedding model and Qdrant together.

```text
User Question
      │
      ▼
EmbeddingModel
      │
      ▼
Query Vector
      │
      ▼
QdrantDB
      │
      ▼
Relevant Results
```

Example:

```python
results = search_engine.search(
    question="What was Apple's total net sales in 2023?",
    top_k=5,
)
```

---

## 4. `context_builder.py`

The Qdrant search returns structured results.

The context builder converts those results into text that can be supplied to the LLM.

```text
Qdrant Results
      │
      ▼
Extract payload text
      │
      ▼
Combine relevant chunks
      │
      ▼
LLM Context
```

---

## 5. `prompt_builder.py`

Responsible for constructing the final prompt.

Conceptually:

```text
System Instructions
        +
Retrieved Context
        +
User Question
        ↓
      Prompt
```

The prompt instructs the model to answer using the supplied document context rather than inventing information.

---

## 6. `LLM.py`

The LLM layer communicates with **Groq**.

The implementation uses the OpenAI-compatible client interface with the Groq API endpoint.

Conceptually:

```text
Prompt
  │
  ▼
Groq API
  │
  ▼
LLM
  │
  ▼
Generated Answer
```

The LLM provider is isolated from the rest of the RAG pipeline so the rest of the system does not need to know how the provider is implemented.

---

## 7. `RAGPipeline.py`

This is the orchestration layer.

It combines all the components:

```python
pipeline = RAGPipeline()

answer = pipeline.ask(
    "What was Apple's total net sales in 2023?"
)
```

Internally:

```text
Question
   ↓
Search
   ↓
Retrieved Chunks
   ↓
Context
   ↓
Prompt
   ↓
Groq
   ↓
Answer
```

This gives the application a simple public interface:

```python
pipeline.ask(question)
```

---

# ⚙️ Configuration

Configuration is centralized in `config.py`.

The project uses **Pydantic Settings**.

Example:

```python
from config import settings

settings.EMBEDDING_MODEL
settings.QDRANT_URL
settings.COLLECTION_NAME
settings.VECTOR_SIZE
settings.CHUNK_DIRECTORY
settings.BATCH_SIZE
```

Configuration is loaded from `.env`.

Example `.env`:

```env
EMBEDDING_MODEL=BAAI/bge-base-en-v1.5

QDRANT_URL=http://localhost:6333
COLLECTION_NAME=financial_rag
VECTOR_SIZE=768

CHUNK_DIRECTORY=data/chunks
BATCH_SIZE=64

GROQ_API_KEY=YOUR_GROQ_API_KEY
GROQ_MODEL=YOUR_GROQ_MODEL
```

> Never commit `.env` or API keys to GitHub.

Create `.env.example` with placeholder values instead.

---

# 🐳 Running Qdrant with Docker

Qdrant is used as the vector database.

## Create a persistent volume

```powershell
docker volume create qdrant_storage
```

## Start Qdrant

PowerShell:

```powershell
docker run -d `
  --name qdrant `
  -p 127.0.0.1:6333:6333 `
  -p 127.0.0.1:6334:6334 `
  -v qdrant_storage:/qdrant/storage `
  qdrant/qdrant:latest
```

Or as a single line:

```powershell
docker run -d --name qdrant -p 127.0.0.1:6333:6333 -p 127.0.0.1:6334:6334 -v qdrant_storage:/qdrant/storage qdrant/qdrant:latest
```

Check the container:

```powershell
docker ps
```

You should see port mappings similar to:

```text
127.0.0.1:6333->6333/tcp
127.0.0.1:6334->6334/tcp
```

Qdrant dashboard:

```text
http://localhost:6333/dashboard
```

---

# 🛠️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/<YOUR_USERNAME>/<YOUR_REPOSITORY>.git
cd <YOUR_REPOSITORY>
```

## 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

## 4. Create `.env`

Copy the example:

```powershell
copy .env.example .env
```

Then add your actual Groq API key.

---

# ▶️ Running the Application

Make sure Qdrant is running:

```powershell
docker ps
```

Then start the application from the project root:

```powershell
python main.py
```

You should see something similar to:

```text
Loading Embedding Model...
Embedding Model Loaded.

Connecting to Qdrant...
Connected Successfully!

Ask:
```

Enter a question:

```text
Ask: What was Apple's total net sales in 2023?
```

---

# 🧪 Example Questions

## Basic retrieval

```text
What was Apple's total net sales in 2023?
```

```text
What was Apple's net income in 2023?
```

```text
How much cash, cash equivalents, and unrestricted marketable securities did Apple have as of September 30, 2023?
```

```text
How much did Apple spend on share repurchases in 2023?
```

---

## Comparison

```text
How did Apple's total net sales in 2023 compare with 2022?
```

```text
Which geographic segment generated the highest net sales in 2023?
```

```text
Compare Apple's Americas and Europe net sales in 2023.
```

---

## Reasoning

```text
Why did Apple's net sales decrease in 2023 compared with 2022?
```

```text
What factors affected Apple's financial performance in 2023?
```

```text
What impact did foreign currency fluctuations have on Apple's business in 2023?
```

---

## Financial position

```text
What were Apple's major cash requirements?
```

```text
How much debt did Apple have outstanding as of September 30, 2023?
```

```text
How much commercial paper did Apple have outstanding?
```

---

## Risk analysis

```text
What major risks did Apple identify in its 2023 Form 10-K?
```

```text
What macroeconomic conditions affected Apple's results?
```

```text
What risks did Apple mention regarding inflation and interest rates?
```

---

# 🚨 Hallucination Test

A good RAG system should not confidently answer questions that aren't supported by the retrieved documents.

Try:

```text
What was Microsoft's revenue in 2023?
```

or:

```text
What was Tesla's net income in 2023?
```

The expected behavior is an answer similar to:

```text
I don't have enough information from the provided documents.
```

This is an important test because a RAG system should be grounded in its retrieved context.

---

# 🔍 Debugging Retrieval

During development, the pipeline can print retrieved search results.

A typical result contains:

```python
{
    "id": 139,
    "score": 0.753,
    "payload": {
        "chunk_id": 42,
        "section": "Item 7",
        "text": "..."
    }
}
```

The similarity score helps inspect whether the retrieved chunks are relevant.

For example:

```text
Question
   ↓
Top-K Retrieval
   ↓
┌──────────────────────────────┐
│ Chunk 1   Score: 0.89        │
│ Chunk 2   Score: 0.84        │
│ Chunk 3   Score: 0.81        │
│ Chunk 4   Score: 0.77        │
│ Chunk 5   Score: 0.75        │
└──────────────────────────────┘
```

This makes it easier to determine whether an incorrect answer is caused by:

- poor retrieval
- poor chunking
- noisy context
- prompt problems
- LLM generation

---

# 📁 Data Pipeline

The data directory is separated into stages:

```text
data/
│
├── raw/
│       Original documents
│
├── cleaned/
│       Cleaned document text
│
├── html/
│       HTML representations
│
├── metadata/
│       Document metadata
│
├── sections/
│       Extracted document sections
│
└── chunks/
        Final chunks used for embedding/retrieval
```

The general ingestion flow is:

```text
Raw Documents
      ↓
Document Extraction
      ↓
Cleaning
      ↓
Section Detection
      ↓
Chunking
      ↓
Metadata
      ↓
Embeddings
      ↓
Qdrant
```

---

# 🔐 Security

The following should never be committed:

```text
.env
API keys
credentials
private configuration
local vector database storage
Python virtual environments
generated caches
```

The `.gitignore` file is configured to exclude sensitive and generated files.

Use:

```text
.env.example
```

to document required environment variables without exposing secrets.

---

# 🧠 Why This Architecture?

The project intentionally separates responsibilities.

Instead of creating one large file:

```text
rag.py
```

containing everything, the system separates:

```text
Embedding
   ↓
Retrieval
   ↓
Context
   ↓
Prompt
   ↓
LLM
```

This provides:

### Maintainability

Each component can be modified independently.

### Testability

Individual components can be tested separately.

### Scalability

The vector database, embedding model, and LLM layer can evolve independently.

### Provider flexibility

The LLM provider can be replaced without rewriting the retrieval system.

### Debuggability

Failures can be isolated to a specific stage.

---

# 📈 Current RAG Pipeline

```text
                    ┌─────────────────┐
                    │  User Question  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Embedding    │
                    │ BGE-base-en-v1.5│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     Qdrant      │
                    │  Vector Search  │
                    └────────┬────────┘
                             │
                       Top-K Chunks
                             │
                             ▼
                    ┌─────────────────┐
                    │ Context Builder │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Prompt Builder  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │      Groq       │
                    │       LLM       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Final Answer   │
                    └─────────────────┘
```

---

# 📊 Example

Question:

```text
What was Apple's total net sales in 2023?
```

Retrieval can find a chunk containing:

```text
Total net sales
$383,285 million
```

The LLM receives that retrieved information and produces:

```text
Apple's total net sales in fiscal 2023 were approximately
$383.3 billion.
```

The key idea is that the answer is grounded in the retrieved document rather than relying only on the model's internal knowledge.

---

# 🧪 Evaluation Strategy

A RAG system should not be evaluated only by checking whether the final answer "looks good."

Evaluation should consider:

## Retrieval Quality

Did the system retrieve the correct chunk?

```text
Question
   ↓
Top-K Results
   ↓
Relevant chunk?
```

## Context Quality

Did the final context contain enough information to answer the question?

## Groundedness

Is the answer supported by the retrieved context?

## Answer Correctness

Does the generated answer match the source information?

## Hallucination Resistance

Does the system refuse questions that aren't supported by the available documents?

---

# 🚧 Known Areas for Improvement

The current system is a strong baseline, but there are several areas that can be improved.

### 1. Better PDF/table extraction

Financial reports contain many tables where normal PDF text extraction can lose alignment between labels and numeric values.

This is particularly important for:

- income statements
- balance sheets
- cash flow statements
- segment revenue tables
- financial ratios

Improving table-aware extraction is therefore a major priority.

### 2. Better chunking

Large chunks can introduce irrelevant information into the context.

Future improvements can include:

- recursive chunking
- semantic chunking
- section-aware chunking
- table-aware chunking
- adaptive chunk sizes
- overlap tuning

### 3. Reranking

Current retrieval is based on vector similarity.

A reranker can improve precision:

```text
Query
 ↓
Vector Search
 ↓
Top 20-50 candidates
 ↓
Cross-Encoder Reranker
 ↓
Top 5
 ↓
LLM
```

### 4. Hybrid Search

Combine:

```text
Dense Vector Search
        +
Keyword/BM25 Search
```

This is particularly useful for financial documents because exact terms, numbers, company names, and section titles matter.

### 5. Citations

The answer should eventually include:

```text
Answer

Sources:
- Apple 2023 Form 10-K
- Item 7
- Chunk 42
```

### 6. Query Rewriting

Complex user questions can be rewritten before retrieval.

### 7. Multi-Query Retrieval

Generate multiple search queries for difficult questions and combine their results.

### 8. Conversation Memory

Support follow-up questions such as:

```text
User:
What was Apple's revenue in 2023?

User:
How did it compare with 2022?
```

### 9. Streaming

Stream LLM tokens instead of waiting for the complete answer.

### 10. Observability

Add metrics for:

- embedding latency
- retrieval latency
- number of retrieved chunks
- similarity scores
- context length
- LLM latency
- total request latency
- token usage
- failure rates

---

# 🗺️ Roadmap

## Phase 1 — Core RAG ✅

- [x] Document ingestion
- [x] Document cleaning
- [x] Chunk generation
- [x] Embedding generation
- [x] Qdrant integration
- [x] Semantic retrieval
- [x] Context building
- [x] Prompt construction
- [x] Groq integration
- [x] End-to-end RAG pipeline

## Phase 2 — Retrieval Quality

- [ ] Improve financial table extraction
- [ ] Improve chunking
- [ ] Metadata-aware retrieval
- [ ] Hybrid search
- [ ] Cross-encoder reranking
- [ ] Retrieval evaluation
- [ ] Source citations

## Phase 3 — Advanced RAG

- [ ] Query rewriting
- [ ] Multi-query retrieval
- [ ] Context compression
- [ ] Conversation memory
- [ ] Streaming
- [ ] Better hallucination control

## Phase 4 — Production

- [ ] FastAPI API
- [ ] Dockerize application
- [ ] Redis caching
- [ ] Authentication
- [ ] Rate limiting
- [ ] Structured logging
- [ ] Monitoring
- [ ] RAG evaluation framework
- [ ] Production deployment

---

# 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| Embeddings | BAAI/bge-base-en-v1.5 |
| Vector Database | Qdrant |
| Vector DB Deployment | Docker |
| LLM Provider | Groq |
| Configuration | Pydantic Settings |
| API Client | OpenAI-compatible Python client |
| Environment Management | `.env` |
| Development | VS Code |
| Version Control | Git + GitHub |

---

# 🎯 Project Goals

This project is built with two goals:

### 1. Build a functional financial RAG system

The system should retrieve information from financial documents and generate grounded answers.

### 2. Learn production RAG architecture

The project focuses on understanding the complete pipeline rather than hiding everything behind a high-level framework.

The architecture makes each stage explicit:

```text
Ingestion
   ↓
Chunking
   ↓
Embedding
   ↓
Vector Storage
   ↓
Retrieval
   ↓
Context Construction
   ↓
Prompt Engineering
   ↓
LLM Generation
   ↓
Evaluation
```

---

# 🤝 Contributing

Contributions and improvements are welcome.

Typical contribution areas include:

- retrieval improvements
- chunking strategies
- document parsing
- table extraction
- evaluation
- prompt engineering
- API development
- testing
- observability

---

# 📄 License

Add the appropriate license for your repository.

---

# ⭐ Final Note

This project is intentionally being developed incrementally.

The current version focuses on understanding and implementing the core RAG architecture before adding advanced retrieval and production infrastructure.

The long-term goal is to evolve this baseline into a robust financial document question-answering system with:

```text
High-quality ingestion
        +
Strong retrieval
        +
Reranking
        +
Grounded generation
        +
Citations
        +
Evaluation
        +
Observability
```

---

## Built with Python, Qdrant, BGE embeddings, and Groq.
