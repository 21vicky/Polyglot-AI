
import html
import streamlit as st
from detector import detect_language, languages


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Polyglot AI | Language Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# SESSION STATE
# =====================================================

DEFAULTS = {
    "history": [],
    "input_text": "",
    "latest_result": None,
    "latest_text": "",
    "theme": "Dark",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def reset_app():
    st.session_state.input_text = ""
    st.session_state.latest_result = None
    st.session_state.latest_text = ""

def is_heuristic(result):
    return (
        result.get("method", "").lower()
        == "tamil vocabulary heuristic"
    )


def score_label(result):
    if is_heuristic(result):
        return "Heuristic Match"
    return f"{result['confidence']:.2f}%"


def safe_text(value):
    return html.escape(str(value))


# =====================================================
# THEME
# =====================================================

dark_mode = st.session_state.theme == "Dark"

if dark_mode:
    C = {
        "bg": "#0B1020",
        "sidebar": "#10182A",
        "card": "#151F33",
        "input": "#10182A",
        "border": "#26334A",
        "text": "#F3F5FC",
        "muted": "#A0ABC0",
        "accent": "#9B8CFF",
        "accent2": "#6F5BEB",
        "hero": "#1A1B3D",
        "success": "#36D6A0",
        "surface": "#1B2940",
        "shadow": "rgba(0, 0, 0, .18)",
    }
else:
    C = {
        "bg": "#F6F7FC",
        "sidebar": "#FFFFFF",
        "card": "#FFFFFF",
        "input": "#FFFFFF",
        "border": "#E6E8F0",
        "text": "#182039",
        "muted": "#68738A",
        "accent": "#6657E8",
        "accent2": "#8B5CF6",
        "hero": "#EFEDFF",
        "success": "#059669",
        "surface": "#F8F9FD",
        "shadow": "rgba(35, 39, 75, .06)",
    }


# =====================================================
# CUSTOM STYLING
# =====================================================

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

    :root {{
        --bg: {C["bg"]};
        --sidebar: {C["sidebar"]};
        --card: {C["card"]};
        --input: {C["input"]};
        --border: {C["border"]};
        --text: {C["text"]};
        --muted: {C["muted"]};
        --accent: {C["accent"]};
        --accent2: {C["accent2"]};
        --shadow: {C["shadow"]};
    }}

    html, body, [class*="css"] {{
        font-family: 'DM Sans', sans-serif;
    }}

    .stApp {{
        background: var(--bg);
        color: var(--text);
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    .block-container {{
        max-width: 1260px;
        padding-top: 2rem;
        padding-bottom: 2.5rem;
    }}

    h1, h2, h3, h4, p, label, li {{
        color: var(--text);
    }}

    [data-testid="stCaptionContainer"] {{
        color: var(--muted);
    }}

    [data-testid="stSidebar"] {{
        background: var(--sidebar);
        border-right: 1px solid var(--border);
    }}

    [data-testid="stSidebar"] * {{
        color: var(--text);
    }}

    .brand {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 5px 0 16px;
    }}

    .brand-icon {{
        width: 46px;
        height: 46px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white !important;
        font-size: 24px;
        background: linear-gradient(135deg, #8B7BFF, #5D4BD6);
        box-shadow: 0 8px 20px rgba(111, 91, 235, .25);
    }}

    .brand-name {{
        color: var(--text);
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -.6px;
    }}

    .brand-name span {{
        color: var(--accent);
    }}

    .hero {{
        position: relative;
        overflow: hidden;
        padding: 36px;
        margin-bottom: 25px;
        border: 1px solid var(--border);
        border-radius: 23px;
        background: linear-gradient(120deg, {C["hero"]}, {C["card"]});
        box-shadow: 0 8px 28px var(--shadow);
    }}

    .hero-tag {{
        display: inline-block;
        padding: 7px 12px;
        margin-bottom: 15px;
        border-radius: 30px;
        background: {C["accent"]}22;
        color: var(--accent) !important;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
    }}

    .hero-title {{
        margin: 0;
        color: var(--text) !important;
        font-size: clamp(30px, 4vw, 42px);
        line-height: 1.15;
        font-weight: 800;
        letter-spacing: -1.3px;
    }}

    .hero-title span {{
        color: var(--accent) !important;
    }}

    .hero-subtitle {{
        max-width: 650px;
        margin: 12px 0 0;
        color: var(--muted) !important;
        font-size: 15px;
        line-height: 1.7;
    }}

    .section-heading {{
        margin: 25px 0 12px;
        color: var(--text);
        font-size: 19px;
        font-weight: 800;
        letter-spacing: -.3px;
    }}

    .metric-card {{
        min-height: 105px;
        padding: 19px;
        border: 1px solid var(--border);
        border-radius: 16px;
        background: var(--card);
        box-shadow: 0 5px 18px var(--shadow);
    }}

    .metric-value {{
        color: var(--accent) !important;
        font-size: 25px;
        font-weight: 800;
        line-height: 1.3;
        overflow-wrap: anywhere;
    }}

    .metric-label {{
        margin-top: 5px;
        color: var(--muted) !important;
        font-size: 12px;
        font-weight: 600;
    }}

    .stTextArea textarea {{
        color: var(--text) !important;
        background: var(--input) !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
        padding: 16px !important;
        font-size: 15px !important;
        line-height: 1.65 !important;
    }}

    .stTextArea textarea:focus {{
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px {C["accent"]}20 !important;
    }}

    .stTextArea textarea::placeholder {{
        color: var(--muted) !important;
    }}

    .stSelectbox div[data-baseweb="select"] > div {{
        color: var(--text);
        background: var(--card);
        border-color: var(--border);
        border-radius: 10px;
    }}

    .stButton > button,
    .stDownloadButton > button {{
        min-height: 44px;
        border: 1px solid var(--border);
        border-radius: 11px;
        font-weight: 700;
        transition: all .2s ease;
    }}

    .stButton > button[kind="primary"] {{
        color: #FFFFFF;
        border: none;
        background: linear-gradient(100deg, #7565F0, #6248D9);
        box-shadow: 0 7px 18px rgba(103, 83, 224, .22);
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover {{
        border-color: var(--accent);
        transform: translateY(-1px);
    }}

    .stButton > button[kind="primary"]:hover {{
        color: #FFFFFF;
        background: linear-gradient(100deg, #6655E4, #553CCB);
    }}

    .result-card {{
        padding: 25px;
        border: 1px solid var(--border);
        border-left: 4px solid var(--accent);
        border-radius: 17px;
        background: var(--card);
        box-shadow: 0 7px 24px var(--shadow);
    }}

    .result-eyebrow {{
        margin-bottom: 8px;
        color: var(--muted) !important;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.2px;
    }}

    .result-language {{
        margin: 0 0 12px;
        color: var(--accent) !important;
        font-size: 32px;
        font-weight: 800;
        overflow-wrap: anywhere;
    }}

    .result-detail {{
        margin: 5px 0;
        color: var(--muted) !important;
        font-size: 14px;
    }}

    .result-detail strong {{
        color: var(--text) !important;
    }}

    [data-testid="stExpander"] {{
        overflow: hidden;
        border: 1px solid var(--border);
        border-radius: 13px;
        background: var(--card);
    }}

    .stProgress > div > div > div {{
        background: linear-gradient(90deg, #7565F0, #A78BFA);
    }}

    hr {{
        border-color: var(--border);
    }}

    .footer {{
        padding: 25px 0 8px;
        color: var(--muted) !important;
        font-size: 12px;
        text-align: center;
        line-height: 1.8;
    }}

    @media (max-width: 640px) {{
        .hero {{
            padding: 25px 20px;
        }}
        .block-container {{
            padding-top: 1rem;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">🌍</div>
            <div class="brand-name">Polyglot<span> AI</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("LANGUAGE INTELLIGENCE PLATFORM")
    st.divider()

    st.markdown("### 🎨 Appearance")

    selected_theme = st.selectbox(
        "Choose your theme",
        ["Dark", "Light"],
        index=0 if dark_mode else 1,
        key="theme_selector",
    )

    if selected_theme != st.session_state.theme:
        st.session_state.theme = selected_theme
        st.rerun()

    st.divider()

    st.markdown("### 🤖 About Polyglot AI")
    st.write(
        "Identify the language behind written text using "
        "natural language processing and language detection."
    )

    st.divider()

    st.markdown("### 🛠️ Technologies")
    st.write("🐍 Python")
    st.write("🧠 Lingua NLP")
    st.write("🎈 Streamlit")

    st.divider()

    st.markdown("### 📊 Your Activity")

    total_detections = len(st.session_state.history)
    unique_languages = len({
        item.get("language", "Unknown")
        for item in st.session_state.history
    })

    stat1, stat2 = st.columns(2)
    stat1.metric("Detections", total_detections)
    stat2.metric("Languages", unique_languages)

    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.history = []
        st.session_state.latest_result = None
        st.session_state.latest_text = ""
        st.rerun()

    st.divider()
    st.caption("DAY 12 · 30 DAYS – 30 AI PROJECTS")


# =====================================================
# HERO
# =====================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-tag">✦ AI LANGUAGE INTELLIGENCE</div>
        <h1 class="hero-title">Every word has a language.<br>
        <span>Discover yours.</span></h1>
        <p class="hero-subtitle">
            Detect the language of any text in seconds.
            Explore multilingual writing with a clean, intelligent workspace.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# OVERVIEW METRICS
# =====================================================

overview = st.columns(3)

overview_data = [
    (str(len(languages)), "Selected detection languages"),
    ("AI + NLP", "Language detection technology"),
    ("Real-time", "Text analysis"),
]

for column, (value, label) in zip(overview, overview_data):
    with column:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =====================================================
# INPUT SECTION
# =====================================================

st.markdown(
    '<div class="section-heading">📝 Language Detection</div>',
    unsafe_allow_html=True,
)
st.caption("Choose a sample text or enter your own content.")

samples = {
    "English": "Hello, how are you today?",
    "Tamil": "நான் நன்றாக இருக்கிறேன்.",
    "Tanglish": "Vanakkam bro, eppadi iruka?",
    "Hindi": "नमस्ते, आप कैसे हैं?",
    "Telugu": "మీరు ఎలా ఉన్నారు?",
    "French": "Bonjour, comment allez-vous?",
    "Spanish": "Hola, ¿cómo estás?",
    "German": "Guten Morgen!",
}

sample_columns = st.columns(4)

for index, (language, sample) in enumerate(samples.items()):
    with sample_columns[index % 4]:
        if st.button(
            f"🌐 {language}",
            key=f"sample_{language}",
            use_container_width=True,
        ):
            st.session_state.input_text = sample
            st.rerun()


user_text = st.text_area(
    "Enter your text",
    key="input_text",
    placeholder="Type or paste a sentence, paragraph, or longer text here...",
    height=175,
)

word_count = len(user_text.split())
character_count = len(user_text)

info1, info2, info3 = st.columns([1, 1, 2])
info1.caption(f"📝 Words: **{word_count:,}**")
info2.caption(f"🔤 Characters: **{character_count:,}**")
info3.caption("🔒 Text is processed locally by the configured detection function.")


# =====================================================
# ACTIONS
# =====================================================

detect_col, reset_col = st.columns([3, 1])

with detect_col:
    detect_clicked = st.button(
        "🔍  Detect Language",
        type="primary",
        use_container_width=True,
    )

with reset_col:
    st.button(
        "↻ Reset",
        use_container_width=True,
        on_click=reset_app,
    )

# =====================================================
# DETECTION
# =====================================================

if detect_clicked:
    if not user_text.strip():
        st.warning("Please enter some text before detecting.")

    elif len(user_text.strip()) < 3:
        st.warning("Please enter at least a few characters for detection.")

    else:
        try:
            with st.spinner("🌍 Analyzing your text..."):
                result = detect_language(user_text)

            if not isinstance(result, dict):
                raise TypeError("The detector must return a dictionary.")

            required_fields = ("language", "code", "confidence")
            missing_fields = [
                field for field in required_fields
                if field not in result
            ]

            if missing_fields:
                raise ValueError(
                    "The detector returned an incomplete result. "
                    f"Missing fields: {', '.join(missing_fields)}"
                )

            confidence = float(result["confidence"])

            if not 0 <= confidence <= 100:
                raise ValueError(
                    "Detector confidence must be between 0 and 100."
                )

            normalized_result = {
                "language": str(result["language"]),
                "code": str(result["code"]),
                "confidence": confidence,
                "script": str(result.get("script", "Unknown")),
                "method": str(result.get("method", "Unknown")),
            }

            st.session_state.latest_result = normalized_result
            st.session_state.latest_text = user_text

            st.session_state.history.insert(
                0,
                {
                    "text": user_text,
                    **normalized_result,
                },
            )

            st.session_state.history = st.session_state.history[:50]

            st.success("Language detection completed!")

        except (ValueError, TypeError, AttributeError) as error:
            st.error(f"Detection failed: {error}")

        except Exception as error:
            st.error(
                "An unexpected error occurred during detection. "
                "Please try again."
            )
            st.exception(error)


# =====================================================
# RESULTS
# =====================================================

if st.session_state.latest_result is not None:
    result = st.session_state.latest_result

    st.divider()
    st.markdown(
        '<div class="section-heading">✨ Detection Results</div>',
        unsafe_allow_html=True,
    )

    language = safe_text(result["language"])
    code = safe_text(result["code"])
    script = safe_text(result["script"])
    method = safe_text(result["method"])
    confidence = float(result["confidence"])
    heuristic = is_heuristic(result)

    result_col, score_col = st.columns([1.7, 1])

    with result_col:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-eyebrow">DETECTED LANGUAGE</div>
                <div class="result-language">🌐 {language}</div>
                <p class="result-detail">
                    ISO language code: <strong>{code}</strong>
                </p>
                <p class="result-detail">
                    Writing system: <strong>{script}</strong>
                </p>
                <p class="result-detail">
                    Detection method: <strong>{method}</strong>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with score_col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    {"DETECTION TYPE" if heuristic else "DETECTION SCORE"}
                </div>
                <div class="metric-value">
                    {"Heuristic Match" if heuristic else f"{confidence:.2f}%"}
                </div>
                <div class="metric-label">
                    {"Rule-based vocabulary match" if heuristic else "Lingua engine score"}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if heuristic:
        st.info(
            "This is a Tanglish heuristic match based on recognized Tamil "
            "transliterated vocabulary. It is not an ML confidence score."
        )
    else:
        st.markdown("### 🎯 Detection Score")
        st.progress(max(0.0, min(1.0, confidence / 100)))
        st.caption(
            "This is the score reported by Lingua. It is not necessarily "
            "a calibrated probability or a guarantee of accuracy."
        )

    with st.expander("📄 View original input"):
        st.text(st.session_state.latest_text)

    download_confidence = (
        "Not applicable (heuristic match)"
        if heuristic
        else f"{confidence:.2f}%"
    )

    st.download_button(
        "⬇️ Download Detection Result",
        data=(
            f"Polyglot AI - Detection Result\n"
            f"Language: {result['language']}\n"
            f"Code: {result['code']}\n"
            f"Writing system: {result['script']}\n"
            f"Confidence: {download_confidence}\n"
            f"Method: {result['method']}\n\n"
            f"Original text:\n{st.session_state.latest_text}\n"
        ),
        file_name="Polyglot_AI_Detection.txt",
        mime="text/plain",
        use_container_width=True,
    )


# =====================================================
# DETECTION HISTORY
# =====================================================

st.divider()
st.markdown(
    '<div class="section-heading">📚 Detection History</div>',
    unsafe_allow_html=True,
)

if st.session_state.history:
    for index, item in enumerate(st.session_state.history):
        with st.expander(
            f"🌐 {item['language']} ({item['code']}) · "
            f"{score_label(item)}",
            expanded=(
                index == 0
                and st.session_state.latest_result is not None
            ),
        ):
            st.markdown("**Original text**")
            st.text(item["text"])

            st.markdown("**Detection details**")
            h1, h2, h3 = st.columns(3)
            h1.metric("Language", item["language"])
            h2.metric("ISO code", item["code"])
            h3.metric("Detection", score_label(item))

            st.caption(
                f"Writing system: {item['script']} · "
                f"Method: {item['method']}"
            )
else:
    st.info(
        "No detection history yet. Enter some text and detect its language!"
    )


# =====================================================
# FOOTER
# =====================================================

st.divider()
st.markdown(
    """
    <div class="footer">
        <strong>🌍 Polyglot AI</strong><br>
        AI-Powered Language Detection System<br><br>
        Built with Python · Lingua NLP · Streamlit<br>
        Day 12 · 30 Days – 30 AI Projects
    </div>
    """,
    unsafe_allow_html=True,
)
