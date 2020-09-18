import os
from typing import Optional
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DOTENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(DOTENV_PATH)

API_KEY: Optional[str] = os.environ.get("API_KEY", None)