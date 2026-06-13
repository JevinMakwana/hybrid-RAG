# proj-grag\GRAG_V3\services\llm\llm_client.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.getenv("AZURE_OPENAI_GPT4OMINI_ENDPOINT")
DEPLOYMENT = os.getenv("AZURE_OPENAI_GPT4OMINI_DEPLOYMENT")
API_KEY = os.getenv("AZURE_OPENAI_GPT4OMINI_API_KEY")
API_VERSION = os.getenv("AZURE_OPENAI_GPT4OMINI_API_VERSION")


def call_llm(system_prompt, user_prompt, temperature=0):
    url = f"{ENDPOINT}/openai/deployments/{DEPLOYMENT}/chat/completions?api-version={API_VERSION}"

    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }

    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature
    }

    response = requests.post(url, headers=headers, json=payload, verify=False)

    if response.status_code != 200:
        raise Exception(f"LLM API Error: {response.text}")

    return response.json()["choices"][0]["message"]["content"]