from typing import Any

from pydantic import BaseModel, Field


class AvailabilityEntry(BaseModel):
    platform: str
    region: str
    status: str
    url: str | None = None


class MovieRecord(BaseModel):
    id: str
    title: str
    year: int
    director: str
    countries: list[str] = Field(default_factory=list)
    genres: list[str] = Field(default_factory=list)
    themes: list[str] = Field(default_factory=list)
    tone: list[str] = Field(default_factory=list)
    short_synopsis: str
    long_synopsis: str | None = None
    political_relevance: str
    review_excerpt: str | None = None
    festival_tags: list[str] = Field(default_factory=list)
    availability: list[AvailabilityEntry] = Field(default_factory=list)
    source_urls: list[str] = Field(default_factory=list)


class MovieChunk(BaseModel):
    chunk_id: str
    movie_id: str
    chunk_type: str
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)