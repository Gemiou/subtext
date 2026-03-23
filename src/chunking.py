from typing import List

from src.schema import MovieRecord, MovieChunk


def build_chunks(movie: MovieRecord) -> List[MovieChunk]:
    chunks: List[MovieChunk] = []

    base_metadata = {
        "movie_id": movie.id,
        "title": movie.title,
        "year": movie.year,
        "director": movie.director,
        "genres": movie.genres,
        "themes": movie.themes,
    }

    # Chunk 1 — Identity + Synopsis
    text_1 = f"""
Title: {movie.title}
Year: {movie.year}
Director: {movie.director}
Genres: {", ".join(movie.genres)}
Themes: {", ".join(movie.themes)}
Synopsis: {movie.short_synopsis}
""".strip()

    chunks.append(
        MovieChunk(
            chunk_id=f"{movie.id}_identity",
            movie_id=movie.id,
            chunk_type="identity",
            text=text_1,
            metadata={
                **base_metadata,
                "chunk_type": "identity",
            },
        )
    )

    # Chunk 2 — Political Meaning
    text_2 = f"""
Title: {movie.title}
Year: {movie.year}
Director: {movie.director}
Themes: {", ".join(movie.themes)}
Political relevance: {movie.political_relevance}
""".strip()

    chunks.append(
        MovieChunk(
            chunk_id=f"{movie.id}_political",
            movie_id=movie.id,
            chunk_type="political",
            text=text_2,
            metadata={
                **base_metadata,
                "chunk_type": "political",
            },
        )
    )

    # Chunk 3 — Aesthetic / Tone
    if movie.review_excerpt or movie.tone:
        tone_text = ", ".join(movie.tone) if movie.tone else "unknown"
        review_text = movie.review_excerpt if movie.review_excerpt else "No review excerpt available."

        text_3 = f"""
Title: {movie.title}
Year: {movie.year}
Director: {movie.director}
Tone: {tone_text}
Review: {review_text}
""".strip()

        chunks.append(
            MovieChunk(
                chunk_id=f"{movie.id}_aesthetic",
                movie_id=movie.id,
                chunk_type="aesthetic",
                text=text_3,
                metadata={
                    **base_metadata,
                    "chunk_type": "aesthetic",
                    "tone": movie.tone,
                },
            )
        )

    # Chunk 4 — Availability
    if movie.availability:
        availability_text = ", ".join(
            [f"{a.platform} ({a.region}) - {a.status}" for a in movie.availability]
        )

        text_4 = f"""
Title: {movie.title}
Availability: {availability_text}
""".strip()

        chunks.append(
            MovieChunk(
                chunk_id=f"{movie.id}_availability",
                movie_id=movie.id,
                chunk_type="availability",
                text=text_4,
                metadata={
                    **base_metadata,
                    "chunk_type": "availability",
                },
            )
        )

    return chunks