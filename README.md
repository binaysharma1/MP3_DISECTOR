# MusicSplit Studio

MusicSplit Studio is an audio stem-separation prototype. It provides a Streamlit interface for uploading audio or entering a YouTube URL, with a FastAPI service prepared for upload and processing endpoints.

## Project Architecture

```text
MP3_POST-MORTEM/
├── page.py                 # Streamlit web UI and user workflows
├── backend.py              # FastAPI application and HTTP endpoints
├── brain.ipynb             # Audio-processing experiments and prototypes
├── audio/                  # Source audio files used during development
├── audio-generated/        # Generated or separated audio output
├── pyproject.toml          # Project metadata and Python dependencies
├── uv.lock                 # Locked dependency versions
├── .gitignore              # Local files excluded from version control
└── README.md               # Project documentation
```

### Runtime Flow

```text
User
  │
  ├── Uploads an audio file
  └── Provides a YouTube URL
       │
       ▼
Streamlit UI (`page.py`)
       │
       ├── FastAPI service (`backend.py`)
       │       │
       │       ▼
       │   Audio separation pipeline
       │       │
       │       ├── Demucs / HTDemucs model
       │       └── Generated stems
       │              │
       │              ▼
       │      `audio-generated/`
       │
       └── Current UI prototype flow
```

## Components

- **Streamlit UI:** Runs the interactive studio interface from `page.py`.
- **FastAPI backend:** Exposes upload processing and a yt-dlp YouTube download endpoint defined in `backend.py`.
- **Separation engine:** Uses Demucs for source separation when connected to the processing workflow.
- **Notebook:** Contains exploratory work in `brain.ipynb`.
- **Audio directories:** `audio/` holds development inputs, while `audio-generated/` is intended for generated results.

## Setup

Python 3.12 or newer is required.

```bash
uv sync
```

## Run

Start the Streamlit interface:

```bash
uv run streamlit run page.py
```

Start the FastAPI service in a separate terminal:

```bash
uv run fastapi dev backend.py
```

Run both services at the same time. Streamlit uploads the selected file as multipart form data to `POST /upload`. YouTube requests use `POST /youtube` with `mode: "raw"` for a high-quality audio-only MP3 or `mode: "separate"` to download the best available audio and generate vocals and instrumental MP3 files. The notebook contains the original exploratory version of this processing logic.

The YouTube workflow requires both yt-dlp and FFmpeg. `uv sync` installs yt-dlp; install the system FFmpeg package separately if it is not already available on the host.

The Streamlit UI assumes the API is at `http://localhost:8000`. Set `MUSICSPLIT_API_URL` when it is hosted elsewhere:

```bash
MUSICSPLIT_API_URL=http://localhost:8000 uv run streamlit run page.py
```
