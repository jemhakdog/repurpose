"""SQLite schema + helpers. One file, WAL mode, stdlib sqlite3."""
import pathlib
import sqlite3

DB_PATH = pathlib.Path(__file__).parent / "var" / "repurpose.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS jobs (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    source     TEXT NOT NULL,                      -- youtube url or var/uploads/<file>
    title      TEXT NOT NULL DEFAULT '',
    status     TEXT NOT NULL DEFAULT 'queued',     -- queued|running|done|failed
    stage      TEXT NOT NULL DEFAULT '',           -- download|transcribe|draft|clip
    error      TEXT NOT NULL DEFAULT '',
    transcript TEXT NOT NULL DEFAULT '[]',         -- JSON [{"start","end","text","words"}]
    duration   REAL NOT NULL DEFAULT 0,
    linkedin   TEXT NOT NULL DEFAULT '',
    twitter    TEXT NOT NULL DEFAULT '',           -- tweets separated by blank lines
    clip       TEXT NOT NULL DEFAULT '',           -- path to var/clips/<id>.mp4
    srt        TEXT NOT NULL DEFAULT '',
    clip_start REAL NOT NULL DEFAULT 0,
    clip_end   REAL NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def get() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    return con


def init() -> None:
    with get() as con:
        con.executescript(SCHEMA)


def get_setting(con: sqlite3.Connection, key: str, default: str = "") -> str:
    row = con.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    return row["value"] if row else default


def set_setting(con: sqlite3.Connection, key: str, value: str) -> None:
    con.execute(
        "INSERT INTO settings(key,value) VALUES(?,?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value),
    )


def add_job(con: sqlite3.Connection, source: str, title: str = "") -> int:
    cur = con.execute("INSERT INTO jobs(source,title) VALUES(?,?)", (source, title))
    return cur.lastrowid


def get_job(con: sqlite3.Connection, jid: int) -> sqlite3.Row | None:
    return con.execute("SELECT * FROM jobs WHERE id=?", (jid,)).fetchone()


def list_jobs(con: sqlite3.Connection, limit: int = 50) -> list[sqlite3.Row]:
    return con.execute(
        "SELECT id,title,source,status,stage,error,clip_start,clip_end,created_at "
        "FROM jobs ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()


def next_queued(con: sqlite3.Connection) -> sqlite3.Row | None:
    return con.execute(
        "SELECT * FROM jobs WHERE status='queued' ORDER BY id LIMIT 1"
    ).fetchone()
