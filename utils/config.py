import yaml
import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

def get_config(path: str = "config.yaml") -> dict:
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config

# Access API keys anywhere like:
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")