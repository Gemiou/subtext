from collections import defaultdict

import chromadb
from openai import OpenAI

from src.config import CHROMA_DIR, OPENAI_API_KEY


client_openai = OpenAI(api_key=OPENAI_API_KEY)

CHUNK_WEIGHTS = {
    "identity": 1.0,
    "political": 1.5,
    "aesthetic": 1.2,
    "availability": 0.4,
}


def embed_text(text: str) -> list[float]:
    response = client_openai.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_collection(name="movies")


def diversify_movies(
    ranked_movies: list[dict],
    max_results: int = 5,
    max_per_director: int = 1,
    debug: bool = False,
) -> list[dict]:
    diversified = []
    used_directors: dict[str, int] = {}
    used_theme_signatures: list[set[str]] = []

    for movie in ranked_movies:
        representative_meta = movie["chunks"][0]["metadata"]

        director = representative_meta.get("director", "unknown")
        themes = set(representative_meta.get("themes", []))

        if used_directors.get(director, 0) >= max_per_director:
            if debug:
                print(f"Skipping {movie['title']} due to repeated director: {director}")
            continue

        too_similar = False
        for used_themes in used_theme_signatures:
            overlap = len(themes & used_themes)
            if overlap >= 3 and len(themes) > 0:
                too_similar = True
                break

        if too_similar:
            if debug:
                print(f"Skipping {movie['title']} due to high theme overlap: {themes}")
            continue

        diversified.append(movie)
        used_directors[director] = used_directors.get(director, 0) + 1
        used_theme_signatures.append(themes)

        if len(diversified) >= max_results:
            break

    return diversified


def retrieve_movies(
    query: str,
    top_k_chunks: int = 10,
    top_k_movies: int = 5,
    debug: bool = False,
) -> list[dict]:
    collection = get_collection()

    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k_chunks,
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    if debug:
        print("\n=== RAW RETRIEVAL RESULTS ===")
        for i, (doc, meta) in enumerate(zip(documents, metadatas), start=1):
            print(f"\n--- CHUNK RESULT {i} ---")
            print("title:", meta.get("title"))
            print("movie_id:", meta.get("movie_id"))
            print("chunk_type:", meta.get("chunk_type"))
            print("year:", meta.get("year"))
            print("director:", meta.get("director"))
            print("themes:", meta.get("themes"))
            print("text:")
            print(doc)

    movie_map = defaultdict(list)

    for doc, meta in zip(documents, metadatas):
        movie_id = meta.get("movie_id")
        movie_map[movie_id].append(
            {
                "text": doc,
                "metadata": meta,
            }
        )

    movie_scores = []

    for movie_id, chunks in movie_map.items():
        score = 0.0
        score_breakdown = []

        for chunk in chunks:
            chunk_type = chunk["metadata"].get("chunk_type", "identity")
            weight = CHUNK_WEIGHTS.get(chunk_type, 1.0)
            score += weight
            score_breakdown.append((chunk_type, weight))

        movie_scores.append(
            {
                "movie_id": movie_id,
                "score": score,
                "score_breakdown": score_breakdown,
            }
        )

    movie_scores.sort(key=lambda x: x["score"], reverse=True)

    if debug:
        print("\n=== MOVIE GROUPING / WEIGHTED SCORING ===")
        for item in movie_scores:
            movie_id = item["movie_id"]
            score = item["score"]
            breakdown = item["score_breakdown"]

            first_meta = movie_map[movie_id][0]["metadata"]

            print(
                f"title={first_meta.get('title')} | "
                f"movie_id={movie_id} | "
                f"score={score:.2f} | "
                f"chunk_count={len(movie_map[movie_id])} | "
                f"breakdown={breakdown}"
            )

    ranked_movies = []

    for item in movie_scores:
        movie_id = item["movie_id"]
        score = item["score"]

        chunks = movie_map[movie_id]
        representative_meta = chunks[0]["metadata"]

        ranked_movies.append(
            {
                "movie_id": movie_id,
                "title": representative_meta.get("title"),
                "year": representative_meta.get("year"),
                "score": score,
                "chunks": chunks,
            }
        )

    if debug:
        print("\n=== RANKED MOVIES BEFORE DIVERSITY ===")
        for i, movie in enumerate(ranked_movies, start=1):
            first_meta = movie["chunks"][0]["metadata"]
            print(
                f"{i}. {movie['title']} ({movie['year']}) | "
                f"director={first_meta.get('director')} | "
                f"themes={first_meta.get('themes')} | "
                f"score={movie['score']:.2f}"
            )

    top_movies = diversify_movies(
        ranked_movies=ranked_movies,
        max_results=top_k_movies,
        max_per_director=2,
        debug=debug,
    )

    if debug:
        print("\n=== FINAL TOP MOVIES AFTER DIVERSITY ===")
        for i, movie in enumerate(top_movies, start=1):
            first_meta = movie["chunks"][0]["metadata"]
            print(
                f"{i}. {movie['title']} ({movie['year']}) | "
                f"director={first_meta.get('director')} | "
                f"themes={first_meta.get('themes')} | "
                f"score={movie['score']:.2f}"
            )

    return top_movies