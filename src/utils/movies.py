from src.schema import MovieRecord


def movie_summary(movie: MovieRecord) -> str:
    return f"{movie.title} ({movie.year}) by {movie.director}"


