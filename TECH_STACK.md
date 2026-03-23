
## 🛠️ The Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **LLM & Embeddings** | [OpenAI](https://platform.openai.com/) | Brains for semantic embeddings and text generation. |
| **Vector Database** | [ChromaDB](https://docs.trychroma.com/) | Local, high-performance storage for vector embeddings. |
| **Schema Validation** | [Pydantic](https://docs.pydantic.dev/) | Data integrity and structured LLM outputs. |
| **Data Engineering** | [Pandas](https://pandas.pydata.org/) | Data cleaning, inspection, and batch processing. |
| **Environment** | [python-dotenv](https://github.com/theskumar/python-dotenv) | Secure management of API keys and configurations. |
| **Testing** | [Pytest](https://docs.pytest.org/) | Unit testing for retrieval logic and model reliability. |
| **R&D / Docs** | [Jupyter](https://jupyter.org/) | Interactive "Living README" for exploration and debugging. |

---

## 🏗️ Project Architecture

1.  **Ingestion:** Raw data is loaded via `pandas`, cleaned, and validated using `pydantic` models.
2.  **Embedding:** Text chunks are transformed into vectors using OpenAI’s `text-embedding-3` models.
3.  **Storage:** Vectors and metadata are persisted in a local `chromadb` instance.
4.  **Retrieval:** Semantic search identifies the most relevant context for a user query.
5.  **Inference:** OpenAI generates a response using the retrieved context, enforced by a `pydantic` schema for consistent application logic.

---

## 🚀 Getting Started

### 1. Installation
Ensure you have Python 3.9+ installed, then run:
```bash
pip install openai chromadb pydantic python-dotenv pandas pytest jupyter