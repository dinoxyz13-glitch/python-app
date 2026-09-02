import logging

import streamlit as st

from utils.gemini_client import generate_text

logger = logging.getLogger(__name__)

st.set_page_config(page_title="メール返信作成", page_icon="📧", layout="wide")
st.title("📧 メール返信作成")

with st.form("email_form"):
    original_mail = st.text_area("受信したメール本文", height=200, placeholder="受け取ったメールの内容を貼り付けてください")
    intent = st.text_area("返信の要点（任意）", placeholder="例: 来週の火曜なら対応可能、金額は再検討してほしいと伝える")
    tone = st.selectbox("トーン", ["丁寧なビジネス文", "カジュアル", "フォーマル", "簡潔"])
    submitted = st.form_submit_button("返信文を生成する", use_container_width=True)

if submitted:
    if not original_mail.strip():
        st.error("受信したメール本文を入力してください。")
    else:
        prompt = f"""あなたは優秀なビジネスアシスタントです。以下の受信メールに対する日本語の返信メールを作成してください。

【受信メール】
{original_mail}

【返信で伝えたい要点】
{intent if intent.strip() else "特に指定なし。内容に沿って適切に返信してください。"}

【トーン】
{tone}

件名と本文を含む、そのまま送信できる形式で出力してください。"""
        with st.spinner("返信文を生成中..."):
            try:
                result = generate_text(prompt)
                st.session_state["email_result"] = result
            except Exception:
                logger.exception("返信メールの生成に失敗しました")
                st.error("エラーが発生しました。しばらくしてから再度お試しください。")

if "email_result" in st.session_state:
    st.markdown("### 生成結果")
    st.markdown(st.session_state["email_result"])
    st.text_area("コピー用テキスト", st.session_state["email_result"], height=250)
