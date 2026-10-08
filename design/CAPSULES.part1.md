# CAPSULES — part 1 (letters A–E) — repurpose, Round 1 stage 1

Neutral concept capsules for `A.html`–`E.html`. One capsule per letter. Not for display
on any page.

## Direction A
- Premise: the app's purpose line is an arrow chain of four links (source → transcript →
  drafts → clip). The page sets that chain as four ascending type steps and files the
  app's own label and status vocabulary beneath it as a four-column monospaced index,
  the way an operator would list a job's fields, stages and states.
- Fonts: display = `Georgia, "Times New Roman", serif` (purpose steps); supporting +
  small = `"Courier New", Courier, monospace` (name, arrow markers, labels, statuses,
  notes, numerals). Source = local system fonts, installed with the OS; license = OS
  font license, nothing embedded or downloaded; fallback = generic `serif` / `monospace`
  at the end of each stack; no `@font-face`, no web fonts.
- Scale & case: mono base 13px / 1.7. Name 13px bold, 0.62em tracking, lowercase.
  Steps 1.5rem / 3rem / 5rem / 8rem, weight 400 except final link 700, line-height 1.06,
  each preceded by a mono arrow marker at 1rem with 0.2em tracking and 1.5rem right
  gap. Labels 11px bold, 0.24em, uppercase. Status words 15px lowercase. Stages
  12.5px, 0.16em, single line. Status sentences 12.5px / 1.8. Notes 12px / 1.8.
  Numerals 14.5px, 0.1em. Copy stays lowercase/sentence case; uppercase is reserved for
  the label index.
- Space: body padding 4rem 7vw 5rem; name margin-bottom 13vh; step gaps grow
  1.7rem → 2.2rem → 2.8rem with the type size; index block margin-top 20vh; four index
  columns `flex: 1 1 0` with 4vw gutters; label line-height 2.4–2.5, status line-height
  2.0–2.2, notes 1.8; no indents.
- Color: flat canvas `#F2EDE3` (100% of page, on `html`/`body` only); one text color
  `#17150E` for every word (100% of text). One-color system: 1 active letterform color.
- Signature: a single mono-to-serif ladder where the last link of the purpose chain is
  roughly five times the first, with the mono arrow marker repeating at the left of
  every link while the steps step down the page.
- Invariants: one text color only; four ascending purpose links with mono arrow
  markers; the four-column label/status/notes/numerals index; cream ground; mono name.
- Assumptions & risks: the 8rem final link may wrap or crowd the right margin on
  narrow viewports (no media query present); the leading arrow on the first link has no
  antecedent and reads as a marker; column counts in the index assume a wide page.
- Round 2: keep the chain-as-staircase and the mono arrow markers verbatim; scale the
  four steps proportionally rather than restyling them, and keep the index in four
  columns of the same vocabulary.

## Direction B
- Premise: the tool converts an ingested source into derived assets, and the app's own
  purpose line is cut by arrows. The page splits that line at its first arrow into two
  columns: what goes in (source fields, queue and stage words, ingest notes) sits
  right-aligned in the primary ink; what comes out (transcript, drafts, clip, copy and
  download actions) sits left-aligned in a second ink. The purpose line itself is
  severed across the gutter, one half heading each column.
- Fonts: single family throughout: `Helvetica, Arial, "Helvetica Neue", sans-serif` for
  display, supporting and small text; hierarchy carried only by size, weight and case.
  Source = local system font; license = OS font license; fallback = generic `sans-serif`;
  no `@font-face`, no web fonts.
- Scale & case: body 14px / 1.6. Name 12px bold, 0.58em, lowercase. Seam lines 40px
  regular, -0.015em, line-height 1.16. Asset headings 26px bold / 1.3. Status words
  19px bold / 1.5. Closing word 21px bold. Actions and status sentences 15px / 1.7.
  Labels 11px, 0.22em. Numerals 14.5px, 0.1em. Notes 12.5px / 1.8. Sentence case and
  lowercase throughout; no uppercase block.
- Space: body padding 6vh 7vw 7vh; name margin-bottom 9vh; split gutter 9vw; input
  column fixed at 32% width with `text-align: right`, output column takes the rest;
  stacked lists separated by 2.6rem; label line-height 2.35; status sentences spaced
  0.9rem; notes 1.1rem; numerals margin-top 1.2rem; closing word margin-top 3.4rem.
