# CAPSULES — part 2 (letters F–J) — repurpose, Round 1 stage 2

Neutral concept capsules for `F.html`–`J.html`. One capsule per letter. Not for display
on any page.

## Direction F
- Premise: the MVP objective caps the source at 15 minutes and returns one 30-second
  clip. The page sets those two supplied durations as the poles of a single scale: the
  source duration is set so large it runs past the right edge of the page and is cropped
  there, the clip duration sits directly beneath it at a small fraction of that size and
  stays inside the page, and the app's whole label/status/notes vocabulary is filed small
  below both.
- Fonts: display = `Georgia, "Times New Roman", serif` (purpose line, both duration
  poles, notes, closing word); supporting = `Helvetica, Arial, sans-serif` (status
  sentences); small = `"Courier New", Courier, monospace` (name, clip-length label,
  label/stage/numeral runs). Source = local system fonts; license = OS font license,
  nothing embedded or downloaded; fallback = generic `serif` / `sans-serif` /
  `monospace` at the end of each stack; no `@font-face`, no web fonts.
- Scale & case: body 14px / 1.6. Name 13px bold, 0.62em tracking, lowercase. Purpose
  1.7rem / 1.34, max 30ch. Source pole 21vw, line-height 0.9, tracking −0.02em,
  `white-space: nowrap` so the line crops at the page edge. Clip label 11px, 0.24em.
  Clip pole 4.2rem, line-height 1. Label and stage runs 12px mono, 0.18em, line-height
  2.35. Status sentences 15px / 1.9. Notes 14.5px serif / 1.85, max 47ch. Closing word
  2.2rem serif. Sentence case and lowercase throughout; no uppercase block.
- Space: body padding 4.5rem 6vw 6rem; name margin-bottom 6vh; purpose margin-bottom
  8vh; clip label margin-top 7vh with 0.7rem to the clip pole; filed block margin-top
  15vh, measure 47ch, 2.2rem between paragraphs; `html` and `body` carry
  `overflow-x: hidden` so the oversized source line is cropped at the page edge; no
  indents.
- Color: flat canvas `#0F1215` (100% of page, on `html`/`body` only); one text color
  `#E9E4D6` for every word (100% of text). One-color system: 1 active letterform color.
- Signature: a 21vw source duration cropped by the right page edge sitting directly above
  a 4.2rem clip duration — magnitude compression carried by size and cropping in one ink.
- Invariants: single ink; the two duration poles and their size relationship; the
  nowrap source line cropped at the right edge; the small 47ch vocabulary block; the
  near-black canvas.
- Assumptions & risks: the crop depends on `overflow-x: hidden` staying in place —
  without it the page gains horizontal scroll; at very narrow viewports 21vw shrinks the
  pole and the crop may disappear; no media query present; the serif poles against sans
  and mono carry most of the hierarchy, so removing any one family flattens it.
- Round 2: keep the source/clip size relationship and the right-edge crop verbatim;
  scale both poles together rather than restyling either, and keep the vocabulary block
  small, flush left and single-ink.

## Direction G
- Premise: the ingest note says a file or a URL works and to leave one blank if you use
  the other. The page takes that rule as its layout: the copy descends in blocks that
  alternate between a left rail and a right rail, each block 42% wide, so every filled
  block faces an empty half — the blank the copy asks for is kept, page after page, and
  each rail carries its own ink.
- Fonts: single family for all copy: `Helvetica, Arial, "Helvetica Neue", sans-serif`;
  the name line only in `"Courier New", Courier, monospace`. Source = local system fonts;
  license = OS font license; fallback = generic `sans-serif` / `monospace`; no
  `@font-face`, no web fonts.
- Scale & case: body 14px / 1.6. Name 12px bold, 0.58em, lowercase. Purpose 1.95rem /
  1.24, max 24ch. Block openers 1.55rem bold / 1.26. Label runs 11px, 0.22em,
  line-height 2.3, kept in their own Title Case (no case transforms). Stage runs 15px /
  1.95. Status sentences 16px / 1.7. Notes 12.5px / 1.85, max 40ch. Figures 14.5px,
  0.08em, line-height 2.1. Sentence case and lowercase for all running copy.
- Space: body padding 7vh 7vw 9vh; every block `width: 42%`, `min-height: 10.5rem`,
  4.5rem below the previous block; rail A at `margin-left: 0`, rail B at
  `margin-left: 50%`; paragraphs inside a block 1.4rem apart; no indents inside blocks.
  The 10.5rem minimum keeps a full empty half opposite short blocks.
- Color: flat canvas `#F0E7E3` (100%); primary `#1A1714` — rail A blocks: name,
  purpose line, the `YouTube URL` block, the asset/action label run with the tweet note,
  and the counter block (≈ 50% of text); secondary `#22458C` — rail B blocks: `Repurpose`
  with the list labels, `…or upload a file` with the ingest note, the status/stage and
  status-sentence block, and the settings labels with the figures and no-clip note
  (≈ 50%). Two-color system: 2 active letterform colors.
