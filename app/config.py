import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PROJECT_NAME = "Africa TTS API"
    VERSION = "1.0.0"
    API_PREFIX = "/api"
    
    # Gradio Space Configuration
    GRADIO_SPACE = os.getenv("GRADIO_SPACE", "Ghana-NLP/Africa-TTS-UI")
    
    # Optional Rate Limiting
    RATE_LIMIT = os.getenv("RATE_LIMIT", "100/minute")

settings = Config()
