"""Background worker: queued job -> download -> transcribe -> drafts -> 9:16 clip.

Pure/IO split: all timing, scoring, draft and ffmpeg-argv math lives in
pipeline.py (tested by checks.py); this file is the queue and the disk writes.
One daemon thread, no broker (BUILD §2).
"""
import json
import pathlib
import subprocess
import threading
import time

import db
import pipeline

LOOP_S = 3          # worker wake-up interval
CLIP_DIR = pathlib.Path(__file__).parent / "var" / "clips"
UPLOAD_DIR = pathlib.Path(__file__).parent / "var" / "uploads"


def _set(con, jid: int, **cols) -> None:
    keys = ", ".join(f"{k}=?" for k in cols)
    con.execute(f"UPDATE jobs SET {keys} WHERE id=?", (*cols.values(), jid))


def run_job(jid: int, app=None) -> dict:
    import transcribe  # lazy: keeps `import jobs` free of yt-dlp/ctranslate2

    def log(msg):
        if app:
            print(f"[repurpose] job {jid}: {msg}")

    with db.get() as con:
        row = db.get_job(con, jid)
    if not row:
        return {"id": jid, "status": "failed"}
    if row["status"] == "done":
        return {"id": jid, "status": "done"}

    with db.get() as con:
        _set(con, jid, status="running", stage="download", error="")
    try:
        # 1. media in (YouTube URL or uploaded file)
        media = transcribe.download(row["source"], UPLOAD_DIR)
        # YouTube jobs take their title from the download; uploads keep the filename
        title = row["title"] or media.get("title") or ""
        path = media["audio"]
        log(f"downloaded {title}")

        # 2. transcript (word-level timings for the subtitles)
        with db.get() as con:
            _set(con, jid, stage="transcribe", title=title)
        with db.get() as con:
            model = db.get_setting(con, "whisper_model", "base") or "base"
        t = transcribe.transcribe(path, model)
        segs = t["segments"]
        log(f"transcribed {len(segs)} segments, {t['duration']}s")

        # 3. extractive drafts (no LLM by design — BUILD §7)
        with db.get() as con:
            _set(con, jid, stage="draft", transcript=json.dumps(segs),
                 duration=t["duration"], linkedin=pipeline.linkedin_post(title, segs),
                 twitter=pipeline.twitter_thread(title, segs))

        # 4. one 9:16 clip with burned, clip-relative subtitles
        with db.get() as con:
            _set(con, jid, stage="clip")
        length = _clip_length()
        if not _has_video(path):
            # audio-only source (mp3/wav podcast): deliver transcript + drafts,
            # skip the clip (job.html says "No clip generated for this job")
            with db.get() as con:
                _set(con, jid, status="done", stage="")
            log("no video track in source — skipping the 9:16 clip")
            return {"id": jid, "status": "done"}
        start, end = pipeline.pick_highlight(segs, t["duration"], length)
        words = [w for s in segs for w in s.get("words", [])]
        cues = pipeline.clip_cues(pipeline.words_to_cues(words), start, end)
        CLIP_DIR.mkdir(parents=True, exist_ok=True)
        srt_name = f"clip-{jid}.srt"
        out = CLIP_DIR / f"clip-{jid}.mp4"
        (CLIP_DIR / srt_name).write_text(pipeline.cues_to_srt(cues), encoding="utf8")
        cmd = pipeline.crop_cmd(path, start, end, str(out), srt_name=srt_name)
        r = subprocess.run(cmd, cwd=CLIP_DIR, capture_output=True, text=True, timeout=1800)
        if r.returncode != 0:
            raise RuntimeError((r.stderr or "ffmpeg failed").strip().splitlines()[-1][:300])
        log(f"clip {start}s -> {end}s")

        with db.get() as con:
            _set(con, jid, status="done", stage="", clip=str(out),
                 srt=str(CLIP_DIR / srt_name), clip_start=start, clip_end=end)
        return {"id": jid, "status": "done"}
    except Exception as e:
        with db.get() as con:
            _set(con, jid, status="failed", stage="", error=str(e)[:400])
        log(f"FAILED: {e}")
        return {"id": jid, "status": "failed", "error": str(e)}


def _has_video(path: str) -> bool:
    """ffprobe: does the source carry a video track? Audio-only input cannot be
    cropped to 9:16 — ffmpeg would exit 0 and mux a silent black mp4."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=codec_type", "-of", "csv=p=0", path],
            capture_output=True, text=True, timeout=60)
        return bool(out.stdout.strip())
    except Exception:
        return True  # no ffprobe: let ffmpeg be the judge


def _clip_length() -> float:
    with db.get() as con:
        raw = db.get_setting(con, "clip_length", "30")
    try:
        return max(5.0, min(60.0, float(raw)))
    except ValueError:
        return 30.0


def run_once(app=None) -> int:
    """Run every queued job once (manual 'process now' or the worker loop)."""
    done = 0
    while True:
        with db.get() as con:
            row = db.next_queued(con)
        if not row:
            return done
        run_job(row["id"], app)
        done += 1


def _loop() -> None:
    while True:
        try:
            if run_once():
                continue        # keep draining before sleeping
        except Exception as e:  # never let the thread die
            print(f"[repurpose] worker error: {e}")
        time.sleep(LOOP_S)


def start_worker(_app=None) -> threading.Thread:
    t = threading.Thread(target=_loop, daemon=True, name="repurpose-worker")
    t.start()
    return t
