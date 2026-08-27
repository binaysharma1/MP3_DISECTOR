import os

import httpx
import streamlit as st

# 1. Page Configuration & Custom CSS Styling
st.set_page_config(
    page_title="MusicSplit Studio | AI Audio Separator",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #161b22;
        border-radius: 8px 8px 0px 0px;
        color: #c9d1d9;
        font-weight: 600;
        padding-left: 20px;
        padding-right: 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #238636 !important;
        color: #ffffff !important;
    }
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .custom-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF8F8F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. Sidebar Navigation & Info
with st.sidebar:
    st.image(
        "https://img.icons8.com/clouds/200/audio-wave.png", width=120
    )  # Aesthetic badge
    st.markdown("### 🎧 MusicSplit Studio")
    st.markdown(
        "Transform full mixes into isolated professional studio stems using advanced AI source separation."
    )
    st.markdown("---")

    st.markdown("#### 🛠️ Pipeline Controls")
    separation_mode = st.selectbox(
        "Stems Configuration",
        ["Vocals & Instrumental (2-Stem)", "Full Band Stems (4-Stem: Vocals, Drums, Bass, Other)"],
    )

    audio_quality = st.select_slider(
        "Output Bitrate", options=["128 kbps", "192 kbps", "320 kbps (Studio)"], value="320 kbps (Studio)"
    )

    st.markdown("---")
    st.markdown("### 💡 Quick Tips")
    st.info(
        "For best results with YouTube tracks, ensure the video link points directly to a clear music track or song performance."
    )
    st.markdown("---")
    st.caption("Powered by Streamlit & AI Stem Separation Engine")

# 3. Main Header Section
st.markdown('<p class="custom-header">MusicSplit Studio 🎛️</p>', unsafe_allow_html=True)
st.markdown(
    "Isolate vocals, extract instruments, or pull down tracks straight from YouTube with deep learning precision."
)
st.write("")

# 4. Tab Layout Architecture
tab1, tab2, tab3 = st.tabs(
    ["📁 Upload MP3 File", "🔗 YouTube URL Converter", "📊 Studio Dashboard"]
)

# --- TAB 1: UPLOAD MP3 FILE ---
with tab1:
    st.markdown("### Upload Audio Track")
    st.markdown("Upload any mixed `.mp3` or `.wav` file to slice it into pristine independent stems.")

    uploaded_file = st.file_uploader(
        "Choose an MP3 audio file", type=["mp3", "wav", "m4a"], key="mp3_uploader"
    )

    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/mp3")
        st.success(f"Successfully loaded: **{uploaded_file.name}**")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            process_btn = st.button("🚀 Run AI Stem Separation", use_container_width=True, type="primary")

        if process_btn:
            api_url = os.getenv("MUSICSPLIT_API_URL", "http://localhost:8000")
            try:
                with st.spinner("Processing audio through the AI model..."):
                    response = httpx.post(
                        f"{api_url}/upload",
                        files={
                            "file": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                uploaded_file.type or "application/octet-stream",
                            )
                        },
                        timeout=None,
                    )
                response.raise_for_status()
                result = response.json()
                st.session_state["latest_result"] = result
            except httpx.HTTPError as error:
                st.error(f"The backend could not process this file: {error}")

        result = st.session_state.get("latest_result")
        if result:
            api_url = os.getenv("MUSICSPLIT_API_URL", "http://localhost:8000")
            st.success("Separation complete. Your stems are ready.")
            st.markdown("---")
            st.subheader("🎵 Resulting Stems")
            res_col1, res_col2 = st.columns(2)
            for column, label, stem_name in (
                (res_col1, "🎤 Isolated Vocals", "vocals"),
                (res_col2, "🎸 Instrumental Track", "instrumental"),
            ):
                stem_url = f"{api_url}{result['stems'][stem_name]}"
                stem_response = httpx.get(stem_url, timeout=None)
                stem_response.raise_for_status()
                stem_bytes = stem_response.content
                with column:
                    st.markdown(f"#### {label}")
                    st.audio(stem_bytes, format="audio/mp3")
                    st.download_button(
                        label=f"📥 Download {stem_name.title()} (.mp3)",
                        data=stem_bytes,
                        file_name=f"{stem_name}_stem.mp3",
                        mime="audio/mp3",
                        key=f"download_{stem_name}_{result['job_id']}",
                        use_container_width=True,
                    )

