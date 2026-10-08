"""Pure pipeline logic: scoring, extractive drafts, clip math, captions, argv.

Stdlib only. No network, no ML imports, no I/O, no classes or config objects —
every function is flat and deterministic (same input -> same output), so
checks.py can assert exact values.

Segment shape, exactly what db.py stores as JSON in jobs.transcript:
    {"start": float, "end": float, "text": str,
     "words": [{"start": float, "end": float, "text": str}]}
"""
import re

HOOK_LIMIT = 200      # hook / bullet trim for the LinkedIn draft
POST_LIMIT = 1300     # LinkedIn budget; excess whole trailing lines are dropped
TWEET_LIMIT = 280     # X per-tweet budget, counter included

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


# --- timestamps ----------------------------------------------------------

def ts(seconds: float) -> str:
    """SRT timestamp HH:MM:SS,ms; negatives clamp to 00:00:00,000."""
    ms = max(0, int(round(seconds * 1000)))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# --- scoring --------------------------------------------------------------

def score_segment(seg: dict, index: int, total: int) -> float:
    """Deterministic highlight/draft score = position * content * length.

    Factors:
    * position — the first 10% of segments (intros) and the last 5% (outros)
      are halved, so "welcome back to the channel" and the sign-off never win
      the clip; the middle of the transcript keeps factor 1.0.
    * content  — +0.5 when the text has digits, +0.3 each for "$", "%" and a
      question mark. Numbers, money, percentages and questions are hooks.
    * length   — 8..30 words is quotable (1.0); 4..7 words ramps 0.4 -> 1.0;
      fewer than 4 words ("um ok yes") is ~0; over 30 words decays slowly.

    Pure: no randomness, no clock, same input -> same float.
    """
    text = " ".join(str(seg.get("text") or "").split())
    words = seg.get("words") or []
    n = len(words) if words else len(text.split())

    if n < 4:
        length = 0.0
    elif n < 8:
        length = 0.4 + 0.6 * (n - 4) / 4
    elif n <= 30:
        length = 1.0
    else:
        length = max(0.4, 1.0 - (n - 30) / 100.0)

    content = 1.0
    if any(ch.isdigit() for ch in text):
        content += 0.5
    if "$" in text:
        content += 0.3
    if "%" in text:
        content += 0.3
    if "?" in text:
        content += 0.3

    position = 1.0
    if total and total > 0:
        intro_n = max(1, int(round(total * 0.10)))
        outro_n = max(1, int(round(total * 0.05)))
        if index < intro_n or index >= total - outro_n:
            position = 0.5

    return round(position * content * length, 6)


def top_sentences(segments, n: int = 5) -> list[dict]:
    """Top-n segments by score; ties broken by lower index.

    Winners are returned in ORIGINAL transcript order (not ranked order).
    """
    segs = list(segments or [])
    if not segs or n <= 0:
        return []
    ranked = sorted(range(len(segs)),
                    key=lambda i: (-score_segment(segs[i], i, len(segs)), i))
    winners = sorted(ranked[:n])          # back to original order
    return [segs[i] for i in winners]


# --- text helpers ---------------------------------------------------------

def _words(text) -> str:
    """Collapse whitespace/newlines to single spaces."""
    return " ".join(str(text or "").split())


def _trim_words(text, limit: int) -> str:
    """Trim to <= limit chars on a word boundary (never mid-word). Falls back
    to a hard cut only when a single token is longer than the limit. Also used
    to make tweets fit: trailing words are dropped until they do."""
    t = _words(text)
    if len(t) <= limit:
        return t
    parts = t.split(" ")
    while parts and len(" ".join(parts)) > limit:
        parts.pop()
    out = " ".join(parts).strip()
    return out if out else t[:limit]


def _first_sentence(text, limit: int = TWEET_LIMIT) -> str:
    """First sentence of the text (split after . ! ? followed by space, so
    "$1.2M" does not break the sentence), trimmed to `limit`."""
    t = _words(text)
    if not t:
        return ""
    return _trim_words(_SENT_SPLIT.split(t)[0], limit)


def _hashtags(title: str) -> str:
    """Up to 3 title words (len > 2), title-cased, # prefixed; #insights
    when the title is empty or has no usable word."""
    seen, tags = set(), []
    for w in (title or "").split():
        w = w.strip(".,!?;:'\"()[]")
        if len(w) > 2 and w.lower() not in seen:
            seen.add(w.lower())
            tags.append("#" + w.title())
        if len(tags) == 3:
            break
    return " ".join(tags) if tags else "#insights"