- Signature: alternating filled and empty halves down the page — the same copy stepping
  between two rails while the opposite position stays blank, the "leave one blank" rule
  made structural.
- Invariants: two inks bound to rails; 42% blocks alternating between 0 and 50%
  left margin; the 10.5rem minimum blank band; single sans family with the mono name;
  the left-to-right reading zigzag.
- Assumptions & risks: the rails are positional, not semantic, and must not be re-read as
  an input/output split; at narrow widths 42% measures become very small (no media query
  present); the blanks are perceived only while the block width and minimum height hold.
- Round 2: keep the alternation, the block width and the honored blanks; new copy joins
  the sequence at the next rail rather than widening an existing block or filling the
  empty half.

## Direction H
- Premise: the pipeline crops footage to 9:16 and hands back text drafts plus a video
  download. The page is set inside one centered column whose width is 9:16 of the
  intended type block, with wide empty ground on both sides, and three inks mark what the
  copy is made of: the frame and queue vocabulary, the text drafts, and the video asset.
- Fonts: display = `Georgia, "Times New Roman", serif` (purpose line, asset headings,
  status sentences); supporting = `Helvetica, Arial, sans-serif` (labels, actions,
  states, notes, figures); small = `"Courier New", Courier, monospace` (name, counter
  line). Source = local system fonts; license = OS font license; fallback = generic
  `serif` / `sans-serif` / `monospace`; no `@font-face`, no web fonts.
- Scale & case: body 14.5px / 1.75. Name 12px bold, 0.55em, lowercase. Purpose 1.5rem
  serif / 1.32. Action word 1.05rem bold, 0.24em. Label runs 10.5px, 0.2em,
  line-height 2.5. Asset headings 2rem serif / 1.16, one per line. Action words 12.5px,
  0.16em, line-height 2.2. Stage run 13.5px, 0.1em, line-height 2.1. Status sentences
  15px serif / 1.7, one per paragraph. Counter 13px mono, 0.14em. Notes 12.5px / 1.8.
  Figures 15px, 0.06em, line-height 2.2. Sentence case and lowercase; no case transforms.
- Space: body padding 7vh 0 9vh; `main` width `48vh` (9:16 of the intended 86vh type
  block), `max-width: 92vw`, `margin: 0 auto`; name margin-bottom 4vh; purpose
  margin-bottom 4.5vh; action word margin-bottom 5vh; first label run to first asset
  3.6vh; `clip length` label margin-bottom 5vh; stage run margin-bottom 4vh; sentences
  1rem apart; counter margin-bottom 4vh; notes 1.6rem apart; no indents.
- Color: flat canvas `#E4E7E2` (100%); primary `#171A18` — name, purpose, `Repurpose`,
  both label runs, stage and status run, all status sentences, counter, ingest note,
  most figures (≈ 60% of text); secondary `#0E6B5E` — `Transcript`, `LinkedIn draft`,
  `X thread`, `Save`, `Copy`, the tweet note and `No clip generated`'s counterpart
  `No transcript segments.` (≈ 22%); tertiary `#B21E2F` — `Video`, `Download clip`,
  `Download .srt`, `clip length`, `No clip generated for this job.` and `30-second`
  (≈ 18%). Three-color system: 3 active letterform colors.
- Signature: one narrow centered column whose ink switches by asset class — three text
  drafts in one color, the video line and its actions in another, everything else in the
  frame ink — so position in the pipeline is read from color alone inside the crop.
- Invariants: the three inks mapped to frame / text drafts / video; the centered 48vh
  column; asset headings at 2rem in their own ink; serif purpose and status sentences;
  no color used for emphasis inside a role.
- Assumptions & risks: the 48vh column assumes the copy fits the intended block height;
  if it runs long the 9:16 relationship weakens (only `max-width: 92vw` guards narrow
  screens, no media query); the roles are asset classes and must not drift into platform
  or state meanings.
- Round 2: keep the three-role ink map, the centered crop width and the asset-heading
  size; new text joins an existing role rather than introducing a fourth color.

## Direction I
- Premise: the app's copy arrives in registers — interface labels, job states and
  stages, the app's own prose, and its figures. The page typesets them as parts of
  speech: each register owns one ink everywhere it occurs, so color alone groups the
  page and no group headings are printed at all.
- Fonts: display = `Georgia, "Times New Roman", serif` (purpose line); supporting =
  `Helvetica, Arial, sans-serif` (name, label run, state runs, notes, closing word);
  small = `"Courier New", Courier, monospace` (counter line and figures). Source = local
  system fonts; license = OS font license; fallback = generic `serif` / `sans-serif` /
  `monospace`; no `@font-face`, no web fonts.
