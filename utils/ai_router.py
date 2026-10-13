import os

from google.genai import errors as genai_errors

from utils import claude_client, gemini_client

GEMINI = "Gemini"
CLAUDE = "Claude（Opus 5.5）"
AI_NAMES = [GEMINI, CLAUDE]
FALLBACK_LABEL = "Gemini が混雑しているときは Claude で自動作成する（Claude の料金がかかります）"

_CHAT = {GEMINI: gemini_client.chat_with_status, CLAUDE: claude_client.chat_with_status}


def claude_available() -> bool:
    return bool(os.getenv("ANTHROPIC_API_KEY"))


def _gemini_busy(e: Exception) -> bool:
    """Gemini の混雑・一時的な不調・利用上限によるエラーかどうか。"""
    return isinstance(e, genai_errors.APIError) and (e.code == 429 or e.code >= 500)


def chat(ai_name: str, messages: list[dict], fallback_to_claude: bool = False) -> tuple[str, bool, str]:
    """選んだ AI で会話の続きを生成し、（文章, 途中で切れたか, 実際に使った AI）を返す。
    Gemini が混雑で失敗し、fallback_to_claude が True で Claude の API キーがあれば Claude で作り直す。"""
    try:
        text, truncated = _CHAT[ai_name](messages)
        return text, truncated, ai_name
    except Exception as e:
        if not (ai_name == GEMINI and fallback_to_claude and claude_available() and _gemini_busy(e)):
            raise
    text, truncated = _CHAT[CLAUDE](messages)
    return text, truncated, CLAUDE
