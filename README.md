# ✍️ AIライティングツール

Gemini API を利用した個人用の AI 文章作成アシスタントです。Streamlit で動作します。

## 機能

- **ブログ記事執筆** — テーマとキーワードから記事を生成
- **メール返信作成** — 受信メールから返信文を生成
- **文章要約** — 長文を要約
- **文章校正/リライト** — トーン調整や誤字脱字の修正

## セットアップ

### 1. リポジトリを取得

```bash
git clone https://github.com/dinoxyz13-glitch/python-app.git
cd python-app
```

### 2. 依存パッケージをインストール

```bash
pip install -r requirements.txt
```

### 3. APIキーを設定

[Google AI Studio](https://aistudio.google.com/apikey) で Gemini API キーを取得し、
`.env.example` をコピーして `.env` を作成、キーを記入してください。

```bash
cp .env.example .env
```

```
GEMINI_API_KEY=あなたのAPIキー
```

`.env` は `.gitignore` で除外されているため、コミットされることはありません。
**APIキーは絶対に公開リポジトリにコミットしないでください。**

### 4. アプリを起動

```bash
streamlit run app.py
```

ブラウザで `http://localhost:8501` が開きます。左のメニューから機能を選んでください。

## 技術スタック

- [Streamlit](https://streamlit.io/) — UI
- [google-genai](https://pypi.org/project/google-genai/) — Gemini API クライアント
- [python-dotenv](https://pypi.org/project/python-dotenv/) — `.env` 読み込み

## ライセンス

個人利用を目的としたプロジェクトです。
