import chromadb
from collections import defaultdict

from openai import OpenAI

from src.config import CHROMA_DIR, OPENAI_API_KEY


client_openai = OpenAI(api_key=OPENAI_API_KEY)


def embed_text(text: str) -> list[float]:
    response = client_openai.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_collection(name="movies")


def retrieve_movies(query: str, top_k_chunks: int = 10, top_k_movies: int = 5):
    collection = get_collection()

    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k_chunks,
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # 👉 Group chunks by movie_id
    movie_map = defaultdict(list)

    for doc, meta in zip(documents, metadatas):
        movie_id = meta.get("movie_id")
        movie_map[movie_id].append({
            "text": doc,
            "metadata": meta
        })

    # 👉 Score movies (simple count-based)
    movie_scores = [
        (movie_id, len(chunks))
        for movie_id, chunks in movie_map.items()
    ]

    # Sort descending
    movie_scores.sort(key=lambda x: x[1], reverse=True)

    # 👉 Keep top movies
    top_movies = []

    for movie_id, _ in movie_scores[:top_k_movies]:
        top_movies.append({
            "movie_id": movie_id,
            "chunks": movie_map[movie_id],
        })

    return top_movies