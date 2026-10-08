"""Media download + transcription helpers.

This module is the only place that touches yt-dlp and faster-whisper; both are
imported lazily inside their functions, so importing this module costs nothing
and never triggers a model load.
"""

import os
from pathlib import Path

# loaded/downloaded once per process, keyed by model size
MODEL = {}


def download(source: str, dest_dir) -> dict:
    """source is either a YouTube URL or an existing local media file path.
    Returns {"audio": <path str>, "title": <str>}.
    Raises ValueError with a readable message (<=300 chars) on any failure."""
    dest = Path(dest_dir)

    if source.startswith(("http://", "https://")):
        import yt_dlp

        dest.mkdir(parents=True, exist_ok=True)
        opts = {
            # video + audio, merged: the 9:16 clip needs real video frames
            "format": "bv*[height<=720]+ba/b[height<=720]/b",
            "merge_output_format": "mp4",
            "outtmpl": str(dest / "%(id)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "socket_timeout": 30,
            "playlist_items": "1",
        }
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(source, download=True)
                if info.get("entries"):
                    entries = [e for e in info["entries"] if e]
                    info = entries[0] if entries else info
                audio = ""
                for rd in info.get("requested_downloads") or []:
                    if rd.get("filepath"):
                        audio = rd["filepath"]
                        break
                audio = audio or info.get("filepath") or ydl.prepare_filename(info)
                if not os.path.exists(audio):
                    # merged downloads change extension: fall back to newest file for this id
                    vid = info.get("id") or ""
                    cand = [p for p in dest.glob(f"{vid}.*")
                            if p.suffix not in (".part", ".ytdl", ".json")]
                    if cand:
                        cand.sort(key=lambda p: p.stat().st_mtime)
                        audio = str(cand[-1])
        except yt_dlp.utils.DownloadError as e:
            raise ValueError(str(e)[:300]) from None
        return {"audio": str(audio), "title": info.get("title") or ""}

    if not os.path.exists(source):
        raise ValueError(f"local media file not found: {source}")
    p = Path(source)
    return {"audio": str(p.resolve()), "title": p.stem}


def transcribe(audio_path: str, model_size: str = "base") -> dict:
    from faster_whisper import WhisperModel

    model = MODEL.get(model_size)
    if model is None:
        model = WhisperModel(model_size, device="cpu", compute_type="int8", cpu_threads=4)
        MODEL[model_size] = model

    try:
        seg_iter, winfo = model.transcribe(audio_path, word_timestamps=True, vad_filter=True)
        segments = []
        last_end = 0.0
        # the generator is lazy: consume it fully here or results are lost
        for seg in seg_iter:
            last_end = max(last_end, float(seg.end))
            segments.append(
                {
                    "start": round(float(seg.start), 3),
                    "end": round(float(seg.end), 3),
                    "text": (seg.text or "").strip(),
                    "words": [
                        {
                            "start": round(float(w.start), 3),
                            "end": round(float(w.end), 3),
                            "text": (w.word or "").strip(),
                        }
                        for w in (seg.words or [])
                    ],
                }
            )
    except Exception as e:
        raise ValueError(f"unreadable audio file {audio_path}: {e}"[:300]) from None

    duration = round(max(float(winfo.duration or 0), last_end), 3)
    return {"duration": duration, "segments": segments}
