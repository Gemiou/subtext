import chromadb
from openai import OpenAI

from src.config import CHROMA_DIR, OPENAI_API_KEY

client_openai = OpenAI(api_key=OPENAI_API_KEY)

def embed_text(text: str) -> list[float]:
    response = client_openai.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding

def main() -> None:
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(name="movies")

    query = "political films about surveillance and corruption"
    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
    )

    print("QUERY:")
    print(query)
    print()

    print("TOP RESULTS:")
    for i, doc in enumerate(results["documents"][0]):
        print(f"--- RESULT {i+1} ---")
        print(doc)
        print()

    print("METADATA:")
    for meta in results["metadatas"][0]:
        print(meta)

if __name__ == "__main__":
    main()