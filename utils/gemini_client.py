import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL_NAME = "gemini-3.6-flash"


@st.cache_resource
def get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY が設定されていません。.env ファイルに設定してください。"
        )
    return genai.Client(api_key=api_key)


def generate_text(prompt: str, temperature: float = 0.7) -> str:
    client = get_client()
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={"temperature": temperature},
    )
    return response.text
