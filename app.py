"""repurpose — YouTube URL -> transcript -> LinkedIn/X drafts -> one 9:16 clip.

Run: uv run flask --app app run      Check: uv run python checks.py
"""
import json
import pathlib
import uuid

import db
from flask import (Flask, abort, jsonify, redirect, render_template, request,
                   send_file, url_for)

app = Flask(__name__)
db.init()

UPLOAD_DIR = pathlib.Path(__file__).parent / "var" / "uploads"
CLIP_DIR = pathlib.Path(__file__).parent / "var" / "clips"
ALLOWED = {".mp4", ".mov", ".mp3", ".wav", ".m4a", ".webm"}
MAX_MB = 500
app.config["MAX_CONTENT_LENGTH"] = MAX_MB * 1024 * 1024   # upload cap

_worker = None


def worker():
    global _worker
    if _worker is None or not _worker.is_alive():
        import jobs  # lazy: starts the background pipeline thread

        _worker = jobs.start_worker(app)
    return _worker


# --- pages ---------------------------------------------------------------

@app.get("/")
def index():
    with db.get() as con:
        jobs_list = db.list_jobs(con)
        model = db.get_setting(con, "whisper_model", "base")
        clip_len = db.get_setting(con, "clip_length", "30")
    return render_template("index.html", jobs=jobs_list, model=model,
                           clip_len=clip_len)


@app.get("/job/<int:jid>")
def job_page(jid: int):
    with db.get() as con:
        row = db.get_job(con, jid)
    if not row:
        abort(404)
    j = dict(row)
    j["segments"] = json.loads(j["transcript"] or "[]")
    return render_template("job.html", j=j)


@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        with db.get() as con:
            for key in ("whisper_model", "clip_length"):
                if key in request.form:
                    db.set_setting(con, key, request.form[key].strip())
        return redirect(url_for("index"))
    with db.get() as con:
        vals = {k: db.get_setting(con, k, d)
                for k, d in (("whisper_model", "base"), ("clip_length", "30"))}
    return render_template("settings.html", s=vals)


# --- actions -------------------------------------------------------------

@app.post("/ingest")
def ingest():
    url = (request.form.get("url") or "").strip()
    f = request.files.get("file")
    source = ""
    title = ""
    if f and f.filename:
        ext = pathlib.Path(f.filename).suffix.lower()
        if ext not in ALLOWED:
            return jsonify(ok=False, msg=f"unsupported file type {ext}"), 400
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        name = f"{uuid.uuid4().hex}{ext}"
        f.save(UPLOAD_DIR / name)
        source = str(UPLOAD_DIR / name)
        title = pathlib.Path(f.filename).stem
    elif url:
        source = url
    else:
        return jsonify(ok=False, msg="paste a YouTube URL or choose a file"), 400

    with db.get() as con:
        jid = db.add_job(con, source, title)
    worker()
    return redirect(url_for("job_page", jid=jid))


@app.get("/job/<int:jid>/status")
def job_status(jid: int):
    with db.get() as con:
        row = db.get_job(con, jid)
    if not row:
        abort(404)
    return jsonify(status=row["status"], stage=row["stage"], error=row["error"],
                   title=row["title"], clip_start=row["clip_start"],
                   clip_end=row["clip_end"], has_clip=bool(row["clip"]))


@app.post("/job/<int:jid>/save")
def job_save(jid: int):
    with db.get() as con:
        if not db.get_job(con, jid):
            abort(404)
        con.execute("UPDATE jobs SET linkedin=?, twitter=? WHERE id=?",
                    (request.form.get("linkedin", ""),
                     request.form.get("twitter", ""), jid))
    return jsonify(ok=True, msg="Saved")


@app.get("/job/<int:jid>/clip")
def job_clip(jid: int):
    with db.get() as con:
        row = db.get_job(con, jid)
    if not row or not row["clip"] or not pathlib.Path(row["clip"]).exists():
        abort(404)
    return send_file(row["clip"], mimetype="video/mp4", conditional=True)


@app.get("/job/<int:jid>/srt")
def job_srt(jid: int):
    with db.get() as con:
        row = db.get_job(con, jid)
    if not row or not row["srt"] or not pathlib.Path(row["srt"]).exists():
        abort(404)
    return send_file(row["srt"], mimetype="application/x-subrip", as_attachment=True,
                     download_name=f"clip-{jid}.srt")


@app.get("/status")
def status():
    with db.get() as con:
        n = con.execute("SELECT COUNT(*) c FROM jobs").fetchone()["c"]
        busy = con.execute(
            "SELECT COUNT(*) c FROM jobs WHERE status IN ('queued','running')"
        ).fetchone()["c"]
    return jsonify(jobs=n, pending=busy,
                   worker_alive=bool(_worker and _worker.is_alive()))


worker()  # start the pipeline thread at import time (`flask --app app run`)
