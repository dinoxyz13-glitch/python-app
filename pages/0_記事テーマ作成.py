import json
import logging
from pathlib import Path

import streamlit as st

from utils import claude_client, gemini_client
from utils.error_messages import describe_error, error_detail
from utils.note_theme_prompt import PROFILE_FIELDS, build_prompt

logger = logging.getLogger(__name__)

# 「私のこと」の入力内容はこのPCだけに保存する（.gitignore で GitHub には上げない）
PROFILE_PATH = Path(__file__).resolve().parent.parent / "data" / "note_profile.json"

AI_OPTIONS = {
    "Gemini": gemini_client.chat_with_status,
    "Claude（Opus 5.5）": claude_client.chat_with_status,
}
MORE_IDEAS_REQUEST = "ピンとこないので、別の角度からもう7案出してください。"

st.set_page_config(page_title="記事テーマ作成", page_icon="💡", layout="wide")
st.title("💡 記事テーマ作成")
st.write("note有料記事の「売れるテーマ」を、あなたの日常や経験から掘り起こします。")


def load_profile() -> dict:
    try:
        return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_profile(profile: dict) -> None:
    PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROFILE_PATH.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")


def ask_ai(messages: list[dict]) -> bool:
    """会話の続きを AI に依頼する。成功したら返答を加えた会話を保存して True を返す。"""
    ai_name = st.session_state["theme_ai"]
    history = [{"role": m["role"], "content": m["content"]} for m in messages]
    with st.spinner(f"{ai_name} が考えています..."):
        try:
            text, truncated = AI_OPTIONS[ai_name](history)
        except (RuntimeError, claude_client.ClaudeRefusalError) as e:
            st.error(str(e))
            return False
        except Exception as e:
            logger.exception("記事テーマの作成に失敗しました")
            st.error(f"{ai_name} で回答を作成できませんでした。{describe_error(e)}")
            st.caption(f"エラーの詳細: {error_detail(e)}")
            return False
    st.session_state["theme_messages"] = messages + [
        {"role": "assistant", "content": text, "truncated": truncated}
    ]
    return True


saved = load_profile()
with st.form("theme_form"):
    ai_name = st.radio("使用するAI", list(AI_OPTIONS), horizontal=True)
    st.markdown("**私のこと**（入力内容はこのPCに保存され、次回も表示されます）")
    profile = {
        key: st.text_area(label, value=saved.get(key, ""), placeholder=example, height=80)
        for key, label, example in PROFILE_FIELDS
    }
    submitted = st.form_submit_button("テーマを提案してもらう", use_container_width=True)

if submitted:
    if not any(v.strip() for v in profile.values()):
        st.error("「私のこと」を1つ以上入力してください。")
    else:
        save_profile(profile)
        st.session_state["theme_ai"] = ai_name
        ask_ai([{"role": "user", "content": build_prompt(profile)}])

messages = st.session_state.get("theme_messages", [])
if messages:
    st.markdown("### 編集者とのやりとり")
    st.caption(f"使用AI: {st.session_state['theme_ai']}")
    with st.expander("最初に送ったプロンプトを見る"):
        st.text(messages[0]["content"])
    for m in messages[1:]:
        with st.chat_message("assistant" if m["role"] == "assistant" else "user"):
            st.markdown(m["content"])
            if m.get("truncated"):
                st.warning("出力の上限に達したため、回答が途中で切れています。")

    col_more, col_reset = st.columns(2)
    more = col_more.button("別の角度からもう7案", use_container_width=True)
    if col_reset.button("やりとりをリセット", use_container_width=True):
        del st.session_state["theme_messages"]
        st.rerun()

    reply = st.chat_input("質問への回答や、追加の依頼を入力（例: 3番のテーマのターゲットをもっと絞って）")
    request = MORE_IDEAS_REQUEST if more else reply
    if request and ask_ai(messages + [{"role": "user", "content": request}]):
        st.rerun()
