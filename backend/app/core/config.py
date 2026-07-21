from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH")
    DATA_FOLDER = os.getenv("DATA_FOLDER")

settings = Settings()