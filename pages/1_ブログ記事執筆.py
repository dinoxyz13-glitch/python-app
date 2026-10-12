import logging

import streamlit as st

from utils.gemini_client import generate_text_with_status

logger = logging.getLogger(__name__)

st.set_page_config(page_title="ブログ記事執筆", page_icon="📝", layout="wide")
st.title("📝 ブログ記事執筆")

with st.form("blog_form"):
    topic = st.text_input("テーマ", placeholder="例: リモートワークの生産性を上げる方法")
    keywords = st.text_input("キーワード（カンマ区切り、任意）", placeholder="例: 集中力, ツール, 習慣")
    tone = st.selectbox("トーン", ["カジュアル", "フォーマル", "専門的", "親しみやすい"])
    length = st.selectbox(
        "文章量",
        [
            "短め（300〜500字）",
            "標準（800〜1200字）",
            "長め（1500字以上）",
            "長文（5,000〜10,000字）",
            "超長文（10,000〜20,000字）",
        ],
    )
    submitted = st.form_submit_button("記事を生成する", use_container_width=True)

if submitted:
    if not topic.strip():
        st.error("テーマを入力してください。")
    else:
        prompt = f"""あなたはプロのブログライターです。以下の条件で日本語のブログ記事を書いてください。

テーマ: {topic}
キーワード: {keywords if keywords.strip() else "指定なし"}
トーン: {tone}
文章量: {length}

見出し（H2/H3相当）を使い、読みやすい構成にしてください。導入・本文・まとめの流れで書いてください。"""
        with st.spinner("記事を生成中..."):
            try:
                result, truncated = generate_text_with_status(prompt)
                st.session_state["blog_result"] = result
                st.session_state["blog_truncated"] = truncated
            except Exception:
                logger.exception("ブログ記事の生成に失敗しました")
                st.error("エラーが発生しました。しばらくしてから再度お試しください。")

if "blog_result" in st.session_state:
    st.markdown("### 生成結果")
    st.caption(f"文字数: {len(st.session_state['blog_result']):,}字")
    if st.session_state.get("blog_truncated"):
        st.warning("出力の上限に達したため、記事が途中で切れています。")
    st.markdown(st.session_state["blog_result"])
    st.text_area("コピー用テキスト", st.session_state["blog_result"], height=300)
