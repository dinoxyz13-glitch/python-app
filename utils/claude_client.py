import os

import anthropic
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "claude-opus-5-5"
# 1回の生成で出力できる最大トークン数。20,000字程度の長文と、モデル内部の思考分を合わせても足りる量。
# 大きな値はストリーミングで受け取る必要があるため、generate_text_with_status ではストリーミングを使う。
MAX_TOKENS = 64000
# 安全上の理由で応答が断られた場合に、Anthropic 推奨の別モデルで自動的にやり直す設定
FALLBACK_BETA = "server-side-fallback-2026-07-01"


class ClaudeRefusalError(Exception):
    """Claude が安全上の理由で生成を断った場合のエラー。"""


@st.cache_resource
def get_client() -> anthropic.Anthropic:
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise RuntimeError(
            "ANTHROPIC_API_KEY が設定されていません。.env ファイルに設定してください。"
        )
    return anthropic.Anthropic()


def chat_with_status(messages: list[dict]) -> tuple[str, bool]:
    """会話（{"role": "user" | "assistant", "content": 文章} のリスト）の続きを生成し、
    生成した文章と、出力上限に達して途中で切れたかどうかを返す。"""
    client = get_client()
    with client.beta.messages.stream(
        model=MODEL_NAME,
        max_tokens=MAX_TOKENS,
        output_config={"effort": "high"},
        betas=[FALLBACK_BETA],
        fallbacks="default",
        messages=messages,
    ) as stream:
        message = stream.get_final_message()
    if message.stop_reason == "refusal":
        raise ClaudeRefusalError("Claude がこの内容の生成を断りました。")
    text = "".join(block.text for block in message.content if block.type == "text")
    return text, message.stop_reason == "max_tokens"


def generate_text_with_status(prompt: str) -> tuple[str, bool]:
    """生成した文章と、出力上限に達して途中で切れたかどうかを返す。"""
    return chat_with_status([{"role": "user", "content": prompt}])
