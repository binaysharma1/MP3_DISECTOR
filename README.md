🎧 AI Audio Source Separation Pipeline
A high-performance, asynchronous backend pipeline designed to isolate vocals, instruments, and custom stems from mixed audio files or direct YouTube tracks using Meta's HTDemucs (Hybrid Transformer Demucs) and FastAPI.

🏗️ Architectural Blueprint & Data Flow

[ Client / UI ] 
      │  (Sends YouTube URL or Direct File)
      ▼
┌──────────────────────────────────────────────┐
│             FastAPI Backend Layer            │
│  - Endpoint routing & validation             │
│  - Task coordination & temp file management  │
└──────────────────────┬───────────────────────┘
                       │
         ┌─────────────┴─────────────↓ (If YouTube URL)
         ▼                           
┌─────────────────┐         ┌──────────────────────────────────┐
│                 │         │         HTDemucs Engine          │
│ Stream Downloader│────────►│  - Dual-Domain U-Net (Waveform)  │
└─────────────────┘         │  - Cross-Domain Transformer Core │
                            └──────────────────┬───────────────┘
                                               │
                                               ▼
                            ┌──────────────────────────────────┐
                            │      Isolated Output Stems       │
                            │  (Vocals, Instrumental, Drums...)│
                            └──────────────────────────────────┘

⚙️ Core Component Breakdown
A. The Ingestion & Routing Layer (FastAPI)
Asynchronous REST Endpoints: Manages incoming requests (POST /process-youtube or POST /upload-audio) using async pathways, ensuring the event loop remains 
unblocked during heavy CPU/GPU operations.
Payload & File Lifecycle Management: Automatically initializes isolated temporary directories (tempfile) to safely handle downloads, stream conversions, and
immediate cleanup to prevent server storage bloat.


B. The Stream Fetcher (yt-dlp / PyTube)
Target Resolution: Extracts raw, high-quality audio media streams directly from target URLs.
Stream Normalization: Converts incoming web video streams into uniform PCM audio codecs (.mp3 / .wav) via integrated ffmpeg subprocess pipelines to prepare
inputs for deep learning inference.


The Deep Learning Separation Core (HTDemucs)
Hybrid Architecture: Utilizes Meta's HTDemucs v4, combining Waveform Temporal Convolutions with Spectrogram Cross-Domain Transformers.

Inference Execution: Processes normalized audio arrays layer-by-layer through self-attention and cross-attention blocks to cleanly isolate mixed sound waves 
into distinct stems (Vocals, Drums, Bass, and Other accompaniments).

🛠️ Production Design Considerations
Process Isolation: Because deep learning frameworks like PyTorch and Demucs consume significant RAM/VRAM, separating execution inside worker subprocesses or 
task queues (e.g., Celery with Redis) prevents memory leaks from crashing the core FastAPI server instance.

Model Caching: Pre-loads htdemucs weights into memory during container startup to eliminate cold-start latency for incoming user requests.


🚀 Quick Start Setup
Prerequisites
Python 3.10+

FFmpeg installed on your system path (sudo apt install ffmpeg or brew install ffmpeg)

Istallation & Run
Clone the repository: git clone https://github.com/your-username/audio-separation-backend.git
cd audio-separation-backend

Install dependencies:uv venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
uv sync

start fastapi and streamlit serer.

📄 License
Distributed under the MIT License. See LICENSE for more information.


