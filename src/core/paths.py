from pathlib import Path

OUTPUTS_ROOT = Path("outputs")


def job_dir(job_id: str) -> Path:
    """Root folder for everything related to one job."""
    return OUTPUTS_ROOT / job_id


def script_path(job_id: str) -> Path:
    """analysis + structure + final_script, as JSON."""
    return job_dir(job_id) / "script.json"


def voice_path(job_id: str) -> Path:
    """Raw voiceover output from the TTS provider."""
    return job_dir(job_id) / "voice.wav"


def voice_trimmed_path(job_id: str) -> Path:
    """Voiceover after dead-air is cut."""
    return job_dir(job_id) / "voice_trimmed.wav"


def captions_path(job_id: str) -> Path:
    """Generated captions file."""
    return job_dir(job_id) / "captions.srt"


def background_video_path(job_id: str) -> Path:
    """Background video the user provided."""
    return job_dir(job_id) / "background.mp4"


def final_video_path(job_id: str) -> Path:
    """The finished, watchable short."""
    return job_dir(job_id) / "final.mp4"


def status_path(job_id: str) -> Path:
    """Current processing status of the job."""
    return job_dir(job_id) / "status.json"


def ensure_job_dir(job_id: str) -> Path:
    """Create the job's folder if it doesn't exist yet, and return it."""
    path = job_dir(job_id)
    path.mkdir(parents=True, exist_ok=True)
    return path