# --- extractive drafts (no LLM) ------------------------------------------

def linkedin_post(title: str, segments) -> str:
    """Extractive LinkedIn draft; never returns "".

    Layout: hook / blank / "3 takeaways:" + 3 bullets / blank / closing
    question (when a title exists) / blank / hashtags.
    Over budget (>1300 chars) whole trailing lines are dropped — a line is
    never cut mid-sentence.
    """
    t = _words(title)
    segs = [s for s in (segments or []) if _words(s.get("text"))]
    if not segs:
        return (f"{t} — highlights worth sharing." if t
                else "Fresh highlights worth sharing.")

    hook_seg = top_sentences(segs, 1)[0]                       # best segment
    hook = _trim_words(hook_seg["text"], HOOK_LIMIT)
    # next-best 3 (distinct segments, hook skipped), original order
    bullets = ["- " + _first_sentence(s["text"], HOOK_LIMIT)
               for s in top_sentences(segs, 4) if s is not hook_seg]

    blocks = [hook, ""]
    if bullets:
        blocks += ["3 takeaways:"] + bullets + [""]
    if t:
        blocks.append(f"What's your take on {t}?")
        blocks.append("")
    blocks.append(_hashtags(title))

    while len("\n".join(blocks)) > POST_LIMIT and len(blocks) > 1:
        blocks.pop()                       # drop whole trailing lines
    return "\n".join(blocks).rstrip("\n")


def twitter_thread(title: str, segments, n: int = 6) -> str:
    """Extractive X thread; never returns "". Tweets are separated by a blank
    line, each starts with the "i/total " counter and fits TWEET_LIMIT chars
    including it (trailing words trimmed to make room, never mid-word).

    tweet 1 = hook, middle = top sentences in original order, last = CTA.
    """
    t = _words(title)
    segs = [s for s in (segments or []) if _words(s.get("text"))]
    if not segs:
        body = (f"{t}: no transcript to quote yet — check back soon." if t
                else "No transcript to quote yet — check back soon.")
        return _trim_words(f"1/1 {body}", TWEET_LIMIT)

    n = max(2, int(n))
    hook_seg = top_sentences(segs, 1)[0]
    bodies = [_words(hook_seg["text"])]
    for s in (x for x in top_sentences(segs, n) if x is not hook_seg):
        if len(bodies) >= n - 1:           # reserve the last tweet for the CTA
            break
        body = _first_sentence(s["text"])
        if body:
            bodies.append(body)
    bodies.append(f"That's the thread on {t}. What would you add?" if t
                  else "That's the thread. What would you add?")

    total = len(bodies)
    tweets = [_trim_words(f"{i}/{total} {b}", TWEET_LIMIT)
              for i, b in enumerate(bodies, 1)]
    return "\n\n".join(tweets)


# --- clip crop math -------------------------------------------------------

def pick_highlight(segments, duration: float, length: float = 30.0) -> tuple[float, float]:
    """Best (start, end) window of `length` seconds, rounded to 3 decimals.

    - duration <= 0  -> duration comes from the last segment's end
    - duration <= length -> the whole thing: (0, duration)
    - no segments -> (0, min(length, duration))
    - else slide a `length`-long window whose start is each segment start
      (clamped so end <= duration), score it by the summed score of the
      segments it overlaps, keep the highest; ties go to the earliest window.

    Invariants: 0 <= start < end <= duration, end - start <= length.
    """
    segs = list(segments or [])
    if duration <= 0:
        duration = float(segs[-1].get("end", 0.0)) if segs else 0.0
    if length <= 0 or duration <= length:
        return (0.0, round(duration, 3))
    if not segs:
        return (0.0, round(min(length, duration), 3))

    scores = [score_segment(s, i, len(segs)) for i, s in enumerate(segs)]
    starts = [float(s.get("start", 0.0) or 0.0) for s in segs]
    ends = [float(s.get("end", 0.0) or 0.0) for s in segs]
    limit = max(0.0, duration - length)

    best_score, best_start = None, 0.0
    for i in range(len(segs)):
        start = min(max(starts[i], 0.0), limit)   # keep end <= duration
        win_end = start + length
        total = sum(sc for j, sc in enumerate(scores)
                    if ends[j] > start and starts[j] < win_end)
        if (best_score is None or total > best_score
                or (total == best_score and start < best_start)):
            best_score, best_start = total, start

    start = round(best_start, 3)
    end = round(min(start + length, duration), 3)
    if end > duration or end - start > length:    # undo round-up slop
        end = round(min(start + length, duration) - 0.001, 3)
    return (start, end)


