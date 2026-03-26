import sys
from openai import OpenAI

from src.config import OPENAI_API_KEY
from src.retrieve import retrieve_movies
from src.prompts import SYSTEM_PROMPT, build_user_prompt


client_openai = OpenAI(api_key=OPENAI_API_KEY)


def build_context(movies: list[dict]) -> str:
    context_parts = []

    for movie in movies:
        chunks = movie["chunks"]

        for c in chunks:
            context_parts.append(c["text"])

    return "\n\n".join(context_parts)


def generate_answer(query: str, context: str) -> str:
    response = client_openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(query, context)},
        ],
    )

    return response.choices[0].message.content


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src.query 'your query here'")
        return

    query = sys.argv[1]

    print("\n🔍 Query:", query)

    # Step 1 — Retrieve
    movies = retrieve_movies(query)

    print(f"\n🎬 Retrieved {len(movies)} movies")

    # Step 2 — Build context
    context = build_context(movies)

    # Step 3 — LLM answer
    answer = generate_answer(query, context)

    print("\n💡 Recommendations:\n")
    print(answer)


if __name__ == "__main__":
    main()