- Color: flat canvas `#FCFBF8` (100%); primary text `#14161A` — name, both seam
  halves' first line, entire input column, statuses, stage line, ingest note, closing
  word (≈ 55% of text); secondary text `#A6421C` — every derived-asset word: asset
  headings, actions, output notes, output numerals, second seam line (≈ 45%). Two-color
  system: 2 active letterform colors.
- Signature: the purpose line severed at its arrow and set as two headings on opposite
  sides of one gutter, with the whole input column right-aligned against the whole
  output column left-aligned — direction of travel carried by alignment and ink.
- Invariants: two inks with the input/output job split; right alignment only in the
  left column; single sans family; the severed purpose line at the top of both columns.
- Assumptions & risks: the 40px seam lines are the widest elements and may wrap at
  narrow widths, which would break the single-line sever; the fixed 32% input column
  depends on a wide viewport; no media query present.
- Round 2: preserve the give/get column split, the alignment opposition and the
  two-ink input/output mapping; do not unify the columns or rebalance them into a grid.

## Direction C
- Premise: a job passes through queued, running and done/failed. The page is one narrow
  column pushed far right, leaving the left of the canvas empty, and it groups the
  working copy by lifecycle: the waiting group, the running group and the settled
  group, each group in its own ink and each with its own leading and rhythm, stacked in
  the order the states occur. Interface labels follow as a tracked caps index.
- Fonts: display = `Palatino, "Book Antiqua", serif` (purpose line and the three
  lifecycle groups); supporting + small = `Arial, Helvetica, sans-serif` (name, caps
  index, notes, numerals). Source = local system fonts; license = OS font license;
  fallback = generic `serif` / `sans-serif`; no `@font-face`, no web fonts.
- Scale & case: body 14px / 1.6. Name 11px bold, 0.5em, lowercase. Purpose 30px
  serif / 1.32. Lifecycle lines 21px serif: waiting group italic at line-height 2.05,
  running group roman at 1.2 with 0.12rem item gaps, settled group roman at 1.55 with
  0.38rem item gaps. Caps index 10.5px bold, 0.28em, uppercase, line-height 2.5. Notes
  13px / 1.75 capped at 46ch. Numerals 15px, 0.08em, line-height 2.1.
- Space: body padding 9vh 8vw 12vh 44vw — a 44vw empty left field (10vw below 900px);
  name margin-bottom 3.5rem; purpose margin-bottom 3.4rem; group gaps 2.8rem, 2.8rem,
  3.2rem; index margin-bottom 2.6rem; notes 1rem apart; numerals margin-top 2.4rem;
  no indents inside groups.
- Color: flat canvas `#1A1512` (100%); primary `#EFE7D7` — name, purpose, settled
  group, caps index, notes, numerals (≈ 65% of text); secondary `#7FA9DC` — waiting
  group only (≈ 15%); tertiary `#E3A83B` — running group only (≈ 20%). Three-color
  system: 3 active letterform colors.
- Signature: lifecycle encoded as ink and rhythm in one column — cool italic waiting
  lines with wide leading, amber tight-leaded running lines, cream settled lines —
  ordered exactly as the job progresses.
- Invariants: three inks mapped to waiting / running / settled; the 44vw left void with
  the single right-offset column; serif lifecycle groups against the tracked sans caps
  index; italic waiting group.
- Assumptions & risks: color alone carries lifecycle meaning, so the mapping must be
  re-explained in any artifact that reuses it; the 44vw void is aggressive on narrow
  screens (handled only by one media query at 900px); group order must stay temporal.
- Round 2: keep the lifecycle-to-ink mapping, the group order and the right-offset
  column; re-typeset the same words rather than moving them into a list or table.

## Direction D
- Premise: the MVP produces four outputs from one source — transcript, LinkedIn draft,
  X thread, vertical clip. The page steps those four outputs down and to the right, one
  indent per output, and gives each output its own ink. The ink then reappears earlier
  in the page inside the purpose line and the stage list, so the platform colors are
  announced before the sections that carry them.
- Fonts: supporting + small = `Helvetica, Arial, "Helvetica Neue", sans-serif` (name,
  status block, section lines, footer); display = `"Times New Roman", Times, serif`
  bold (purpose line and section headings). Source = local system fonts; license = OS
  font license; fallback = generic `sans-serif` / `serif`; no `@font-face`, no web fonts.
