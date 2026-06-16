# hybrid_RAG\services\embedding\embeddings.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

AZURE_OPENAI_EMB_ENDPOINT = os.getenv("AZURE_OPENAI_EMB_ENDPOINT")
AZURE_OPENAI_EMB_API_KEY = os.getenv("AZURE_OPENAI_EMB_API_KEY")
AZURE_OPENAI_EMB_API_VERSION = os.getenv("AZURE_OPENAI_EMB_API_VERSION")
AZURE_OPENAI_EMB_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMB_DEPLOYMENT")


def get_embedding(text):
    url = f"{AZURE_OPENAI_EMB_ENDPOINT}/openai/deployments/{AZURE_OPENAI_EMB_DEPLOYMENT}/embeddings?api-version={AZURE_OPENAI_EMB_API_VERSION}"

    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_EMB_API_KEY
    }

    payload = {
        "input": text
    }

    response = requests.post(url, headers=headers, json=payload, verify=False)

    if response.status_code != 200:
        raise Exception(f"Embedding API Error: {response.text}")

    return response.json()["data"][0]["embedding"]