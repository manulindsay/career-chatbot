# AI Career Guidance Chatbot (France Travail)

This project is a smart, AI-powered career recommendation chatbot developed as part of an AI Capstone. It analyzes user-provided skills (either written manually or extracted from a CV) and recommends relevant jobs based on semantic similarity and real labor market data from France Travail.

## Features

- Two input modes:
  - Manual skill or experience description
  - CV upload (PDF) with automatic skill extraction
- Semantic job matching using `sentence-transformers` (CamemBERT)
- Filter by sector of activity after matching
- Based on real job data from the France Travail API (ROME Métiers)
- Streamlit web interface (local and lightweight)
- Optimized with `st.session_state` for performance

## How It Works

1. The user either writes their skills or uploads a PDF CV
2. The system extracts or processes their skills
3. These are vectorized using a CamemBERT sentence transformer
4. Compared to each job’s skill vector from France Travail
5. Jobs are filtered by semantic similarity (cosine distance)
6. Results are displayed with optional sector filtering

## Tech Stack

| Component         | Tool / Library                        |
|-------------------|----------------------------------------|
| Web Interface     | Streamlit                             |
| NLP / Embeddings  | sentence-transformers, CamemBERT      |
| CV Parsing        | PyMuPDF and spaCy (fr_core_news_md)   |
| Data Source       | France Travail API (ROME métiers)     |
| Optimization      | st.session_state and local caching    |

## Installation

### Requirements

```bash
pip install streamlit sentence-transformers spacy pymupdf
python -m spacy download fr_core_news_md