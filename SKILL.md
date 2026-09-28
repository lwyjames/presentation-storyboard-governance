---
name: presentation-storyboard-governance
description: Create and govern a presentation storyboard in one stable-ID Storyboard_Manifest.md, from page-by-page draft through user approval to deck production; bind PPT slides through speaker-note IDs, and audit or revise decks without relying on page numbers. Use for draft or approved keynote storyboards and for creating, updating, reordering, migrating, or validating decks against them. Do not use for a standalone slide task without a storyboard.
---

# Presentation Storyboard Governance

Treat `Storyboard_Manifest.md` as the single working storyboard file. Its `draft` status supports review and revision; its `approved` status is the contract for derived presentations. `source_of_truth: true` identifies the canonical file, not user approval.

## Non-negotiable invariants

- Identify a slide only by its stable semantic `slide_id`.
- Treat `order` as mutable and page number as derived. Never join storyboard and PPT by page number.
- Embed `STORYBOARD_ID: <slide_id>` in each PPT slide's speaker notes.
- Use titles only to locate legacy candidates; a title is not a primary key.
- Never reconstruct, overwrite, or “improve” an approved storyboard from the PPT.
- Do not produce a storyboard-controlled deck from a draft Manifest. Obtain user approval of a specific revision, record it, then change the document and retained slide statuses to `approved`.
- Preserve approved wording and visual requirements. Do not fill omissions with assumptions.
- Do not alter `locked: true` content without an explicit user instruction.
- Record only video and official-site URLs explicitly designated by the user; never substitute a similar video or silently broaden the source set.

## User-designated visual and factual sources

- Put a `## 用户指定来源` register before slide entries in every new manifest. Give each designated video and official-site URL a stable `source_id` and document its purpose. Write `未指定` for a missing category rather than inventing a URL.
- Use designated videos to find frames supporting specific slide arguments. For each saved frame, record source ID, timestamp, visible subject, target `slide_id`, and saved asset path. Distinguish planned captures from saved assets.
- Use designated official pages for product imagery and for checking storyboard facts. Revise approved content only when the user's instruction permits it and the correction is grounded in the designated page; record the evidence and increment each affected slide's `revision`.
- Reference source IDs in relevant slides' `视觉设计` or `可用来源`. Carry image attribution into later PPT notes or the project asset register.

## Choose the workflow

### Create and revise a draft in the same Manifest

1. Read [references/manifest-schema.md](references/manifest-schema.md). Create `Storyboard_Manifest.md` with document and slide statuses `draft`, a provisional version, `effective_date: "未批准"`, and the user-designated sources. The project ID and semantic slide IDs may be assigned now; refine draft IDs if the underlying meaning changes before approval.
2. Preserve user-specified core questions and approximate pages per question. Write each page's core expression, content, visual intent, and evidence in the manifest body. Summarize in chat and provide the actual Markdown file for review. Do not create a second standalone Storyboard draft.
3. Apply feedback to this same file, increment its draft version, and run structural validation. Keep an explicit record of which revision the user approved.
4. On approval, mark the document and retained slides `approved`, fill `effective_date` and `source_reference` with the user-approved revision, and freeze the semantic IDs. Run validation with `--require-approved` before handing the Manifest to Presentations.

### Convert an approved storyboard

1. Read only the user-designated approved source. If it is DOCX, use the Documents skill for extraction and inspection.
2. Ignore the current PPT as a content source. It may be used later only for comparison.
3. Read [references/manifest-schema.md](references/manifest-schema.md), create `Storyboard_Manifest.md`, and assign stable semantic IDs.
4. Keep original content under its original semantic labels such as `核心表达`, `页面内容`, and `视觉设计`. Record source page numbers only as provenance.
5. Register user-designated video and official-site URLs with their visual and factual-review purposes, and attach source IDs to relevant slides.
6. Mark pre-finalized or externally supplied pages as locked when the source says they should be skipped or preserved.
7. Run `scripts/validate_storyboard_manifest.py --require-approved` and resolve every error before deck production.

### Create or revise a PPT from the manifest

1. Load the Presentations skill and validate the manifest with `--require-approved` first.
2. Sort slides by `order`; derive display page numbers after sorting.
3. Match an existing PPT slide by speaker-note `STORYBOARD_ID` only.
4. Implement the manifest's core expression, page content, and visual design as separate acceptance criteria. Check referenced visuals against the user-designated source register and preserve attribution. A correct title alone is not sufficient.
5. Write or preserve the exact `STORYBOARD_ID` marker in speaker notes.
6. Revalidate the complete ID map and render the affected slides for visual QA.

### Audit or migrate a legacy PPT

Read [references/audit-contract.md](references/audit-contract.md). First inventory PPT titles, notes IDs, and order; then compare against the manifest.

- Exact notes ID: authoritative match.
- Missing notes ID: use exact title plus core-expression and visual-structure evidence to propose a candidate.
- Duplicate, conflicting, or ambiguous candidate: stop and ask for confirmation before binding.
- Missing storyboard page or orphan PPT slide: report it; do not manufacture a match.

### Insert, delete, or reorder slides

- Add a new semantic ID only for a genuinely new slide.
- Change `order` to move slides; never rename existing IDs because positions changed.
- Recalculate the derived page map and PPT page numbers after sorting.
- For deletion, retain a manifest record with an explicit deprecated status when traceability matters; otherwise follow the user's explicit versioning policy.

## Change control

- Update the manifest before changing a storyboard-controlled PPT.
- Increment the affected slide's `revision` for an approved content change.
- Record what changed and why in the project's changelog when one exists.
- If the user changes only a score, weight, source, or wording, update every slide that consumes that fact; do not infer impact by page adjacency.
- Keep generated page maps, DOCX exports, and PPTs as derivatives. They must not become competing sources of truth.

## Stop conditions

Stop and ask the user when the approved manifest is missing, two IDs collide, a legacy mapping is ambiguous, two approved sources conflict, or a requested edit would overwrite locked content without explicit authorization.

## Deterministic validation

Run:

```bash
python3 scripts/validate_storyboard_manifest.py /path/to/Storyboard_Manifest.md
```

For a deck handoff, require an approved document and approved active slides:

```bash
python3 scripts/validate_storyboard_manifest.py /path/to/Storyboard_Manifest.md --require-approved
```

To emit a derived page map:

```bash
python3 scripts/validate_storyboard_manifest.py /path/to/Storyboard_Manifest.md \
  --page-map /path/to/Storyboard_Page_Map.json
```

Deliver the validation result with the artifact. A successful structural check does not replace semantic and visual acceptance against the manifest.