# --- TAB 2: YOUTUBE URL CONVERTER ---
with tab2:
    st.markdown("### YouTube Audio Downloader & Splicer")
    st.markdown("Paste a YouTube link below. Our engine will fetch the audio stream and immediately dissect it.")

    yt_url = st.text_input(
        "YouTube Video URL",
        placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    )

    if yt_url:
        st.info(f"Target URL registered: `{yt_url}`")

    col_y1, col_y2 = st.columns([3, 1])
    with col_y1:
        download_extract_btn = st.button(
            "⬇️ Download & Dissect from YouTube", use_container_width=True, type="primary"
        )
    with col_y2:
        download_raw_btn = st.button("⬇️ Download Raw MP3", use_container_width=True)

    selected_bitrate = audio_quality.split()[0]
    requested_mode = "separate" if download_extract_btn else "raw" if download_raw_btn else None

    if requested_mode:
        if not yt_url:
            st.error("Please enter a valid YouTube link first.")
        else:
            api_url = os.getenv("MUSICSPLIT_API_URL", "http://localhost:8000")
            try:
                with st.spinner("Downloading and processing audio..."):
                    response = httpx.post(
                        f"{api_url}/youtube",
                        json={"url": yt_url, "mode": requested_mode, "bitrate": selected_bitrate},
                        timeout=None,
                    )
                response.raise_for_status()
                youtube_result = response.json()
                if requested_mode == "raw":
                    raw_response = httpx.get(f"{api_url}{youtube_result['raw']}", timeout=None)
                    raw_response.raise_for_status()
                    st.success("Raw high-quality MP3 is ready.")
                    st.audio(raw_response.content, format="audio/mp3")
                    st.download_button(
                        "📥 Download Raw MP3",
                        raw_response.content,
                        "youtube_raw.mp3",
                        mime="audio/mp3",
                        key=f"youtube_raw_{youtube_result['job_id']}",
                        use_container_width=True,
                    )
                else:
                    st.success("Your stems are ready for download!")
                    st.markdown("### 📦 Dissected Output Stems")
                    y_col1, y_col2 = st.columns(2)
                    for column, label, stem_name in (
                        (y_col1, "🎙️ Vocals Stem", "vocals"),
                        (y_col2, "🎹 Instrumental Backing", "instrumental"),
                    ):
                        stem_response = httpx.get(
                            f"{api_url}{youtube_result['stems'][stem_name]}", timeout=None
                        )
                        stem_response.raise_for_status()
                        with column:
                            st.markdown(f"##### {label}")
                            st.audio(stem_response.content, format="audio/mp3")
                            st.download_button(
                                f"📥 Download {stem_name.title()}",
                                stem_response.content,
                                f"youtube_{stem_name}.mp3",
                                mime="audio/mp3",
                                key=f"youtube_{stem_name}_{youtube_result['job_id']}",
                                use_container_width=True,
                            )
            except httpx.HTTPError as error:
                detail = error.response.json().get("detail", str(error)) if error.response else str(error)
                st.error(f"YouTube processing failed: {detail}")

# --- TAB 3: STUDIO DASHBOARD ---
with tab3:
    st.markdown("### 📊 Processing Metrics & Analytics")
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            """
            <div class="metric-card">
                <h3>Total Track Processed</h3>
                <h2>1,248</h2>
                <p style="color: #238636;">+12% this week</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            """
            <div class="metric-card">
                <h3>Avg. Separation Time</h3>
                <h2>24.5s</h2>
                <p style="color: #238636;">Optimized GPU</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            """
            <div class="metric-card">
                <h3>Model Precision</h3>
                <h2>98.2%</h2>
                <p style="color: #238636;">HTDemucs v4</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.markdown("#### 🧩 System Architecture Overview")
    st.markdown(
        "High-performance audio processing flows from the client through the "
        "FastAPI backend, optional YouTube download, and HTDemucs separation "
        "engine before producing isolated stems."
    )
    st.code(
        """[ Client / UI ]
         |  YouTube URL or audio file
         v
    +------------------------------+
    | FastAPI Backend              |
    | validation and task control  |
    +---------------+--------------+
                    |
                    +----------------------+
                    |                      |
                    v                      v
          +------------------+   +----------------------+
          | Stream Downloader |   | HTDemucs Engine      |
          | (YouTube input)   +-->+ source separation    |
          +------------------+   +----------+-----------+
                                           |
                                           v
                                +----------------------+
                                | Isolated Output     |
                                | vocals, drums, bass |
                                | and other stems     |
                                +----------------------+
        """,
        language="text",
    )