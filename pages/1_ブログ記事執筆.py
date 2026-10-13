import logging

import streamlit as st

from utils import claude_client, gemini_client
from utils.error_messages import describe_error, error_detail

logger = logging.getLogger(__name__)

st.set_page_config(page_title="ブログ記事執筆", page_icon="📝", layout="wide")
st.title("📝 ブログ記事執筆")

AI_OPTIONS = {
    "Gemini": gemini_client.generate_text_with_status,
    "Claude（Opus 5.5）": claude_client.generate_text_with_status,
}

with st.form("blog_form"):
    ai_name = st.radio("使用するAI", list(AI_OPTIONS), horizontal=True)
    topic = st.text_input("テーマ", placeholder="例: リモートワークの生産性を上げる方法")
    keywords = st.text_input("キーワード（カンマ区切り、任意）", placeholder="例: 集中力, ツール, 習慣")
    tone = st.selectbox("トーン", ["カジュアル", "フォーマル", "専門的", "親しみやすい"])
    col_age, col_gender = st.columns(2)
    with col_age:
        target_age = st.selectbox(
            "読者の年代", ["20〜30代", "30〜40代", "40〜50代", "50〜60代", "60〜80代"]
        )
    with col_gender:
        target_gender = st.selectbox(
            "読者の性別", ["男性向け", "女性向け", "男性女性とも"], index=2
        )
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
想定読者: {target_age}・{target_gender}

見出し（H2/H3相当）を使い、読みやすい構成にしてください。想定読者の年代・性別に合わせて、関心を持ちやすい話題や具体例、言葉づかいを選んでください。導入・本文・まとめの流れで書いてください。"""
        with st.spinner(f"{ai_name} で記事を生成中..."):
            try:
                result, truncated = AI_OPTIONS[ai_name](prompt)
                st.session_state["blog_result"] = result
                st.session_state["blog_truncated"] = truncated
                st.session_state["blog_ai"] = ai_name
            except (RuntimeError, claude_client.ClaudeRefusalError) as e:
                st.error(str(e))
            except Exception as e:
                logger.exception("ブログ記事の生成に失敗しました")
                st.error(f"{ai_name} で記事を生成できませんでした。{describe_error(e)}")
                st.caption(f"エラーの詳細: {error_detail(e)}")

if "blog_result" in st.session_state:
    st.markdown("### 生成結果")
    st.caption(
        f"使用AI: {st.session_state.get('blog_ai', 'Gemini')}　"
        f"文字数: {len(st.session_state['blog_result']):,}字"
    )
    if st.session_state.get("blog_truncated"):
        st.warning("出力の上限に達したため、記事が途中で切れています。")
    st.markdown(st.session_state["blog_result"])
    st.text_area("コピー用テキスト", st.session_state["blog_result"], height=300)
