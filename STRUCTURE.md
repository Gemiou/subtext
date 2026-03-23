# Project Structure

```bash
movie-rag/
├── data/                     # Contains all project data (raw and processed knowledge)
│   ├── raw/                  # Unprocessed data (initial movie lists, notes, scraped data)
│   ├── processed/            # Cleaned/transformed data (chunks, embeddings, vector storage)
│   └── movies.json           # Main curated dataset with movie records and metadata
│
├── src/                      # Core application logic (the "brain" of the system)
│   ├── __init__.py           # Makes src a Python package (enables clean imports)
│   ├── config.py             # Central configuration (env variables, paths, constants)
│   ├── schema.py             # Data models (MovieRecord, Availability, MovieChunk)
│   ├── chunking.py           # Splits movie data into semantic chunks for retrieval
│   ├── ingest.py             # Data pipeline (load → validate → chunk → index)
│   ├── retrieve.py           # Semantic search logic (query → relevant chunks → movies)
│   ├── prompts.py            # LLM prompts and response rules (grounded generation)
│   ├── query.py              # Main entrypoint (connects retrieval + LLM output)
│   └── utils.py              # Helper functions (formatting, debugging, small utilities)
│
├── tests/                    # Testing and evaluation
│   └── test_queries.md       # Sample user queries for manual evaluation and benchmarking
│
├── notebooks/                # Experimentation environment
│   └── exploration.ipynb     # Data exploration, debugging, quick experiments
│
├── .env                      # Environment variables (API keys, config settings)
├── requirements.txt          # Python dependencies for reproducible setup
└── README.md                 # Project documentation (this file)