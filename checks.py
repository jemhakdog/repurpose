"""repurpose self-check: uv run python checks.py  (exit 0 = pass)"""
import pathlib
import re
import sys

import pipeline

fails = 0


def ok(cond, msg):
    global fails
    if cond:
        print(f"  ok: {msg}")
    else:
        fails += 1
        print(f"FAIL: {msg}")


def seg(start, end, text):
    """Build a transcript segment with evenly spread word timings."""
    ws = text.split()
    step = (end - start) / max(1, len(ws))
    return {"start": start, "end": end, "text": text,
            "words": [{"text": w, "start": start + i * step,
                       "end": start + (i + 1) * step}
                      for i, w in enumerate(ws)]}


PLAIN = "we talked about the plan for the quarter in some detail today"   # 12w, no digits
DIGITS = "we shipped 47 units in two days to the north region"            # 11w, 1 digit

print("[1] score_segment")
s_intro = pipeline.score_segment(seg(0, 4, PLAIN), 0, 20)
s_mid = pipeline.score_segment(seg(40, 44, PLAIN), 10, 20)
s_outro = pipeline.score_segment(seg(80, 84, PLAIN), 19, 20)
ok(s_intro < s_mid, f"intro scores below middle segment ({s_intro} < {s_mid})")
ok(s_outro < s_mid, f"outro scores below middle segment ({s_outro} < {s_mid})")
s_digits = pipeline.score_segment(seg(44, 48, DIGITS), 11, 20)
ok(s_digits > s_mid, f"digits beat filler ({s_digits} > {s_mid})")
s_money = pipeline.score_segment(seg(48, 52, "does 5% growth beat $2 a share?"), 12, 20)
ok(s_money > s_digits, f"$ / % / ? add on top of digits ({s_money} > {s_digits})")
s_two = pipeline.score_segment(seg(52, 53, "um ok"), 13, 20)
ok(s_two < 0.01, f"2-word segment scores near 0 (got {s_two})")
ok(pipeline.score_segment(seg(40, 44, PLAIN), 10, 20) == s_mid, "deterministic (same input -> same float)")
ok(pipeline.score_segment(dict(seg(40, 44, PLAIN)), 10, 20) == s_mid, "deterministic across fresh dicts")

print("[2] top_sentences")
texts2 = [PLAIN] * 10
texts2[3] = DIGITS                                                    # 1.5 (idx 3)
texts2[5] = "we hold 12 meetings every week with the design guild"    # 1.5 (idx 5, tie)
texts2[7] = "did 47 units at $2 each hit 98% of the goal in week 3?"  # 2.4 (idx 7)
segs2 = [seg(i * 4, i * 4 + 4, t) for i, t in enumerate(texts2)]
idx_of = {t: i for i, t in enumerate(texts2)}
top3 = pipeline.top_sentences(segs2, 3)
win3 = [s["text"] for s in top3]
ok(win3 == [texts2[3], texts2[5], texts2[7]],
   f"top3 = highest scores, ties by index asc (got {win3})")
ok([idx_of[t] for t in win3] == sorted(idx_of[t] for t in win3),
   "winners returned in ORIGINAL order")
ok(len(pipeline.top_sentences(segs2, 2)) == 2, "respects n=2")
ok([s["text"] for s in pipeline.top_sentences(segs2, 2)] == [texts2[3], texts2[7]],
   "n=2 tie broken by lower index (idx 3 over idx 5)")
ok(len(pipeline.top_sentences(segs2)) == 5, "default n=5")
ok(len(pipeline.top_sentences(segs2, 99)) == 10, "n > len is safe")
ok(pipeline.top_sentences([], 5) == [], "empty -> []")
ok(pipeline.top_sentences(segs2, 0) == [], "n=0 -> []")

print("[3] linkedin_post")
ok(pipeline.linkedin_post("", []) != "", "no segments, no title -> non-empty fallback")
ok(pipeline.linkedin_post("My Title", []) != "", "no segments -> non-empty fallback")
TITLE = "AI Growth Playbook 2024"
texts20 = [f"segment {i} covers a distinct idea about growth and planning for the team"
           for i in range(20)]
