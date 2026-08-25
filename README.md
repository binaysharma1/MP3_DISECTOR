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
- **FastAPI backend:** Exposes the service application defined in `backend.py`.
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

The UI and API are currently prototype surfaces: the Streamlit processing results use placeholder audio data, and the backend processing endpoint is not yet connected to the full Demucs pipeline.
