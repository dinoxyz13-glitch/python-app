import logging

import streamlit as st

from utils import ai_router, claude_client
from utils.error_messages import describe_error, error_detail
from utils.options import READER_AGES, TONES

logger = logging.getLogger(__name__)

st.set_page_config(page_title="ストーリー作成", page_icon="📖", layout="wide")
st.title("📖 ストーリー作成")
st.write("人の心に響く感動ストーリーを作成します。")

with st.form("story_form"):
    ai_name = st.radio("使用するAI", ai_router.AI_NAMES, horizontal=True)
    fallback = st.checkbox(ai_router.FALLBACK_LABEL, value=True)
    theme = st.text_input("ストーリーのテーマ", placeholder="例: 20年通い続けたサウナで、ようやく水風呂に入れた日")
    details = st.text_area(
        "盛り込みたい要素・エピソード（任意）",
        placeholder="例: 主人公は40代の会社員。きっかけは常連のおじいさんのひと言。",
        height=100,
    )
    keywords = st.text_input("キーワード（カンマ区切り、任意）", placeholder="例: サウナ, 水風呂, 挑戦")
    col_tone, col_age = st.columns(2)
    with col_tone:
        tone = st.selectbox("トーン", TONES)
    with col_age:
        target_age = st.selectbox("読者の年代", READER_AGES)
    length = st.selectbox(
        "文章量", ["300〜500字", "500〜1,000字", "1,000〜2,000字", "5,000字以上"]
    )
    submitted = st.form_submit_button("ストーリーを作成する", use_container_width=True)

if submitted:
    if not theme.strip():
        st.error("ストーリーのテーマを入力してください。")
    else:
        prompt = f"""＃あなたは世界最高の感動物語を語る「ストーリーテラー」です

＃人間の琴線に触れるストーリーを作成することができます

＃文字数は「{length}」

＃ストーリーのテーマ：{theme}

＃盛り込みたい要素・エピソード：{details.strip() if details.strip() else "指定なし"}

＃キーワード：{keywords.strip() if keywords.strip() else "指定なし"}

＃トーン：{tone}

＃想定読者の年代：{target_age}（この年代の読者が共感しやすい登場人物・場面・言葉づかいにしてください）

上記の条件で、日本語のストーリーを1つ作成してください。"""
        with st.spinner(f"{ai_name} でストーリーを作成中..."):
            try:
                result, truncated, used_ai = ai_router.chat(
                    ai_name, [{"role": "user", "content": prompt}], fallback
                )
                st.session_state["story_result"] = result
                st.session_state["story_truncated"] = truncated
                st.session_state["story_ai"] = used_ai
                if used_ai != ai_name:
                    st.info("Gemini が混雑していたため、Claude で作成しました。")
            except (RuntimeError, claude_client.ClaudeRefusalError) as e:
                st.error(str(e))
            except Exception as e:
                logger.exception("ストーリーの作成に失敗しました")
                st.error(f"{ai_name} でストーリーを作成できませんでした。{describe_error(e)}")
                st.caption(f"エラーの詳細: {error_detail(e)}")

if "story_result" in st.session_state:
    st.markdown("### 作成結果")
    st.caption(
        f"使用AI: {st.session_state['story_ai']}　"
        f"文字数: {len(st.session_state['story_result']):,}字"
    )
    if st.session_state.get("story_truncated"):
        st.warning("出力の上限に達したため、ストーリーが途中で切れています。")
    st.markdown(st.session_state["story_result"])
    st.text_area("コピー用テキスト", st.session_state["story_result"], height=250)
