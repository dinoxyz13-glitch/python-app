import anthropic
from google.genai import errors as genai_errors


def describe_error(e: Exception) -> str:
    """API のエラーを、原因と対処がわかる日本語のメッセージにする。"""
    if isinstance(e, anthropic.AuthenticationError):
        return "Claude の API キーが正しくありません。.env の ANTHROPIC_API_KEY を確認してください。"
    if isinstance(e, anthropic.PermissionDeniedError):
        return "Claude の API キーにこの操作の権限がありません。Claude Console でキーの設定を確認してください。"
    if isinstance(e, anthropic.BadRequestError) and "credit balance" in str(e).lower():
        return "Claude API のクレジット残高が不足しています。Claude Console の Billing でクレジットを購入してください。"
    if isinstance(e, anthropic.RateLimitError):
        return "Claude API の利用回数の上限に達しました。少し時間をおいてから再度お試しください。"
    if isinstance(e, anthropic.APIConnectionError):
        return "Claude API に接続できませんでした。インターネット接続を確認してください。"
    if isinstance(e, anthropic.APIStatusError) and e.status_code >= 500:
        return "Claude API が混み合っているか、一時的に不調です。少し時間をおいてから再度お試しください。"

    if isinstance(e, genai_errors.APIError):
        if e.code in (401, 403) or (e.code == 400 and "api key" in str(e.message).lower()):
            return "Gemini の API キーが正しくありません。.env の GEMINI_API_KEY を確認してください。"
        if e.code == 429:
            return "Gemini API の利用回数の上限に達しました。少し時間をおいてから再度お試しください。"
        if e.code >= 500:
            return (
                "Gemini API が混み合っているか、一時的に不調です（自動で数回やり直しましたが失敗しました）。"
                "少し時間をおいてから再度お試しいただくか、「Claude」に切り替えてお試しください。"
            )

    return "予期しないエラーが発生しました。"


def error_detail(e: Exception) -> str:
    """原因調査用に、エラーの種類と内容を短くまとめる（API キーは含まれない）。"""
    detail = f"{type(e).__name__}: {e}"
    return detail if len(detail) <= 500 else detail[:500] + "…"