- Scale & case: body 14px / 1.6. Name 12px bold, 0.58em, lowercase. Purpose 3.6rem
  serif bold, line-height 1.08. Status block 13px, 0.16em, line-height 2.3, one state
  per line. Section headings 34px serif bold, 0.05em, uppercase. Section lines
  13.5px / 1.8; numeral lines 15px, 0.08em. Footer tag 11px bold, 0.24em, uppercase,
  line-height 2.4; footer sentences 12.5px / 1.85 capped at 62ch; footer numerals
  14.5px, 0.08em.
- Space: body padding 5rem 7vw 6rem; name and purpose each margin-bottom 6vh; status
  block margin-bottom 8vh; section indents 0, 9vw, 18vw, 27vw with each section capped
  at 42ch and spaced 4.6rem; heading-to-line gap 0.65rem; line gap 0.5rem; footer
  margin-top 9vh with 0.9rem between paragraphs.
- Color: flat canvas `#EAEDF0` (100%); primary `#1B1C20` — name, purpose remainder,
  full status block, transcript section, footer text (≈ 55% of text); secondary
  `#2A5DB0` — LinkedIn role: the LinkedIn token in the purpose line, the LinkedIn
  heading and its lines (≈ 12%); tertiary `#6D3FA0` — X role: the X token in the
  purpose line, the X heading and its lines (≈ 12%); accent `#B33A1B` — video role:
  "9:16 clip" in the purpose line, "clip" in the stage line, the video heading, its
  lines and its numeral (≈ 21%). Four-color system: 4 active letterform colors.
- Signature: a four-step staircase of outputs where each step's ink is already present
  in the sentence and stage line above, so platform identity is read twice — first in
  the purpose line, then in the section that carries it.
- Invariants: four inks with the transcript/LinkedIn/X/video job split; the 0 → 9vw →
  18vw → 27vw indent order; uppercase serif headings; the ink re-occurrence between
  purpose line, stage line and sections.
- Assumptions & risks: the deepest indent plus 42ch measure assumes a wide viewport;
  four inks must stay assigned to platforms and never become emphasis tools; the
  footer tag line runs labels as one continuous string and depends on wrapping to stay
  legible.
- Round 2: keep the platform-to-ink map and the staircase indents exactly; new text
  must be assigned to an existing platform ink rather than introducing a fifth color.

## Direction E
- Premise: the transcript is the first derived asset and it is read line by line as a
  running column. The whole copy is set in vertical writing mode so it reads top to
  bottom, with columns advancing right to left across the page, and the column gaps are
  sized by the role of each block: name, purpose line, body copy, numerals.
- Fonts: single family throughout: `Georgia, "Times New Roman", serif` for display,
  supporting and small text. Source = local system font; license = OS font license;
  fallback = generic `serif`; no `@font-face`, no web fonts.
- Scale & case: body 16px / 1.95 with `writing-mode: vertical-rl`. Name 24px bold,
  0.34em tracking, line-height 1.6. Purpose line 30px, line-height 1.75. Body blocks
  16px / 1.95. Numerals block 19px, 0.06em, line-height 1.9. Below 1000px: body 14px /
  1.9, name 21px, purpose 26px / 1.7, body 14px, numerals 17px. Sentence case and
  lowercase throughout; no uppercase block.
- Space: body padding 7vh 12vw, height 86vh (88vh and 6vh/10vw padding below 1000px);
  `main` margin-left 3rem; block margin-left 3.4rem (name), 3.2rem (purpose), 2.6rem
  (body blocks) act as the gaps between successive columns; no indents inside blocks;
  numerals block carries no extra margin.
- Color: flat canvas `#20423B` (100%); one text color `#EDE7D6` for every word
  (100% of text). One-color system: 1 active letterform color.
- Signature: the entire copy chain running vertically — name, purpose line, four body
  blocks and numerals as successive columns — with column gaps shrinking from name to
  body so reading position is set by spacing alone.
- Invariants: single ink; `writing-mode: vertical-rl`; serif throughout; the 86vh
  column height; role-based column gaps (3.4rem / 3.2rem / 2.6rem); the step-down
  scale below 1000px.
- Assumptions & risks: vertical flow can overflow the page width at long copy lengths,
  where cropping at the left edge is the expected behavior; mixed-direction tokens in
  the copy (arrows, "9:16", "·") need source-level checking against the vertical
  reading order; no uppercase or accent role exists in this direction.
- Round 2: keep the vertical reading direction, the single ink and the role-based
  column gaps; extend by adding columns, never by rotating individual blocks back to
  horizontal.
