import logging

import streamlit as st

from utils.gemini_client import generate_text

logger = logging.getLogger(__name__)

st.set_page_config(page_title="文章要約", page_icon="📄", layout="wide")
st.title("📄 文章要約")

with st.form("summary_form"):
    source_text = st.text_area("要約したい文章", height=300, placeholder="要約対象の文章を貼り付けてください")
    length = st.selectbox("要約の長さ", ["一言（1文）", "短め（3〜5文）", "箇条書き（5項目程度）", "標準（元の1/3程度）"])
    submitted = st.form_submit_button("要約する", use_container_width=True)

if submitted:
    if not source_text.strip():
        st.error("文章を入力してください。")
    else:
        prompt = f"""以下の日本語の文章を要約してください。

【要約の形式】
{length}

【文章】
{source_text}"""
        with st.spinner("要約中..."):
            try:
                result = generate_text(prompt)
                st.session_state["summary_result"] = result
            except Exception:
                logger.exception("文章の要約に失敗しました")
                st.error("エラーが発生しました。しばらくしてから再度お試しください。")

if "summary_result" in st.session_state:
    st.markdown("### 要約結果")
    st.markdown(st.session_state["summary_result"])
    st.text_area("コピー用テキスト", st.session_state["summary_result"], height=200)
