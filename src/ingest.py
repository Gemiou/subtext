import json
from pathlib import Path

import chromadb
from openai import OpenAI

from src.schema import MovieRecord
from src.utils.movies import validate_movies
from src.chunking import build_chunks
from src.config import CHROMA_DIR, OPENAI_API_KEY


client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection(name="movies")

client_openai = OpenAI(api_key=OPENAI_API_KEY)


def load_movies(path: str | Path) -> list[MovieRecord]:
    path = Path(path)

    with path.open("r", encoding="utf-8") as f:
        raw_data = json.load(f)

    movies = [MovieRecord(**item) for item in raw_data]
    return movies


def embed_text(text: str) -> list[float]:
    response = client_openai.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding


def main() -> None:
    all_chunks = []

    movies = load_movies("data/movies.json")
    validate_movies(movies)

    for movie in movies:
        chunks = build_chunks(movie)
        all_chunks.extend(chunks)

    with open("data/processed/chunks_debug.json", "w", encoding="utf-8") as f:
        json.dump([c.dict() for c in all_chunks], f, indent=2, ensure_ascii=False)

    for chunk in all_chunks:
        embedding = embed_text(chunk.text)

        collection.upsert(
            ids=[chunk.chunk_id],
            documents=[chunk.text],
            embeddings=[embedding],
            metadatas=[chunk.metadata],
        )

    print(f"Inserted {len(all_chunks)} chunks into collection 'movies'")


if __name__ == "__main__":
    main()