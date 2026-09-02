import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AIライティングツール", page_icon="✍️", layout="wide")

st.title("✍️ AIライティングツール")
st.write("個人用のAI文章作成アシスタントです。左のメニューから機能を選んでください。")

st.markdown(
    """
- **ブログ記事執筆** — テーマとキーワードから記事を生成
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
