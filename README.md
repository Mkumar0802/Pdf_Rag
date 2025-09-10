📄 PDF Q&A (Streamlit + OpenRouter)

Ask natural-language questions about a PDF with a simple Streamlit UI.
It extracts text with pypdf and sends it to an LLM via OpenRouter (default: openai/gpt-3.5-turbo).

✨ Features

Upload a PDF (≤5MB) and ask questions interactively

Streamlit web UI

Chat history saved per session (also logged to chat_YYYY-MM-DD.json)

Environment-based config with .env

🚀 Quickstart
1. Clone & enter
git clone <your-repo-url>.git
cd pdf-qa-app

2. Virtual environment (recommended)
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

3. Install dependencies
pip install -r requirements.txt

4. Add API key

Create a file named .env:

OPENROUTER_API_KEY=your_openrouter_api_key_here

5. Run the app
streamlit run app.py


Open the link (usually http://localhost:8501
).

🧪 Usage

Upload a PDF (max 5MB).

Type your question.

Get an answer from GPT-3.5 via OpenRouter.

See chat history and saved logs.

🔧 Configuration

API key is set in .env.

Default model: openai/gpt-3.5-turbo.

Change it in app.py → payload["model"].

🧯 Troubleshooting

401 Unauthorized → Check OPENROUTER_API_KEY.

413 Payload Too Large → PDF text too long; use smaller files.

429 Rate Limit → Slow requests or upgrade plan.

No answers → Inspect logs with st.write(response.json()).

📦 Deploy

Local: streamlit run app.py

Streamlit Community Cloud: push to GitHub, add OPENROUTER_API_KEY in secrets.

Docker: see docs for example Dockerfile.

📜 License

MIT – free to use, modify, and share.
