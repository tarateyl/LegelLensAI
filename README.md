# LegalLensAI
# 🧾 LegalLens AI

LegalLens AI is a Streamlit-powered GenAI tool that helps users — especially non-experts — understand complex contracts using natural language summaries, AI insights, and a retrieval-augmented glossary of legal terms.

## ✨ Features
- 🔍 Upload contracts (PDF or TXT)
- 💬 Plain English summaries tailored to your age/context
- 🧩 "What If" scenario generator
- 🚨 Red Flag Radar to spot risky clauses
- 📄 Clause-by-Clause breakdown
- ❓ Ask any follow-up legal question
- 📚 RAG-powered glossary (including Spain-specific clauses)
- 🎙️ Optional podcast-style summary (via gTTS)

## 🧠 Tech Stack
- **Streamlit** – UI and UX
- **Gemini 1.5 Flash** – LLM from Google
- **FAISS** + `sentence-transformers` – RAG support
- **PyMuPDF** – PDF parsing
- **gTTS** – Text-to-speech (optional)

## 🛠️ Setup & Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/legallens-ai.git
cd legallens-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
>>>>>>> d01812c (initial commit)
