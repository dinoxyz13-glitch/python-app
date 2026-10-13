import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

load_dotenv()

MODEL_NAME = "gemini-3.6-flash"
# 1回の生成で出力できる最大トークン数（日本語はおおよそ1文字≒1トークン）。
# 20,000字程度の長文と、モデル内部の思考分を合わせても足りるよう大きめに設定。
MAX_OUTPUT_TOKENS = 65536


@st.cache_resource
def get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY が設定されていません。.env ファイルに設定してください。"
        )
    # Gemini が混雑（503）などで一時的に失敗したときは、間隔をあけて自動で再試行する
    retry = types.HttpRetryOptions(
        attempts=4, initial_delay=2, max_delay=30, http_status_codes=[429, 500, 502, 503, 504]
    )
    return genai.Client(api_key=api_key, http_options=types.HttpOptions(retry_options=retry))


def chat_with_status(messages: list[dict], temperature: float = 0.7) -> tuple[str, bool]:
    """会話（{"role": "user" | "assistant", "content": 文章} のリスト）の続きを生成し、
    生成した文章と、出力上限に達して途中で切れたかどうかを返す。"""
    client = get_client()
    contents = [
        types.Content(
            role="user" if m["role"] == "user" else "model", parts=[types.Part(text=m["content"])]
        )
        for m in messages
    ]
    config = {"temperature": temperature, "max_output_tokens": MAX_OUTPUT_TOKENS}
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=contents, config=config)
    except errors.ClientError as e:
        # 上限値がモデルの許容範囲を超えている場合は、上限を指定せずにやり直す（モデルの初期値が使われる）
        if e.code != 400 or "maxoutputtokens" not in str(e).lower().replace("_", ""):
            raise
        del config["max_output_tokens"]
        response = client.models.generate_content(model=MODEL_NAME, contents=contents, config=config)
    truncated = bool(response.candidates) and (
        response.candidates[0].finish_reason == types.FinishReason.MAX_TOKENS
    )
    return response.text or "", truncated


def generate_text_with_status(prompt: str, temperature: float = 0.7) -> tuple[str, bool]:
    """生成した文章と、出力上限に達して途中で切れたかどうかを返す。"""
    return chat_with_status([{"role": "user", "content": prompt}], temperature)


def generate_text(prompt: str, temperature: float = 0.7) -> str:
    text, _ = generate_text_with_status(prompt, temperature)
    return text
