import time
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
            with st.status("🔄 Processing audio through AI model...", expanded=True) as status:
                st.write("Initializing Demucs neural network architecture...")
                time.sleep(1.2)
                st.write("Isolating vocals and backing instrumental frequencies...")
                time.sleep(1.5)
                st.write("Reconstructing high-fidelity stereo outputs...")
                time.sleep(1.0)
                status.update(label="✅ Separation Complete!", state="complete", expanded=False)

            st.balloons()
            st.markdown("---")
            st.subheader("🎵 Resulting Stems")

            # Mock layout for outputs
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.markdown("#### 🎤 Isolated Vocals")
                st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") # Placeholder link for UI experience
                st.download_button(
                    label="📥 Download Vocals (.mp3)",
                    data=b"mock_audio_bytes",
                    file_name="vocals_stem.mp3",
                    mime="audio/mp3",
                    use_container_width=True,
                )

            with res_col2:
                st.markdown("#### 🎸 Instrumental Track")
                st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3") # Placeholder link for UI experience
                st.download_button(
                    label="📥 Download Instrumental (.mp3)",
                    data=b"mock_audio_bytes",
                    file_name="instrumental_stem.mp3",
                    mime="audio/mp3",
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

    if download_extract_btn:
        if not yt_url:
            st.error("Please enter a valid YouTube link first.")
        else:
            with st.status("🌐 Connecting to YouTube & Processing...", expanded=True) as status_yt:
                st.write("Fetching media stream via yt-dlp...")
                time.sleep(1.5)
                st.write("Converting container to high-rate MP3...")
                time.sleep(1.0)
                st.write("Running audio separation model...")
                time.sleep(1.8)
                status_yt.update(label="✨ Extraction & Separation Finished!", state="complete", expanded=False)

            st.success("Your stems are ready for download!")
            
            # Display columns for 2 or 4 stems depending on user selection
            st.markdown("### 📦 Dissected Output Stems")
            y_col1, y_col2 = st.columns(2)
            
            with y_col1:
                st.markdown("##### 🎙️ Vocals Stem")
                st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3")
                st.download_button("Download Vocals", b"data", "youtube_vocals.mp3", key="y_voc", use_container_width=True)
                
            with y_col2:
                st.markdown("##### 🎹 Instrumental Backing")
                st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3")
                st.download_button("Download Instrumental", b"data", "youtube_instrumental.mp3", key="y_inst", use_container_width=True)

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