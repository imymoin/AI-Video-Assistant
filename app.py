import streamlit as st
from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
  font-family: 'Inter', sans-serif;
  background: #060810 !important;
  color: #e2e8f0;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2.5rem 4rem !important; max-width: 1200px !important; }

/* ── Animated gradient background ── */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 20% -10%, rgba(99,102,241,0.18) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 110%, rgba(168,85,247,0.14) 0%, transparent 60%),
    radial-gradient(ellipse 40% 30% at 60% 30%, rgba(59,130,246,0.08) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}

/* ── Hero section ── */
.hero {
  padding: 4.5rem 0 3rem;
  position: relative;
}
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: rgba(99,102,241,0.12);
  border: 1px solid rgba(99,102,241,0.3);
  border-radius: 100px;
  padding: 5px 14px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  font-weight: 500;
  color: #a5b4fc;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 1.4rem;
}
.hero-badge::before {
  content: '';
  width: 6px; height: 6px;
  background: #6366f1;
  border-radius: 50%;
  box-shadow: 0 0 8px #6366f1;
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; box-shadow: 0 0 8px #6366f1; }
  50% { opacity: 0.5; box-shadow: 0 0 16px #6366f1; }
}
.hero-title {
  font-family: 'Syne', sans-serif;
  font-size: clamp(2.4rem, 5vw, 3.8rem);
  font-weight: 800;
  line-height: 1.08;
  letter-spacing: -0.02em;
  color: #f8fafc;
  margin-bottom: 1rem;
}
.hero-title .accent {
  background: linear-gradient(135deg, #818cf8 0%, #a78bfa 50%, #60a5fa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-sub {
  font-size: 1rem;
  color: #64748b;
  line-height: 1.65;
  max-width: 520px;
}

/* ── Input card ── */
.input-shell {
  background: rgba(15,17,28,0.7);
  border: 1px solid rgba(99,102,241,0.2);
  border-radius: 16px;
  padding: 28px 28px 24px;
  backdrop-filter: blur(20px);
  margin-bottom: 2.5rem;
  box-shadow: 0 0 0 1px rgba(255,255,255,0.03), 0 24px 48px rgba(0,0,0,0.4);
}
.input-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  font-weight: 500;
  color: #6366f1;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin-bottom: 10px;
}

/* ── Streamlit widget overrides ── */
.stTextInput > div > div > input {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 10px !important;
  color: #e2e8f0 !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.875rem !important;
  padding: 14px 18px !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input::placeholder { color: #334155 !important; }
.stTextInput > div > div > input:focus {
  border-color: rgba(99,102,241,0.6) !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.12), 0 0 20px rgba(99,102,241,0.08) !important;
  background: rgba(99,102,241,0.05) !important;
}
.stTextInput > label { display: none !important; }

/* Buttons */
.stButton > button {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
  color: #fff !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.875rem !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 14px 24px !important;
  letter-spacing: 0.02em !important;
  box-shadow: 0 4px 20px rgba(99,102,241,0.35) !important;
  transition: all 0.2s !important;
  white-space: nowrap !important;
}
.stButton > button:hover {
  box-shadow: 0 6px 28px rgba(99,102,241,0.55) !important;
  transform: translateY(-1px) !important;
  filter: brightness(1.1) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Stats bar ── */
.stats-bar {
  display: flex;
  gap: 24px;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}
.stat-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 8px;
  padding: 8px 14px;
  font-size: 0.8rem;
  color: #94a3b8;
}
.stat-pill strong { color: #e2e8f0; font-weight: 600; }

/* ── Section heading ── */
.section-heading {
  font-family: 'Syne', sans-serif;
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: #475569;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.section-heading::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(to right, rgba(71,85,105,0.4), transparent);
}

/* ── Result cards ── */
.r-card {
  background: rgba(15,17,28,0.6);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 14px;
  padding: 22px 22px 20px;
  margin-bottom: 16px;
  backdrop-filter: blur(12px);
  box-shadow: 0 1px 0 rgba(255,255,255,0.04) inset, 0 16px 40px rgba(0,0,0,0.25);
  transition: border-color 0.2s, box-shadow 0.2s;
  height: 100%;
}
.r-card:hover {
  border-color: rgba(99,102,241,0.25);
  box-shadow: 0 1px 0 rgba(255,255,255,0.04) inset, 0 16px 40px rgba(0,0,0,0.25), 0 0 0 1px rgba(99,102,241,0.1);
}
.r-card-icon {
  font-size: 1.4rem;
  margin-bottom: 10px;
  display: block;
}
.r-card-title {
  font-family: 'Syne', sans-serif;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #6366f1;
  margin-bottom: 12px;
}
.r-card-body {
  font-size: 0.875rem;
  color: #94a3b8;
  line-height: 1.7;
  white-space: pre-wrap;
}

/* Wide card (full width) */
.r-card-wide {
  background: rgba(15,17,28,0.6);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 14px;
  padding: 22px 24px 20px;
  margin-bottom: 16px;
  backdrop-filter: blur(12px);
  box-shadow: 0 1px 0 rgba(255,255,255,0.04) inset, 0 16px 40px rgba(0,0,0,0.25);
}

/* ── Video title banner ── */
.video-banner {
  background: linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(139,92,246,0.08) 100%);
  border: 1px solid rgba(99,102,241,0.25);
  border-radius: 14px;
  padding: 20px 24px;
  margin-bottom: 24px;
  display: flex;
  align-items: flex-start;
  gap: 16px;
}
.video-banner-icon {
  font-size: 2rem;
  flex-shrink: 0;
  line-height: 1;
  margin-top: 2px;
}
.video-banner-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: #6366f1;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin-bottom: 4px;
}
.video-banner-title {
  font-family: 'Syne', sans-serif;
  font-size: 1.35rem;
  font-weight: 700;
  color: #f1f5f9;
  line-height: 1.3;
}

/* ── Chat ── */
.chat-wrap {
  background: rgba(15,17,28,0.6);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 16px 48px rgba(0,0,0,0.3);
}
.chat-header {
  background: rgba(99,102,241,0.08);
  border-bottom: 1px solid rgba(255,255,255,0.06);
  padding: 14px 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.chat-header-dot {
  width: 8px; height: 8px;
  background: #6366f1;
  border-radius: 50%;
  box-shadow: 0 0 10px #6366f1;
  animation: pulse 2s infinite;
}
.chat-header-text {
  font-family: 'Syne', sans-serif;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #a5b4fc;
}
.chat-messages {
  padding: 20px;
  min-height: 280px;
  max-height: 420px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.chat-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #334155;
  font-size: 0.85rem;
  gap: 8px;
}
.chat-empty-icon { font-size: 2rem; }
.msg-row-user { display: flex; justify-content: flex-end; }
.msg-row-bot  { display: flex; justify-content: flex-start; align-items: flex-end; gap: 8px; }
.bot-avatar {
  width: 28px; height: 28px; flex-shrink: 0;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem;
}
.bubble-user {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: #fff;
  padding: 10px 16px;
  border-radius: 18px 18px 4px 18px;
  font-size: 0.875rem;
  max-width: 72%;
  font-weight: 500;
  line-height: 1.5;
  box-shadow: 0 4px 16px rgba(99,102,241,0.3);
}
.bubble-bot {
  background: rgba(30,38,56,0.9);
  border: 1px solid rgba(255,255,255,0.07);
  color: #cbd5e1;
  padding: 10px 16px;
  border-radius: 18px 18px 18px 4px;
  font-size: 0.875rem;
  max-width: 72%;
  line-height: 1.6;
}
.chat-input-area {
  border-top: 1px solid rgba(255,255,255,0.06);
  padding: 14px 16px;
  background: rgba(8,10,18,0.5);
}

/* ── Expander ── */
.streamlit-expanderHeader {
  background: rgba(255,255,255,0.02) !important;
  border: 1px solid rgba(255,255,255,0.07) !important;
  border-radius: 10px !important;
  color: #475569 !important;
  font-size: 0.8rem !important;
}

/* ── Alerts ── */
.stAlert { border-radius: 10px !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #6366f1 !important; }

/* ── Divider ── */
.fancy-divider {
  height: 1px;
  background: linear-gradient(to right, transparent, rgba(99,102,241,0.3), transparent);
  margin: 2.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for key, default in [("result", None), ("chat_history", [])]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Pipeline ──────────────────────────────────────────────────────────────────
def run_pipeline(src: str) -> dict:
    chunks = process_input(src)
    transcript = transcribe_all(chunks)
    title = generate_title(transcript)
    summary_text = summarize(transcript)
    action_items = extract_action_items(transcript)
    decisions = extract_key_decisions(transcript)
    questions = extract_questions(transcript)
    rag_chain = build_rag_chain(transcript)
    return {
        "title": title,
        "transcript": transcript,
        "summary": summary_text,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
    }

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">✦ Powered by Whisper + Mistral AI</div>
  <h1 class="hero-title">Turn any video into<br><span class="accent">actionable intelligence.</span></h1>
  <p class="hero-sub">Paste a YouTube URL or local file path. Get an instant summary, action items, key decisions — and chat with your video.</p>
</div>
""", unsafe_allow_html=True)

# ── Input shell ───────────────────────────────────────────────────────────────
st.markdown('<div class="input-shell"><div class="input-label">⌘ Video source</div>', unsafe_allow_html=True)

col_in, col_btn = st.columns([5, 1], gap="small")
with col_in:
    source = st.text_input(
        "source",
        placeholder="https://youtube.com/watch?v=...   or   C:/path/to/video.mp4",
        label_visibility="collapsed",
    )
with col_btn:
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    run_clicked = st.button("Analyse →", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Trigger pipeline ──────────────────────────────────────────────────────────
if run_clicked and source.strip():
    st.session_state.chat_history = []
    st.session_state.result = None

    prog_placeholder = st.empty()
    steps = [
        ("🎵", "Downloading & extracting audio…"),
        ("🎙️", "Transcribing with Whisper…"),
        ("✨", "Summarising & extracting insights…"),
        ("🔗", "Building RAG knowledge base…"),
    ]

    with st.spinner(""):
        prog_placeholder.markdown(f"""
        <div style="background:rgba(15,17,28,0.8);border:1px solid rgba(99,102,241,0.2);
        border-radius:12px;padding:20px 24px;margin-bottom:16px;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;
          color:#6366f1;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:14px;">
            Processing pipeline
          </div>
          {''.join(f'<div style="display:flex;align-items:center;gap:10px;padding:6px 0;color:#94a3b8;font-size:0.85rem;"><span>{icon}</span><span>{label}</span></div>' for icon, label in steps)}
        </div>
        """, unsafe_allow_html=True)
        try:
            st.session_state.result = run_pipeline(source.strip())
            prog_placeholder.empty()
        except Exception as e:
            prog_placeholder.empty()
            st.error(f"**Pipeline error:** {e}")

elif run_clicked and not source.strip():
    st.warning("Please enter a YouTube URL or file path.")

# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.result:
    res = st.session_state.result
    word_count = len(res["transcript"].split())
    char_count = len(res["transcript"])

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # Video title banner
    st.markdown(f"""
    <div class="video-banner">
      <div class="video-banner-icon">🎬</div>
      <div>
        <div class="video-banner-label">Analysed video</div>
        <div class="video-banner-title">{res['title']}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats pills
    st.markdown(f"""
    <div class="stats-bar">
      <div class="stat-pill">📝 <strong>{word_count:,}</strong>&nbsp;words transcribed</div>
      <div class="stat-pill">💬 <strong>{len(res['summary'].split()):,}</strong>&nbsp;word summary</div>
      <div class="stat-pill">🤖 <strong>RAG</strong>&nbsp;chat ready</div>
    </div>
    """, unsafe_allow_html=True)

    # ── 3-column insight cards ──
    st.markdown('<div class="section-heading">Extracted insights</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.markdown(f"""
        <div class="r-card">
          <span class="r-card-icon">✦</span>
          <div class="r-card-title">Summary</div>
          <div class="r-card-body">{res['summary']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="r-card">
          <span class="r-card-icon">✅</span>
          <div class="r-card-title">Action Items</div>
          <div class="r-card-body">{res['action_items']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="r-card">
          <span class="r-card-icon">🔑</span>
          <div class="r-card-title">Key Decisions</div>
          <div class="r-card-body">{res['key_decisions']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Open questions — full width
    st.markdown(f"""
    <div class="r-card-wide">
      <span style="font-size:1.3rem;display:block;margin-bottom:10px;">❓</span>
      <div class="r-card-title">Open Questions</div>
      <div class="r-card-body">{res['open_questions']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Transcript
    with st.expander("📄  Raw transcript"):
        st.code(res["transcript"], language=None)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # ── Chat ──────────────────────────────────────────────────────────────────
    # Build messages HTML
    if st.session_state.chat_history:
        msgs_html = ""
        for turn in st.session_state.chat_history:
            msgs_html += f'<div class="msg-row-user"><div class="bubble-user">{turn["user"]}</div></div>'
            msgs_html += f'<div class="msg-row-bot"><div class="bot-avatar">🤖</div><div class="bubble-bot">{turn["bot"]}</div></div>'
    else:
        msgs_html = """
        <div class="chat-empty">
          <div class="chat-empty-icon">💬</div>
          <div>Ask anything about the video</div>
        </div>
        """

    st.markdown(f"""
    <div class="chat-wrap">
      <div class="chat-header">
        <div class="chat-header-dot"></div>
        <div class="chat-header-text">Chat with your video</div>
      </div>
      <div class="chat-messages">{msgs_html}</div>
    </div>
    """, unsafe_allow_html=True)

    # Chat input row (outside the HTML div — Streamlit widgets)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    c_in, c_btn = st.columns([5, 1], gap="small")
    with c_in:
        user_q = st.text_input(
            "q",
            placeholder="Ask a question about the video…",
            key="chat_input",
            label_visibility="collapsed",
        )
    with c_btn:
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        send = st.button("Send →", use_container_width=True, key="send_btn")

    if send and user_q.strip():
        with st.spinner("Thinking…"):
            answer = ask_question(res["rag_chain"], user_q.strip())
        st.session_state.chat_history.append({"user": user_q.strip(), "bot": answer})
        st.rerun()