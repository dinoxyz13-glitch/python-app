import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AIライティングツール", page_icon="✍️", layout="wide")

st.title("✍️ AIライティングツール")
st.write("個人用のAI文章作成アシスタントです。左のメニューから機能を選んでください。")

st.markdown(
    """
- **記事テーマ作成** — 日常や経験から、note有料記事の「売れるテーマ」を掘り起こす
- **ブログ記事執筆** — テーマとキーワードから記事を生成
- **ストーリー作成** — テーマから、人の心に響く感動ストーリーを作成（300字〜5,000字以上）
- **メール返信作成** — 受信メールから返信文を生成
- **文章要約** — 長文を要約
- **文章校正/リライト** — トーン調整や誤字脱字の修正
"""
)

if not os.getenv("GEMINI_API_KEY"):
    st.warning(
        "GEMINI_API_KEY が設定されていません。プロジェクト直下に `.env` ファイルを作成し、"
        "`GEMINI_API_KEY=あなたのAPIキー` を記入してください（`.env.example` を参考にしてください）。"
    )
else:
    st.success("Gemini API キーが読み込まれています。")

if os.getenv("ANTHROPIC_API_KEY"):
    st.success("Claude API キーが読み込まれています。")
else:
    st.info(
        "ANTHROPIC_API_KEY は未設定です。ブログ記事執筆で Claude を使う場合は、"
        "`.env` に `ANTHROPIC_API_KEY=あなたのAPIキー` を追記してください。"
    )