- Scale & case: body 16.5px / 1.75. Name 13px bold, 0.6em, lowercase. Purpose 2.5rem
  serif / 1.16, max 30ch. Label run 11.5px, 0.2em, line-height 2.45, max 52ch, kept in
  its own Title Case. Stage run 15.5px / 2.0, max 54ch. Status-word run 15.5px / 2.0,
  max 54ch. Notes at body size / 1.75, max 58ch, 1.7rem apart. Counter 1.25rem mono,
  0.1em. Figures 1.35rem mono / 1.95, one per line. Closing word 1.6rem bold, 0.26em.
  Sentence case and lowercase throughout; no case transforms.
- Space: body padding 8vh 10vw 9vh; name margin-bottom 4.5vh; purpose margin-bottom 6vh;
  label run, state runs and counter each 4.5rem apart; notes 1.7rem apart; figures
  margin-top 3.5rem; closing word margin-top 5rem; four different measures — 30ch, 52ch,
  54ch, 58ch — set by register, not by column; no indents.
- Color: flat canvas `#EBE6DA` (100%); primary `#15130F` — name, purpose, the four
  notes, closing word (≈ 45% of text); secondary `#7A2E86` — the single label run
  covering all interface labels (≈ 20%); tertiary `#0E5F70` — the stage run and the
  status-word run (≈ 25%); accent `#8A5205` — the counter line and the figures block
  (≈ 10%). Four-color system: 4 active letterform colors.
- Signature: a page with no headings where every interface label is violet, every job
  state petrol, every figure amber and the app's prose black — the vocabulary typeset as
  grammar, register readable before meaning.
- Invariants: four inks with those four jobs; the absence of group headings; the four
  register measures; serif purpose line against mono figures; canvas value.
- Assumptions & risks: the register map must be re-explained wherever it is reused; the
  accent role sits in two blocks (counter and figures), so it depends on those staying
  mid and lower page to hold its share; a new word colored for emphasis alone would break
  the system.
- Round 2: assign every new string to an existing register; never highlight an isolated
  word, and never add a fifth color to signal something the registers already cover.

## Direction J
- Premise: the status line `[n] jobs · [n] pending` is the one string the app re-reads
  continuously while everything else is written once. The page repeats that line alone in
  its own band at an equal 11vh lead-in between blocks of the remaining copy, so the
  counter keeps coming back down the page while the rest passes between its
  occurrences — all of it in one ink.
- Fonts: small/machine text = `"Courier New", Courier, monospace` (name, refrain line,
  figures); display and reading text = `Georgia, "Times New Roman", serif` (purpose
  line, status sentences, notes); supporting = `Helvetica, Arial, sans-serif` (label run,
  stage run, closing word). Source = local system fonts; license = OS font license;
  fallback = generic `monospace` / `serif` / `sans-serif`; no `@font-face`, no web fonts.
- Scale & case: body 15px / 1.7. Name 12px bold, 0.6em, lowercase. Purpose 1.9rem serif
  / 1.3, max 30ch. Refrain 1.55rem mono, 0.16em, `text-align: center`, alone in its
  band. Label run 11.5px, 0.2em, line-height 2.4, max 50ch. Stage run 15px / 2.0. Status
  sentences 17px serif / 1.7. Notes 14.5px serif / 1.85, max 55ch. Figures 1.2rem mono,
  0.1em, line-height 2.0. Closing word 1.5rem bold, 0.3em. Sentence case and lowercase;
  no case transforms.
- Space: body padding 6vh 8vw 8vh; purpose line then first refrain; each refrain
  `margin-top: 11vh`; each block `margin-top: 3.4rem`, `min-height: 24vh`, paragraphs
  1.6rem apart; closing word margin-top 3rem inside the last block; refrain lines centered
  on the page, all block copy flush left; no indents.
- Color: flat canvas `#101B2E` (100%); one text color `#E8E9E4` for every word (100% of
  text). One-color system: 1 active letterform color.
- Signature: the counter line repeated four times, centered and alone in a band at equal
  lead-ins, while every other supplied line sits flush left in the bands between —
  repetition and interval carrying the reading order without a second color.
- Invariants: single ink; four refrain occurrences with the 11vh lead-in and 24vh band
  minimum; centered refrain against left-set blocks; mono refrain, serif sentences; the
  navy canvas.
- Assumptions & risks: the even interval depends on blocks staying under 24vh — if a
  block grows the rhythm drifts (no media query present); the fixed interval is a
  spacing promise, so restyling block sizes silently breaks it; the direction has no
  accent or secondary role at all.
- Round 2: keep the refrain's wording, count, centered position and fixed lead-in; add
  copy inside bands rather than between a refrain and its band, and never color the
  refrain differently from the rest.
