import json
import sys

from openai import OpenAI

from src.config import OPENAI_API_KEY
from src.prompts import SYSTEM_PROMPT, build_user_prompt
from src.retrieve import retrieve_movies


client_openai = OpenAI(api_key=OPENAI_API_KEY)


def build_context(movies: list[dict], max_chunks_per_movie: int = 3) -> str:
    context_parts = []

    for movie in movies:
        chunks = movie["chunks"]

        chunk_by_type = {}
        for c in chunks:
            ctype = c["metadata"].get("chunk_type", "unknown")
            chunk_by_type[ctype] = c["text"]

        context_parts.append("=== MOVIE ===")
        context_parts.append(f"Title: {movie['title']}")
        context_parts.append(f"Year: {movie['year']}")

        if "identity" in chunk_by_type:
            context_parts.append("\n[IDENTITY]")
            context_parts.append(chunk_by_type["identity"])

        if "political" in chunk_by_type:
            context_parts.append("\n[POLITICAL]")
            context_parts.append(chunk_by_type["political"])

        if "aesthetic" in chunk_by_type:
            context_parts.append("\n[AESTHETIC]")
            context_parts.append(chunk_by_type["aesthetic"])

        if "availability" in chunk_by_type:
            context_parts.append("\n[AVAILABILITY]")
            context_parts.append(chunk_by_type["availability"])

        context_parts.append("\n")

    return "\n".join(context_parts)


def generate_answer_raw(query: str, context: str) -> str:
    response = client_openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(query, context)},
        ],
    )

    return response.choices[0].message.content or ""


def parse_llm_json(raw_text: str) -> dict:
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        raise ValueError("LLM did not return valid JSON")


def pretty_print_recommendations(data: dict) -> None:
    recommendations = data.get("recommendations", [])

    if not recommendations:
        print("No recommendations found.")
        return

    print("\n💡 Recommendations:\n")

    for i, item in enumerate(recommendations, start=1):
        print(f"{i}. {item.get('title', 'Unknown')} ({item.get('year', 'Unknown')})")
        print(f"   Why match: {item.get('why_match', '')}")
        print(f"   Themes: {', '.join(item.get('themes', []))}")
        print(f"   Tone: {', '.join(item.get('tone', []))}")
        print(f"   Availability: {item.get('availability', 'unknown')}")
        print()


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m src.query \"your query here\" [--debug]")
        return

    query = sys.argv[1]
    debug = "--debug" in sys.argv

    print("\n🔍 Query:")
    print(query)

    movies = retrieve_movies(query=query, debug=debug)

    print(f"\n🎬 Retrieved {len(movies)} movies")

    context = build_context(movies)

    if debug:
        print("\n=== CONTEXT SENT TO LLM ===")
        print(context)

    raw_answer = generate_answer_raw(query, context)

    if debug:
        print("\n=== RAW LLM OUTPUT ===")
        print(raw_answer)

    try:
        parsed = parse_llm_json(raw_answer)
        pretty_print_recommendations(parsed)
    except ValueError as e:
        print("\n⚠ Failed to parse structured output.")
        print(str(e))
        print("\nRaw response:\n")
        print(raw_answer)


if __name__ == "__main__":
    main()