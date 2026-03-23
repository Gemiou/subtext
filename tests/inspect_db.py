import chromadb

from src.config import CHROMA_DIR

def main() -> None:
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(name="movies")

    results = collection.get(limit=5)

    print("IDS:")
    print(results["ids"])
    print()

    print("DOCUMENTS:")
    for doc in results["documents"]:
        print("---")
        print(doc)
        print()

    print("METADATAS:")
    for meta in results["metadatas"]:
        print(meta)

if __name__ == "__main__":
    main()