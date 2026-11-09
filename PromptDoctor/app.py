import streamlit as st
import requests
import json
import re
import time
import uuid
from datetime import datetime
from pathlib import Path

# ============================================================
# PROMPT DOCTOR — keyless MVP
# ============================================================
APP_TITLE = "Prompt Doctor"
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "qwen2.5:3b"
HISTORY_FILE = Path("prompt_doctor_history.json")

st.set_page_config(
    page_title="Prompt Doctor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------- THEME ----------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

theme = st.session_state.theme
if theme == "Dark":
    BG = "#0b1020"
    PANEL = "#121a2b"
    PANEL2 = "#172238"
    TEXT = "#edf2ff"
    MUTED = "#a8b3c7"
    BORDER = "#26344d"
    ACCENT = "#7c9cff"
    USER_BG = "#1b2a46"
else:
    BG = "#f4f7fb"
    PANEL = "#ffffff"
    PANEL2 = "#eef3fa"
    TEXT = "#172033"
    MUTED = "#5d6b82"
    BORDER = "#dbe3ef"
    ACCENT = "#365fce"
    USER_BG = "#e8efff"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

    .stApp {{
        background:
            radial-gradient(ellipse at 12% 0%, rgba(92, 108, 255, .14), transparent 38%),
            radial-gradient(ellipse at 90% 12%, rgba(0, 198, 170, .09), transparent 32%),
            {BG};
        color: {TEXT};
        font-family: 'DM Sans', sans-serif;
    }}
    [data-testid="stHeader"] {{ background: transparent; }}
    [data-testid="stSidebar"] {{
        background: {PANEL};
        border-right: 1px solid {BORDER};
    }}
    h1, h2, h3, p, label, span {{ color: {TEXT}; }}
    .hero {{
        position: relative;
        overflow: hidden;
        padding: 30px 32px;
        border: 1px solid {BORDER};
        border-radius: 24px;
        background: linear-gradient(120deg, {PANEL}, {PANEL2});
        box-shadow: 0 14px 40px rgba(0,0,0,.12);
        margin-bottom: 24px;
    }}
    .hero:after {{
        content: "✦";
        position: absolute;
        right: 34px;
        top: 8px;
        font-size: 100px;
        opacity: .10;
        color: {ACCENT};
    }}
    .hero-title {{
        font-size: clamp(28px, 4vw, 40px);
        font-weight: 800;
        letter-spacing: -1.2px;
        line-height: 1.15;
    }}
    .hero-sub {{ color: {MUTED}; margin-top: 10px; font-size: 1.02rem; }}
    .panel {{
        background: {PANEL};
        border: 1px solid {BORDER};
        border-radius: 18px;
        padding: 18px 20px;
        margin: 12px 0;
        box-shadow: 0 8px 24px rgba(0,0,0,.07);
    }}
    .chat-user {{
        background: {USER_BG};
        border: 1px solid {BORDER};
        border-radius: 18px 18px 5px 18px;
        padding: 15px 18px;
        margin: 12px 0 16px 10%;
    }}
    .chat-assistant {{
        background: {PANEL};
        border: 1px solid {BORDER};
        border-radius: 18px 18px 18px 5px;
        padding: 15px 18px;
        margin: 12px 10% 16px 0;
        box-shadow: 0 6px 20px rgba(0,0,0,.06);
    }}
    .small-muted {{ color: {MUTED}; font-size: .88rem; }}
    div.stButton > button {{
        border-radius: 12px;
        min-height: 44px;
        font-weight: 700;
        border: 1px solid {BORDER};
        transition: all .18s ease;
    }}
    div.stButton > button:hover {{
        border-color: {ACCENT};
        transform: translateY(-1px);
    }}
    div.stButton > button[kind="primary"] {{
        background: linear-gradient(100deg, {ACCENT}, #6b83e8);
        color: white;
        border: 0;
    }}
    textarea, input {{
        border-radius: 12px !important;
    }}
    [data-testid="stMetric"] {{
        background: {PANEL};
        border: 1px solid {BORDER};
        padding: 16px;
        border-radius: 16px;
    }}
    [data-testid="stProgressBar"] > div > div {{
        background: linear-gradient(90deg, {ACCENT}, #26c6a5);
    }}
    .stTabs [data-baseweb="tab"] {{ color: {TEXT}; }}
    hr {{ border-color: {BORDER}; margin: 22px 0; }}
    [data-testid="stFileUploader"] {{
        border: 1px dashed {BORDER};
        border-radius: 14px;
        padding: 8px;
        background: {PANEL};
    }}
    section[data-testid="stSidebar"] .stButton > button {{
        border-radius: 11px;
    }}
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1180px;
    }}
</style>
""", unsafe_allow_html=True)


# --------------------- LOCAL HISTORY -----------------------
def load_history():
    if HISTORY_FILE.exists():
        try:
            data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except Exception:
            return []
    return []

def save_history():
    try:
        HISTORY_FILE.write_text(
            json.dumps(st.session_state.conversations, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    except Exception as exc:
        st.warning(f"Could not save local chat history: {exc}")

if "conversations" not in st.session_state:
    st.session_state.conversations = load_history()
if "active_chat" not in st.session_state:
    st.session_state.active_chat = None
if "pending" not in st.session_state:
    st.session_state.pending = None


def new_chat():
    chat = {
        "id": str(uuid.uuid4()),
        "title": "New conversation",
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "messages": []
    }
    st.session_state.conversations.insert(0, chat)
    st.session_state.active_chat = chat["id"]
    st.session_state.pending = None
    save_history()


def get_active_chat():
    for chat in st.session_state.conversations:
        if chat["id"] == st.session_state.active_chat:
            return chat
    return None


if not st.session_state.conversations:
    new_chat()
elif st.session_state.active_chat is None:
    st.session_state.active_chat = st.session_state.conversations[0]["id"]


# ---------------------- FILE READING -----------------------
def read_uploaded_files(files):
    extracted = []
    attachment_names = []
    visual_names = []

    for uploaded in files or []:
        name = uploaded.name
        attachment_names.append(name)
        suffix = Path(name).suffix.lower()

        try:
            if suffix in [".txt", ".md", ".csv", ".json", ".py", ".html", ".xml"]:
                raw = uploaded.getvalue().decode("utf-8", errors="ignore")
                extracted.append(f"\n--- FILE: {name} ---\n{raw[:12000]}\n")
            elif suffix == ".pdf":
                try:
                    from pypdf import PdfReader
                    import io
                    reader = PdfReader(io.BytesIO(uploaded.getvalue()))
                    pages = []
                    for page in reader.pages[:20]:
                        pages.append(page.extract_text() or "")
                    extracted.append(
                        f"\n--- PDF: {name} ---\n" +
                        "\n".join(pages)[:16000] + "\n"
                    )
                except ImportError:
                    extracted.append(
                        f"\n[PDF attached: {name}. Install pypdf to extract its text.]"
                    )
            elif suffix in [".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".mov", ".avi", ".mkv"]:
                visual_names.append(name)
            else:
                extracted.append(
                    f"\n[File attached: {name}. This file type is not text-extracted.]"
                )
        except Exception as exc:
            extracted.append(f"\n[Could not read {name}: {exc}]")

    return "\n".join(extracted), attachment_names, visual_names


# ------------------------ AI CALL --------------------------
def ask_ai(system_message, user_message):
    """Send a chat request to the locally running Ollama model."""
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180
        )
        response.raise_for_status()
        data = response.json()
        answer = data.get("message", {}).get("content", "").strip()

        if not answer:
            raise RuntimeError("Ollama returned an empty response.")
        return answer

    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Cannot connect to Ollama. Make sure Ollama is running, "
            "then try again. Ollama should be available at http://localhost:11434."
        ) from exc
    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            "Ollama took too long to respond. Please try again; "
            "the first response can take longer while the model loads."
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Ollama request failed: {exc}") from exc
    except (ValueError, KeyError, TypeError) as exc:
        raise RuntimeError(f"Could not read Ollama's response: {exc}") from exc


# ------------------ PROMPT DIAGNOSIS -----------------------
def diagnose_prompt(prompt):
    checks = {
        "Clear task": bool(re.search(
            r"\b(write|create|explain|分析|summari[sz]e|compare|solve|design|build|分析|generate|review|analy[sz]e|teach|plan|translate|debug|code|draft|prepare)\b",
            prompt, re.I
        )),
        "Role or perspective": bool(re.search(
            r"\b(as a|act as|you are|role|expert|teacher|developer|editor|analyst|consultant|examiner)\b",
            prompt, re.I
        )),
        "Context": len(prompt.split()) >= 18 or bool(re.search(
            r"\b(context|background|for my|audience|student|business|project|subject|level)\b",
            prompt, re.I
        )),
        "Constraints": bool(re.search(
            r"\b(must|should|avoid|include|exclude|limit|within|under|at least|maximum|minimum|tone|style)\b",
            prompt, re.I
        )),
        "Output format": bool(re.search(
            r"\b(format|table|bullet|list|steps|paragraph|json|report|outline|headings|word count|markdown)\b",
            prompt, re.I
        ))
    }
    score = round(sum(checks.values()) / len(checks) * 100)
    return score, checks


def fallback_options(prompt):
    base = prompt.strip()
    return [
        {
            "title": "Clear and structured",
            "reason": "Improves clarity, context, and the expected structure.",
            "prompt": (
                "Act as a knowledgeable subject-matter expert. Complete this task clearly and accurately. "
                "State any assumptions, organize the response with useful headings, and give concrete examples "
                "where helpful. If important information is missing, ask concise clarifying questions.\n\n"
                f"Task:\n{base}"
            )
        },
        {
            "title": "Detailed expert approach",
            "reason": "Encourages deeper reasoning, careful coverage, and useful detail.",
            "prompt": (
                "Act as a senior expert in the relevant field. First identify the goal, audience, and constraints. "
                "Address the task comprehensively, explain important decisions, check for gaps or errors, "
                "and finish with a concise summary and practical next steps.\n\n"
                f"Task:\n{base}"
            )
        },
        {
            "title": "Concise, outcome-focused",
            "reason": "Prioritizes a direct, practical answer without unnecessary filler.",
            "prompt": (
                "Complete the task below with a direct, useful, well-organized answer. Prioritize correctness "
                "and actionable information. Use concise headings or bullets where they improve readability. "
                "Avoid repetition and clearly flag uncertainty.\n\n"
                f"Task:\n{base}"
            )
        }
    ]


def parse_options(raw, original_prompt):
    # Accept either pure JSON or JSON surrounded by markdown fences/text.
    candidate = raw.strip()
    candidate = re.sub(r"^```(?:json)?\s*", "", candidate, flags=re.I)
    candidate = re.sub(r"\s*```$", "", candidate)
    try:
        data = json.loads(candidate)
    except Exception:
        match = re.search(r"\{.*\}", candidate, flags=re.S)
        if not match:
            return fallback_options(original_prompt)
        try:
            data = json.loads(match.group(0))
        except Exception:
            return fallback_options(original_prompt)

    options = data.get("options", data) if isinstance(data, dict) else data
    if not isinstance(options, list):
        return fallback_options(original_prompt)

    cleaned = []
    for item in options[:3]:
        if isinstance(item, dict) and item.get("prompt"):
            cleaned.append({
                "title": str(item.get("title", "Optimized prompt"))[:80],
                "reason": str(item.get("reason", "A refined version of your request."))[:300],
                "prompt": str(item["prompt"])
            })
    return cleaned if len(cleaned) >= 2 else fallback_options(original_prompt)


def generate_options(prompt, file_context):
    system = (
        "You are Prompt Doctor, an expert prompt engineer. Diagnose the user's request and create "
        "exactly three distinct, high-quality prompt alternatives. Preserve the user's actual goal. "
        "Do not answer the task. Return ONLY valid JSON in this schema: "
        '{"options":[{"title":"...","reason":"...","prompt":"..."},'
        '{"title":"...","reason":"...","prompt":"..."},'
        '{"title":"...","reason":"...","prompt":"..."}]}'
    )
    user = "Original request:\n" + prompt
    if file_context:
        user += "\n\nExtracted text from attached files:\n" + file_context[:18000]
    raw = ask_ai(system, user)
    return parse_options(raw, prompt)


# ---------------------- SIDEBAR ----------------------------
with st.sidebar:
    st.markdown("## 🩺 Prompt Doctor")
    st.caption("Your prompt improvement workspace")

    st.markdown("### Appearance")
    chosen_theme = st.radio(
        "Choose theme",
        ["Dark", "Light"],
        index=0 if st.session_state.theme == "Dark" else 1,
        horizontal=True,
        label_visibility="collapsed"
    )
    if chosen_theme != st.session_state.theme:
        st.session_state.theme = chosen_theme
        st.rerun()

    st.divider()
    if st.button("＋  New chat", use_container_width=True, type="primary"):
        new_chat()
        st.rerun()

    st.markdown("### Chat history")
    if st.session_state.conversations:
        chat_labels = {
            c["id"]: f'{c["title"]}  ·  {c["created"]}'
            for c in st.session_state.conversations
        }
        ids = list(chat_labels.keys())
        current_index = ids.index(st.session_state.active_chat) if st.session_state.active_chat in ids else 0
        selected_id = st.selectbox(
            "Your conversations",
            ids,
            index=current_index,
            format_func=lambda x: chat_labels.get(x, "Conversation"),
            label_visibility="collapsed"
        )
        if selected_id != st.session_state.active_chat:
            st.session_state.active_chat = selected_id
            st.session_state.pending = None
            st.rerun()

    if st.button("Clear current chat", use_container_width=True):
        chat = get_active_chat()
        if chat:
            chat["messages"] = []
            chat["title"] = "New conversation"
        st.session_state.pending = None
        save_history()
        st.rerun()

    st.divider()
    st.markdown("### About this MVP")
    st.caption(
        "AI replies are generated locally using Ollama and the Qwen model. "
        "No API key or account is required. Chat history is stored locally "
        "in prompt_doctor_history.json."
    )


# ------------------------- MAIN ----------------------------
st.markdown("""
<div class="hero">
  <div class="hero-title">🩺 Prompt Doctor</div>
  <div class="hero-sub">Your AI prompt studio · Diagnose, refine, and get better answers.</div>
</div>
""", unsafe_allow_html=True)

step_a, step_b, step_c = st.columns(3)
with step_a:
    st.markdown("**① Diagnose**")
    st.caption("Check prompt quality")
with step_b:
    st.markdown("**② Refine**")
    st.caption("Choose from 3 improved prompts")
with step_c:
    st.markdown("**③ Execute**")
    st.caption("Get an answer from local AI")

chat = get_active_chat()
if chat is None:
    new_chat()
    chat = get_active_chat()

# Conversation transcript
for message in chat["messages"]:
    if message["role"] == "user":
        st.markdown(
            f'<div class="chat-user"><b>You</b><br>{message["content"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="chat-assistant"><b>Prompt Doctor</b><br>{message["content"]}</div>',
            unsafe_allow_html=True
        )

# Prompt quality snapshot
st.markdown("### ✍️ Start with your request")
st.caption("Write naturally. Prompt Doctor will evaluate it and suggest three improved versions.")

with st.form("prompt_form", clear_on_submit=False):
    user_prompt = st.text_area(
        "Your prompt",
        placeholder="Example: Create a 7-day study plan for my university biology exam. I have 2 hours per day...",
        height=135,
        key="main_prompt_input"
    )
    uploaded_files = st.file_uploader(
        "Add files (optional)",
        type=[
            "txt", "md", "csv", "json", "py", "html", "xml",
            "pdf", "png", "jpg", "jpeg", "webp", "gif",
            "mp4", "mov", "avi", "mkv"
        ],
        accept_multiple_files=True,
        help="Text files and PDFs can be read. Images/videos can be attached but are not visually analyzed by this keyless text model."
    )
    submit_prompt = st.form_submit_button("✦  Diagnose & improve prompt", type="primary", use_container_width=True)

if submit_prompt:
    if not user_prompt.strip():
        st.warning("Please enter a prompt first.")
    else:
        file_context, attachment_names, visual_names = read_uploaded_files(uploaded_files)
        score, checks = diagnose_prompt(user_prompt)
        chat = get_active_chat()
        chat["title"] = user_prompt.strip().replace("\n", " ")[:42] or "New conversation"
        user_display = user_prompt.strip()
        if attachment_names:
            user_display += "\n\nAttachments: " + ", ".join(attachment_names)
        chat["messages"].append({"role": "user", "content": user_display})
        save_history()

        st.session_state.pending = {
            "id": str(uuid.uuid4()),
            "original": user_prompt.strip(),
            "file_context": file_context,
            "attachment_names": attachment_names,
            "visual_names": visual_names,
            "score": score,
            "checks": checks,
            "options": None,
            "error": None
        }

        with st.spinner("Reviewing your prompt and preparing alternatives..."):
            try:
                st.session_state.pending["options"] = generate_options(
                    user_prompt.strip(), file_context
                )
            except Exception as exc:
                st.session_state.pending["options"] = fallback_options(user_prompt.strip())
                st.session_state.pending["error"] = str(exc)
        save_history()
        st.rerun()


# ------------------ OPTIMIZATION WORKSPACE -----------------
pending = st.session_state.pending
if pending:
    st.divider()
    st.markdown("## 📊 Prompt health report")

    metric_col, info_col = st.columns([1, 2])
    with metric_col:
        st.metric("Prompt score", f'{pending["score"]}/100')
        st.progress(pending["score"] / 100)
    with info_col:
        st.markdown("**Prompt checklist**")
        cols = st.columns(5)
        for col, (label, passed) in zip(cols, pending["checks"].items()):
            with col:
                st.markdown(("✅ " if passed else "➕ ") + label)

    if pending["error"]:
        st.info(
            "Ollama could not generate the alternatives, so these were created "
            "using the built-in prompt optimizer. Check that Ollama is running "
            "and try again when ready."
        )

    if pending["visual_names"]:
        st.warning(
            "Image/video files attached: " + ", ".join(pending["visual_names"]) +
            ". They are listed here but this text-only AI connection cannot interpret their visual content."
        )

    st.markdown("## ✨ Choose your improved prompt")
    options = pending["options"] or fallback_options(pending["original"])
    option_titles = [f'{i+1}. {o["title"]}' for i, o in enumerate(options)]
    selection_key = "choice_" + pending["id"]
   

    selected_title = st.radio(
        "Prompt alternatives",
        option_titles,
        key=selection_key,
        horizontal=False
    )
    selected_index = option_titles.index(selected_title)
    selected_option = options[selected_index]
    edit_key = f'edit_{pending["id"]}_{selected_index}'


    st.markdown(f'<div class="panel"><b>{selected_option["title"]}</b><br><span class="small-muted">{selected_option["reason"]}</span></div>', unsafe_allow_html=True)

    edited_prompt = st.text_area(
        "Edit the selected prompt before running it",
        value=selected_option["prompt"],
        height=220,
        key=edit_key
    )

    run_col, reset_col = st.columns([3, 1])
    with run_col:
        execute = st.button("➤  Execute selected prompt", type="primary", use_container_width=True)
    with reset_col:
        if st.button("Discard", use_container_width=True):
            st.session_state.pending = None
            st.rerun()

    if execute:
        if not edited_prompt.strip():
            st.warning("The selected prompt is empty. Please edit it first.")
        else:
            with st.spinner("Generating your answer..."):
                try:
                    answer = ask_ai(
                        "You are a helpful, accurate assistant. Follow the user's prompt carefully. "
                        "Use clear formatting. Be honest about uncertainty and do not invent facts.",
                        edited_prompt.strip()
                    )
                    chat = get_active_chat()
                    chat["messages"].append({
                        "role": "assistant",
                        "content": answer
                    })
                    save_history()
                    st.session_state.pending = None
                    st.success("Answer generated.")
                    st.rerun()
                except Exception as exc:
                    st.error(str(exc))
                    st.caption(
                        "Your optimized prompt is still in the editor above. "
                        "You can copy it and retry later; no chat history has been lost."
                    )

# ----------------------- FOOTER ----------------------------
st.divider()
st.caption(
    "Prompt Doctor · Local AI powered by Ollama and Qwen · "
    "No API key or account required · Chat history stays on this computer"
)