texts20[10] = "we grew 37% to $1.2M across 15 markets in 2024 with just 9 people"
segs20 = [seg(i * 4, i * 4 + 4, t) for i, t in enumerate(texts20)]
post = pipeline.linkedin_post(TITLE, segs20)
lines = post.split("\n")
bullets = [l for l in lines if l.startswith("- ")]
ok(post.strip() != "", "non-empty post")
ok(texts20[10] in post, "contains the hook (top segment text)")
ok(len(bullets) == 3, f"exactly 3 '- ' bullets (got {len(bullets)})")
ok(len(set(bullets)) == 3, "bullets come from 3 distinct segments")
ok("3 takeaways:" in post, "has the '3 takeaways:' header")
ok(any(l.startswith("#") for l in lines), f"has the hashtag line ({[l for l in lines if l.startswith('#')]})")
ok("#Growth" in post and "#Playbook" in post, "hashtags title-cased from title words")
ok("What's your take on AI Growth Playbook 2024?" in post, "closing line references title")
long40 = " ".join(f"word{i}" for i in range(40))
segs60 = [seg(i * 2, i * 2 + 2, long40) for i in range(60)]
post60 = pipeline.linkedin_post(TITLE, segs60)
ok(post60 != "", "60 x 40-word input -> non-empty")
ok(len(post60) <= 1300, f"<= 1300 chars on 60-segment 40-word input (got {len(post60)})")
ok(all(len(l) <= 202 for l in post60.split("\n")),
   "hook and bullets trimmed on word boundaries (<= 200 chars)")

print("[4] twitter_thread")
ok(pipeline.twitter_thread("", []) != "", "no segments -> non-empty generic tweet")
ok(pipeline.twitter_thread("T", []) != "", "no segments -> non-empty")
thread = pipeline.twitter_thread(TITLE, segs20)
tweets = thread.split("\n\n")
ok(thread != "", "non-empty thread")
ok(2 <= len(tweets) <= 6, f"2..6 tweets (got {len(tweets)})")
ok(all(len(t) <= 280 for t in tweets),
   f"every tweet <= 280 incl. counter (max {max(len(t) for t in tweets)})")
ok(all(re.match(r"^\d+/\d+ ", t) for t in tweets), "every tweet starts with i/total counter")
ok(texts20[10] in tweets[0], "first tweet carries the hook")
ok("AI Growth Playbook 2024" in tweets[-1], "final tweet is a CTA referencing the title")
ok(pipeline.twitter_thread("", segs20).split("\n\n")[-1].find("AI Growth") == -1,
   "empty title -> generic CTA")
t3 = pipeline.twitter_thread(TITLE, segs20, 3).split("\n\n")
ok(len(t3) == 3 and all(len(t) <= 280 for t in t3), "n=3 respected, all <= 280")
t_long = pipeline.twitter_thread(TITLE, [seg(0, 4, long40)]).split("\n\n")
ok(len(t_long) == 2 and all(len(t) <= 280 for t in t_long),
   f"long hook trimmed to <= 280 by dropping trailing words (got {[len(t) for t in t_long]})")

print("[5] pick_highlight (clip crop math)")
ok(pipeline.pick_highlight(segs20, 20) == (0.0, 20.0), "duration <= length -> (0, duration)")
ok(pipeline.pick_highlight(segs20, 30) == (0.0, 30.0), "duration == length -> (0, duration)")
ok(pipeline.pick_highlight([], 120) == (0.0, 30.0), "no segments -> (0, min(length, duration))")
ok(pipeline.pick_highlight([], 12) == (0.0, 12.0), "no segments, duration < length -> (0, 12)")
short = [seg(0, 10, PLAIN), seg(10, 20, DIGITS)]
ok(pipeline.pick_highlight(short, 0, 30) == (0.0, 20.0), "duration<=0 -> duration from last segment end")
ok(pipeline.pick_highlight(short, -5) == (0.0, 20.0), "negative duration -> last segment end")
# synthetic 120s transcript: only segments 15..22 (60s-92s) are number-heavy
REGION = ("in 2024 we grew revenue 37% to $1.2 million across 15 markets "
          "and hired 42 engineers for 9 product teams")
big = [seg(i * 4.0, i * 4.0 + 4.0, REGION if 15 <= i <= 22 else "um ok yes")
       for i in range(30)]
s, e = pipeline.pick_highlight(big, 120.0, 30.0)
ok(s >= 0, f"start never negative (got {s})")
ok(e <= 120.0 + 1e-9, f"end never past duration (got {e})")
ok(s < e, f"start < end (got {s} < {e})")
ok(e - s <= 30.0 + 1e-9, f"window <= length (got {round(e - s, 3)})")
ok(60.0 <= s < 90.0, f"start lands inside the number-heavy 60-90s region (got {s})")
ok(pipeline.pick_highlight(big, 0.0) == pipeline.pick_highlight(big, 120.0),
   "duration<=0 on the long transcript -> duration from last segment end (120)")
ok(all(isinstance(v, float) for v in (s, e)), "returns floats")

print("[6] clip_cues")
cues6 = [{"start": 100.0, "end": 101.0, "text": "before"},
         {"start": 125.0, "end": 126.0, "text": "inside"},
         {"start": 145.0, "end": 155.0, "text": "straddle"},
         {"start": 155.0, "end": 160.0, "text": "after"},
         {"start": 130.0, "end": 130.04, "text": "tiny"}]
