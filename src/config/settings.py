import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    MODEL_NAME: str = "llama-3.1-8b-instant"
    TEMPERATURE: float = 0.9
    MAX_RETRYS: int = 3

settings = Settings()