# --- captions -------------------------------------------------------------

def words_to_cues(words, max_words: int = 4, max_chars: int = 24,
                  gap: float = 0.6) -> list[dict]:
    """Group words into short caption cues (adapted from videofactory/render).

    A cue breaks on max_words, on max_chars, or on silence > gap. Cue end
    never overlaps the next cue's start; minimum cue duration is 0.2s.
    """
    groups, cur = [], []
    for w in words or []:
        text = str(w.get("text") or "").strip()
        if not text:
            continue
        if cur:
            joined = " ".join(c["text"] for c in cur) + " " + text
            too_long = len(cur) >= max_words or len(joined) > max_chars
            silent = float(w.get("start", 0.0)) - cur[-1]["end"] > gap
            if too_long or silent:
                groups.append(cur)
                cur = []
        cur.append({"text": text,
                    "start": float(w.get("start", 0.0)),
                    "end": float(w.get("end", 0.0))})
    if cur:
        groups.append(cur)

    out = []
    for i, group in enumerate(groups):
        start = group[0]["start"]
        end = max(group[-1]["end"], start + 0.2)       # min duration 0.2s
        if i + 1 < len(groups):
            nxt = groups[i + 1][0]["start"]
            if nxt > start:
                end = min(end, nxt)                    # never overlap next
        out.append({"start": start, "end": end,
                    "text": " ".join(c["text"] for c in group)})
    return out


def cues_to_srt(cues) -> str:
    """Standard SubRip: "N\\nHH:MM:SS,mmm --> HH:MM:SS,mmm\\ntext" blocks
    separated by a blank line."""
    blocks = []
    for i, c in enumerate(cues or [], 1):
        text = _words(c.get("text")).replace("\n", " ")
        blocks.append(f"{i}\n{ts(float(c['start']))} --> {ts(float(c['end']))}\n{text}")
    return "\n\n".join(blocks)


def clip_cues(cues, start: float, end: float) -> list[dict]:
    """Keep cues overlapping [start, end], clamp them to the window, then
    REBASE so the window begins at 0.0 — burned-in subtitles of a cut clip
    need clip-relative times. Cues fully outside, or that collapse to <= 0.05s,
    are dropped."""
    out = []
    for c in cues or []:
        cs, ce = float(c.get("start", 0.0)), float(c.get("end", 0.0))
        if ce <= start or cs >= end:            # no overlap with the window
            continue
        ns = max(cs, start) - start             # rebase to clip-relative time
        ne = min(ce, end) - start
        if ne - ns <= 0.05:
            continue
        out.append({"start": ns, "end": ne, "text": c.get("text", "")})
    return out


# --- ffmpeg argv ----------------------------------------------------------

def crop_cmd(src: str, start: float, end: float, out: str,
             srt_name: str | None = None, ffmpeg_bin: str = "ffmpeg") -> list[str]:
    """argv for cropping a 9:16 clip out of the source (never a shell string).

    The crop expression takes the largest even 9:16 box that fits BOTH
    landscape (min(iw, ih*9/16)) and portrait (min(ih, iw*16/9)) sources, the
    /2)*2 keeps dimensions even for x264, then scale pads to 1080x1920.
    srt_name is a bare filename ("clip.srt"): the caller runs ffmpeg with
    cwd = the job dir, so the subtitles filter needs no path escaping.
    """
    duration = float(end) - float(start)
    cmd = [ffmpeg_bin, "-y", "-hide_banner", "-loglevel", "error",
           "-ss", f"{start}", "-i", str(src), "-t", f"{duration}"]
    vf = ("crop='trunc(min(iw,ih*9/16)/2)*2':'trunc(min(ih,iw*16/9)/2)*2',"
          "scale=1080:1920,setsar=1")
    if srt_name:
        vf += f",subtitles={srt_name}"
    cmd += ["-vf", vf,
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
            str(out)]
    return cmd
