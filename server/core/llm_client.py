from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)

print(os.environ.get("GEMINI_API_KEY"))
client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
