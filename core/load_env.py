from dotenv import load_dotenv
import os

load_dotenv()

def get_gemini_api_key() -> str | None:
    return os.getenv("GEMINI_API_KEY")