got = pipeline.clip_cues(cues6, 120.0, 150.0)
inside = [c for c in got if c["text"] == "inside"]
ok(len(inside) == 1 and inside[0]["start"] == 5.0 and inside[0]["end"] == 6.0,
   f"125-126 in window (120,150) rebases to (5,6) (got {inside})")
ok(not any(c["text"] == "before" for c in got), "cue entirely before window dropped")
ok(not any(c["text"] == "after" for c in got), "cue entirely after window dropped")
ok(not any(c["text"] == "tiny" for c in got), "cue collapsing to <= 0.05s dropped")
strad = [c for c in got if c["text"] == "straddle"]
ok(len(strad) == 1 and strad[0]["start"] == 25.0 and strad[0]["end"] == 30.0,
   f"straddling cue clamps to the window edge (got {strad})")
ok(all(c["start"] >= 0 for c in got), "all output starts >= 0")
ok(all(c["end"] <= 30.0 + 1e-6 for c in got), "all ends <= window length + 1e-6")

print("[7] cues_to_srt (+ words_to_cues)")
srt = pipeline.cues_to_srt([{"start": 5.0, "end": 6.0, "text": "hello world"}])
ok(srt == "1\n00:00:05,000 --> 00:00:06,000\nhello world",
   f"exact format (got {srt!r})")
srt2 = pipeline.cues_to_srt([{"start": 0.0, "end": 1.0, "text": "a"},
                             {"start": 1.5, "end": 2.5, "text": "b"}])
ok(srt2.split("\n\n")[1] == "2\n00:00:01,500 --> 00:00:02,500\nb", "second block numbered")
ws = [{"text": f"w{i}", "start": i * 0.3, "end": i * 0.3 + 0.25} for i in range(10)]
cues = pipeline.words_to_cues(ws)
ok(cues[0]["text"] == "w0 w1 w2 w3", f"breaks at max_words=4 (got {cues[0]['text']!r})")
ok(len(cues) == 3, f"10 words -> 3 cues (got {len(cues)})")
ok(all(cues[i]["end"] <= cues[i + 1]["start"] + 1e-9 for i in range(len(cues) - 1)),
   "cue end never overlaps next cue start")
ok(all(c["end"] - c["start"] >= 0.2 - 1e-9 for c in cues), "min cue duration 0.2s")

print("[8] crop_cmd")
cmd = pipeline.crop_cmd("in.mp4", 12.5, 42.5, "out.mp4")
ok(isinstance(cmd, list) and all(isinstance(x, str) for x in cmd), "returns a list of str")
ok(cmd[0] == "ffmpeg" and cmd[1:4] == ["-y", "-hide_banner", "-loglevel"],
   "quiet flags up front")
ok(cmd.index("-ss") < cmd.index("-i"), "-ss appears BEFORE -i")
ok(float(cmd[cmd.index("-ss") + 1]) == 12.5, "-ss value is the start")
ok(abs(float(cmd[cmd.index("-t") + 1]) - 30.0) < 1e-9, "-t is end-start")
vf = cmd[cmd.index("-vf") + 1]
ok("crop=" in vf and "9/16" in vf and "16/9" in vf,
   f"9:16 crop for landscape and portrait (got {vf!r})")
ok("scale=1080:1920" in vf and "setsar=1" in vf, "scale=1080:1920 + setsar=1")
ok(not any("subtitles=" in x for x in cmd), "no subtitles filter when srt_name omitted")
ok(cmd[-1] == "out.mp4", "output path is the last element")
cmd2 = pipeline.crop_cmd("in.mp4", 0, 10, "o.mp4", srt_name="clip.srt")
ok(any("subtitles=clip.srt" in x for x in cmd2), "subtitles=clip.srt when srt_name given")
ok("libx264" in cmd and "yuv420p" in cmd and "+faststart" in cmd, "x264 / yuv420p / faststart")
ok(pipeline.crop_cmd("in.mp4", 0, 1, "o.mp4", ffmpeg_bin="/usr/bin/ffmpeg")[0] == "/usr/bin/ffmpeg",
   "ffmpeg_bin honoured")

print("[9] no hardcoded credentials")
bad = []
for f in pathlib.Path(__file__).parent.glob("*.py"):
    if f.name == "checks.py":  # this file contains the literals on purpose
        continue
    for i, line in enumerate(f.read_text(encoding="utf8").splitlines(), 1):
        if "sk-" in line or "Authorization: Bearer" in line:
            bad.append(f"{f.name}:{i}")
ok(not bad, f"no keys in source ({bad})")

print()
sys.exit(1 if fails else 0)
