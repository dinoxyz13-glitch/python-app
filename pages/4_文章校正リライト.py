import logging

import streamlit as st

from utils.gemini_client import generate_text

logger = logging.getLogger(__name__)

st.set_page_config(page_title="文章校正/リライト", page_icon="🪄", layout="wide")
st.title("🪄 文章校正・リライト")

with st.form("proofread_form"):
    source_text = st.text_area("校正・リライトしたい文章", height=300, placeholder="対象の文章を貼り付けてください")
    mode = st.selectbox(
        "モード",
        ["誤字脱字・文法チェックのみ", "自然な文章にリライト", "トーンを変更してリライト"],
    )
    tone = None
    if mode == "トーンを変更してリライト":
        tone = st.selectbox("変更後のトーン", ["フォーマル", "カジュアル", "丁寧", "簡潔", "情熱的"])
    submitted = st.form_submit_button("実行する", use_container_width=True)

if submitted:
    if not source_text.strip():
        st.error("文章を入力してください。")
    else:
        if mode == "誤字脱字・文法チェックのみ":
            instruction = "誤字脱字・文法の誤りのみを修正してください。文体や表現は基本的に変えないでください。修正箇所がわかるように、修正後の文章の後に修正点の一覧も付けてください。"
        elif mode == "自然な文章にリライト":
            instruction = "より自然で読みやすい文章にリライトしてください。"
        else:
            instruction = f"文章のトーンを「{tone}」に変更してリライトしてください。"

        prompt = f"""以下の日本語の文章について、次の指示に従って修正してください。

【指示】
{instruction}

【文章】
{source_text}"""
        with st.spinner("処理中..."):
            try:
                result = generate_text(prompt)
                st.session_state["proofread_result"] = result
            except Exception:
                logger.exception("文章の校正・リライトに失敗しました")
                st.error("エラーが発生しました。しばらくしてから再度お試しください。")

if "proofread_result" in st.session_state:
    st.markdown("### 結果")
    st.markdown(st.session_state["proofread_result"])
    st.text_area("コピー用テキスト", st.session_state["proofread_result"], height=250)
