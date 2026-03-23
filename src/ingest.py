import json
from pathlib import Path

from src.schema import MovieRecord
from src.utils.movies import validate_movies


def load_movies(path: str | Path) -> list[MovieRecord]:
    path = Path(path)

    with path.open("r", encoding="utf-8") as f:
        raw_data = json.load(f)
    movies = [MovieRecord(**item) for item in raw_data]
    return movies


def main() -> None:
    movies = load_movies("data/movies.json")
    print(f"Loaded {len(movies)} movies successfully.")

    validate_movies(movies)

    for movie in movies:
        print(f"- {movie.id}: {movie.title} ({movie.year}) | themes={movie.themes}")


if __name__ == "__main__":
    main()