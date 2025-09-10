import streamlit as st
from pypdf import PdfReader
import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load API key
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Streamlit UI
st.title("📄 Ask Questions About Your PDF (GPT-4o via OpenRouter)")
st.write("Upload a PDF and ask questions powered by GPT-4o.")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Upload PDF
uploaded_file = st.file_uploader(
    "📎 Upload your PDF (Max 5MB)", 
    type="pdf", 
    help="Only PDF files under 5MB are allowed. Drag & drop or click to select."
)


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

if uploaded_file and uploaded_file.size > MAX_FILE_SIZE:
    st.error("❌ File size exceeds 5MB limit. Please upload a smaller PDF.")
    uploaded_file = None


if uploaded_file:
    # Extract text
    pdf_reader = PdfReader(uploaded_file)
    pdf_text = ""
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            pdf_text += text

    st.success("✅ PDF uploaded and text extracted!")

    with st.expander("📄 View Extracted PDF Text"):
        st.text(pdf_text[:1000] + "...")

    # Ask question
    question = st.text_input("❓ Ask a question about the PDF:")

    if question:
        # Prepare request
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://yourdomain.com",
            "X-Title": "PDF GPT Assistant",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openai/gpt-3.5-turbo",  # ✅ usually free
            "messages": [
                {
                    "role": "user",
                    "content": f"PDF Content:\n{pdf_text}\n\nQuestion: {question}"
                }
            ]
        }

        with st.spinner("🧠 Thinking..."):
            try:
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    data=json.dumps(payload)
                )
                response.raise_for_status()
                result = response.json()
                answer = result["choices"][0]["message"]["content"]

                # Show response
                st.subheader("📝 Answer:")
                st.write(answer)

                # Save to session chat history
                st.session_state.chat_history.append({
                    "question": question,
                    "answer": answer,
                    "time": datetime.now().strftime("%H:%M:%S")
                })

                # Save to local file
                today = datetime.today().strftime("%Y-%m-%d")
                filename = f"chat_{today}.json"
                with open(filename, "a", encoding="utf-8") as f:
                    json.dump({
                        "time": datetime.now().isoformat(),
                        "question": question,
                        "answer": answer
                    }, f)
                    f.write("\n")  # newline for each entry

            except Exception as e:
                st.error(f"❌ Error: {e}")

    # Show chat history
    if st.session_state.chat_history:
        st.markdown("## 💬 Chat History")
        for i, qa in enumerate(st.session_state.chat_history[::-1], 1):
            st.markdown(f"**Q{i}:** {qa['question']}")
            st.markdown(f"**A{i}:** {qa['answer']}")
            st.markdown("---")
