from src.schema import MovieRecord


def movie_summary(movie: MovieRecord) -> str:
    return f"{movie.title} ({movie.year}) by {movie.director}"


def validate_movies(movies: list[MovieRecord]) -> None:
    for m in movies:
        print("Title: ", m.title)
        print("Themes: ", m.themes)
        if not m.title:
            raise ValueError(f"Missing title in {m.id}")
        if not m.themes:
            raise ValueError(f"No themes in {m.id}")
