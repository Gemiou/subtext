from src.config import APP_ENV, CHROMA_DIR, OPENAI_API_KEY

def print_config_summary() -> None:
    print("APP_ENV:", APP_ENV)
    print("CHROMA_DIR:", CHROMA_DIR)
    print("OPENAI_API_KEY loaded:", bool(OPENAI_API_KEY))