from pathlib import Path
from tempfile import NamedTemporaryFile
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from brain import separate_audio


BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "audio-generated"
RESULTS_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="MusicSplit Studio API",
    description="Audio separation API for MusicSplit Studio.",
    version="1.0.0",
)
app.mount("/results", StaticFiles(directory=RESULTS_DIR), name="results")


class YouTubeRequest(BaseModel):
    url: str = Field(min_length=1)
    mode: str = "separate"
    bitrate: str = "320"


def download_youtube_audio(url: str, output_dir: Path, bitrate: str) -> Path:
    """Download the best available audio and convert it to an MP3."""
    output_dir.mkdir(parents=True, exist_ok=True)
    options = {
        "format": "bestaudio/best",
        "outtmpl": str(output_dir / "source.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": bitrate,
            }
        ],
    }
    try:
        with YoutubeDL(options) as downloader:
            downloader.download([url])
    except DownloadError as error:
        raise ValueError(f"Could not download the YouTube audio: {error}") from error

    audio_path = output_dir / "source.mp3"
    if not audio_path.exists():
        raise ValueError("yt-dlp did not produce an MP3 file.")
    return audio_path


@app.post("/upload")
async def upload_mp3(file: UploadFile = File(...)):
    """Run the uploaded audio through the Demucs separation pipeline."""
    suffix = Path(file.filename or "audio.wav").suffix.lower()
    if suffix not in {".mp3", ".wav", ".m4a"}:
        raise HTTPException(status_code=400, detail="Only mp3, wav, and m4a files are supported.")

    job_id = uuid4().hex
    input_path = None
    try:
        with NamedTemporaryFile(suffix=suffix, delete=False) as temporary_file:
            input_path = Path(temporary_file.name)
            while chunk := await file.read(1024 * 1024):
                temporary_file.write(chunk)

        output_dir = RESULTS_DIR / job_id
        await run_in_threadpool(separate_audio, input_path, output_dir)
        return {
            "job_id": job_id,
            "stems": {
                "vocals": f"/results/{job_id}/vocals.mp3",
                "instrumental": f"/results/{job_id}/instrumental.mp3",
            },
        }
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Audio separation failed: {error}") from error
    finally:
        if input_path is not None:
            input_path.unlink(missing_ok=True)
        await file.close()


@app.post("/youtube")
async def download_from_youtube(request: YouTubeRequest):
    """Download a YouTube track as a high-quality MP3, optionally separating it."""
    if request.mode not in {"raw", "separate"}:
        raise HTTPException(status_code=400, detail="Mode must be 'raw' or 'separate'.")
    if request.bitrate not in {"128", "192", "320"}:
        raise HTTPException(status_code=400, detail="Bitrate must be 128, 192, or 320 kbps.")

    job_id = uuid4().hex
    output_dir = RESULTS_DIR / job_id
    try:
        source_path = await run_in_threadpool(
            download_youtube_audio, request.url, output_dir, request.bitrate
        )
        if request.mode == "raw":
            return {
                "job_id": job_id,
                "raw": f"/results/{job_id}/{source_path.name}",
            }

        await run_in_threadpool(separate_audio, source_path, output_dir, request.bitrate)
        source_path.unlink(missing_ok=True)
        return {
            "job_id": job_id,
            "stems": {
                "vocals": f"/results/{job_id}/vocals.mp3",
                "instrumental": f"/results/{job_id}/instrumental.mp3",
            },
        }
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"YouTube processing failed: {error}") from error
