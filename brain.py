from pathlib import Path

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


def separate_audio(input_path: Path, output_dir: Path) -> None:
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
    torchaudio.save(str(output_dir / "vocals.mp3"), vocals, model.samplerate, format="mp3")
    torchaudio.save(
        str(output_dir / "instrumental.mp3"), instrumental, model.samplerate, format="mp3"
    )
