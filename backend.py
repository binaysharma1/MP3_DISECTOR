from pathlib import Path
from tempfile import NamedTemporaryFile
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool

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
