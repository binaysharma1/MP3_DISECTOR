from pathlib import Path
from subprocess import run

import torch
import torchaudio
from demucs.apply import apply_model
from demucs.pretrained import get_model


_model = None


def _get_model():
    global _model
    if _model is None:
        _model = get_model("htdemucs")
        _model.eval()
    return _model


def _save_mp3(waveform: torch.Tensor, sample_rate: int, output_path: Path, bitrate: str) -> None:
    wav_path = output_path.with_suffix(".wav")
    torchaudio.save(str(wav_path), waveform, sample_rate, format="wav")
    try:
        run(
            [
                "ffmpeg",
                "-y",
                "-loglevel",
                "error",
                "-i",
                str(wav_path),
                "-codec:a",
                "libmp3lame",
                "-b:a",
                f"{bitrate}k",
                str(output_path),
            ],
            check=True,
        )
    finally:
        wav_path.unlink(missing_ok=True)


def separate_audio(input_path: Path, output_dir: Path, bitrate: str = "320") -> None:
    """Separate an audio file into vocals and instrumental MP3 files."""
    model = _get_model()
    waveform, sample_rate = torchaudio.load(str(input_path))
    if sample_rate != model.samplerate:
        waveform = torchaudio.functional.resample(waveform, sample_rate, model.samplerate)

    with torch.inference_mode():
        sources = apply_model(
            model,
            waveform.unsqueeze(0),
            device="cuda" if torch.cuda.is_available() else "cpu",
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    vocals = sources[0, model.sources.index("vocals")].cpu()
    instrumental = sum(
        sources[0, model.sources.index(source)]
        for source in ("drums", "bass", "other")
    ).cpu()
    _save_mp3(vocals, model.samplerate, output_dir / "vocals.mp3", bitrate)
    _save_mp3(instrumental, model.samplerate, output_dir / "instrumental.mp3", bitrate)
