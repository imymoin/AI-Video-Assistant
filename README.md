# 🎬 AI Video Assistant

> Transform any YouTube video or local recording into structured insights — summary, action items, key decisions, and an interactive chat powered by RAG.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sbnkmyb9tbpccnzcbchvr7.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Whisper](https://img.shields.io/badge/Whisper-OpenAI-orange)
![Mistral](https://img.shields.io/badge/LLM-Mistral%20AI-blueviolet)
![LangChain](https://img.shields.io/badge/LangChain-LCEL-green)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-red)

---

## ✨ Features

- 🎵 **YouTube & Local File Support** — paste any YouTube URL or local video/audio path
- 🎙️ **Local Transcription** — powered by OpenAI Whisper (runs fully offline)
- 🌐 **Hindi → English Translation** — automatic translation via Deep Translator
- ✦ **AI Summary** — concise summary of the entire video
- ✅ **Action Items** — extracted tasks and next steps
- 🔑 **Key Decisions** — important decisions made during the video
- ❓ **Open Questions** — unresolved questions identified from the content
- 💬 **RAG Chat** — ask anything about the video using a retrieval-augmented chatbot

---

## 🧠 Tech Stack

| Layer | Technology |
|---|---|
| Transcription | OpenAI Whisper |
| Translation | Deep Translator (Google) |
| LLM | Mistral AI (`mistral-small-2603`) |
| Orchestration | LangChain LCEL |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Vector Store | ChromaDB |
| Audio Processing | yt-dlp, pydub, FFmpeg |
| UI | Streamlit |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12
- FFmpeg installed on your system
- Mistral AI API key → [console.mistral.ai](https://console.mistral.ai)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/imymoin/AI-Video-Assistant.git
cd AI-Video-Assistant

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Add your MISTRAL_API_KEY to .env
```

### Environment Variables

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

### Run Locally

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📁 Project Structure

```
AI-Video-Assistant/
│
├── app.py                  # Streamlit UI
├── main.py                 # CLI entry point
├── requirements.txt
├── packages.txt            # System deps (FFmpeg for Streamlit Cloud)
├── runtime.txt             # Python 3.12 pin for Streamlit Cloud
├── .env                    # API keys (never commit this)
│
├── core/
│   ├── transcriber.py      # Whisper transcription
│   ├── summarize.py        # LLM summarization & title generation
│   ├── extractor.py        # Action items, decisions, questions
│   ├── rag_engine.py       # LangChain RAG chain (LCEL)
│   └── vector_store.py     # ChromaDB vector store + embeddings
│
└── utils/
    └── audio_processor.py  # yt-dlp download + pydub chunking
```

---

## 🖥️ Usage

**YouTube URL:**
```
https://youtube.com/watch?v=your_video_id
```

**Local file:**
```
C:/path/to/your/video.mp4
```

After processing you get:
1. A structured analysis (summary, action items, decisions, questions)
2. A live chat interface to ask questions about the video content

---

## ⚡ Pipeline

```
Input (URL / File)
       ↓
  yt-dlp / pydub         → Audio extraction & chunking
       ↓
  OpenAI Whisper          → Speech-to-text transcription
       ↓
  Deep Translator         → Hindi → English (if needed)
       ↓
  Mistral AI (LLM)        → Summary, action items, decisions, questions
       ↓
  ChromaDB + MiniLM       → Vector store for RAG
       ↓
  LangChain LCEL RAG      → Chat with your video
```

---

## ☁️ Deployed On

[Streamlit Cloud](https://streamlit.io/cloud) — free tier with Python 3.12 and FFmpeg support.

---

## 🙋 Author

**Yusuf** — M.Sc. AI/ML | Babasaheb Bhimrao Ambedkar University, Lucknow

[![GitHub](https://img.shields.io/badge/GitHub-imymoin-black?logo=github)](https://github.com/imymoin)

---

## 📄 License

MIT License — free to use, modify, and distribute.
