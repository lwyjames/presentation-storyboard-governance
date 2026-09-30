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

## Default review presentation

- Default user-facing Manifest drafts, analytical decks and delivery summaries to conclusions, page content, visual intent and useful speaker notes. Do not show evidence locators, source IDs, timestamps, claim-type ledgers, uncertainty/boundary sections, source conflicts, capture diagnostics or verification checklists unless the user explicitly requests them. Do not hide these details in HTML comments or append a review annex.
- Keep verification, claim distinctions, source conflicts and traceability in the internal project evidence/assets register keyed by `slide_id`. Preserve existing records when simplifying a Manifest; never create a second authoritative storyboard.
- Describe visuals by subject, layout and purpose in the review Manifest; keep source IDs, timestamps, asset paths and capture readiness in the internal register.
- Keep short product qualifiers that change the meaning of a claim (preview, planned release, eligible plans, paid usage, compatibility). Integrate them into page content instead of adding a separate judgment-boundary block. Express strategic forecasts as conditional forecasts, not established facts.
- Disclose a concrete blocker only when it materially prevents completion or requires a user decision; do not repeat routine internal verification details in the handoff.

## User-designated visual and factual sources

- Register user-designated video and official-site URLs with stable `source_id` and purpose in the internal project register. Write `未指定` for a missing category rather than inventing a URL. Add a visible `## 用户指定来源` section to the Manifest only when the user explicitly requests source documentation.
- Use designated videos to find frames supporting specific slide arguments. For each saved frame, record source ID, timestamp, visible subject, target `slide_id`, and saved asset path. Track planned captures, saved assets and final-crop-reviewed assets separately. Record actual player time, visible subject, stream resolution and saved-image pixel dimensions; do not present a high-resolution stream as an equally high-resolution screenshot.
- Use designated official pages for product imagery and for checking storyboard facts. Revise approved content only when the user's instruction permits it and the correction is grounded in the designated page; record the evidence and increment each affected slide's `revision`.
- Associate source IDs and locators with the relevant `slide_id` in the internal project register. Keep review-facing `视觉设计` focused on subject, composition and purpose. Carry image attribution into later production notes or the project asset register.

## Agenda, chapter covers and visible sources

- Title the agenda `内容目录` or a meaningful thematic title. Do not count questions or pages in its title; avoid constructions such as `三个问题，25页正文`.
- Plan a dedicated chapter cover before each substantive chapter. Give each one its own stable semantic `slide_id`, the corresponding `section_id`, and `type: section_divider`. Its visual intent should introduce the chapter's subject or central question, not duplicate the entire agenda. The overall cover and agenda are not substantive chapters.
- Track content pages separately from the overall cover, agenda and chapter covers. Preserve the user's requested content allocation; unless explicitly included in a fixed total, chapter covers are additional structural pages. Surface a fixed-total conflict during draft planning rather than silently consuming content pages or omitting chapter covers.
- Keep sources in speaker notes and evidence/asset registers. Do not put source text at the lower-left of an image, in visible image captions or slide footers, or in another corner as a workaround. If required attribution conflicts, choose a suitable alternative asset rather than discard provenance or mandatory attribution.
- Write visible analytical slide copy as a direct account of the function, user value and product competitiveness. Avoid source-by-source narration such as “发布会说” or “官网补充” in the body; retain precise provenance and fact/demo/plan/inference distinctions in the internal project register and production notes, outside the default review body. Keep material availability, cost and compatibility limits visible when needed for a truthful user-facing claim.
- These defaults guide new drafts and authorized revisions. Do not silently retrofit extra pages or change approved titles in an existing approved deck without authorization.

## Choose the workflow

### Create and revise a draft in the same Manifest

1. Read [references/manifest-schema.md](references/manifest-schema.md). Create `Storyboard_Manifest.md` with document and slide statuses `draft`, a provisional version and `effective_date: "未批准"`; keep user-designated sources in the internal project register. The project ID and semantic slide IDs may be assigned now; refine draft IDs if the underlying meaning changes before approval.
2. Preserve user-specified core questions and approximate pages per question. Write each page's core expression, content, visual intent and optional speaker notes in the manifest body; keep evidence locators and judgment boundaries in the internal register. Summarize in chat and provide the actual Markdown file for review. Do not create a second standalone Storyboard draft.
3. Apply feedback to this same file, increment its draft version, and run structural validation. Keep an explicit record of which revision the user approved.
4. On approval, mark the document and retained slides `approved`, fill `effective_date` and `source_reference` with the user-approved revision, and freeze the semantic IDs. Run validation with `--require-approved` before handing the Manifest to Presentations.

### Convert an approved storyboard

1. Read only the user-designated approved source. If it is DOCX, use the Documents skill for extraction and inspection.
2. Ignore the current PPT as a content source. It may be used later only for comparison.
3. Read [references/manifest-schema.md](references/manifest-schema.md), create `Storyboard_Manifest.md`, and assign stable semantic IDs.
4. Keep original content under its original semantic labels such as `核心表达`, `页面内容`, and `视觉设计`. Record source page numbers as internal provenance; use `source_page_reference: "内部登记"` in the default review Manifest.
5. Register user-designated video and official-site URLs with their visual and factual-review purposes in the internal project register, linking each to relevant stable slide IDs.
6. Mark pre-finalized or externally supplied pages as locked when the source says they should be skipped or preserved.
7. Run `scripts/validate_storyboard_manifest.py --require-approved` and resolve every error before deck production.

## Default diagram production

- For conceptual, scenario and strategic illustrations, default to the 创建图像 (`imagegen`) skill and available image-generation tool. Generate a visually polished PNG that explains the approved page's argument; the diagram itself need not be editable. Use a consistent visual language across the deck.
- Generate the diagram/illustration area, then compose it with separately typeset slide titles and viewpoint/body copy through Presentations. Keep primary Chinese copy out of the generated bitmap when separate typesetting improves clarity. Do not replace the complete slide with an image by default; honor an explicit request for whole-slide PNG output separately.
- Match the image to the approved visual intent, surrounding light palette, allotted aspect ratio and negative space. Inspect legibility, relevance and crop after placing it in the slide. Refine the image if it weakens the point or conflicts with the copy.
- Render exact numeric charts, precise process/relationship diagrams and information that must be exact with deterministic plotting/vector/layout tools. Embed those as non-editable PNGs when useful; do not use generated imagery for them. Preserve the approved labels, values and relationships.
- Keep genuine product/UI evidence from designated official imagery or verified video frames. A generated illustration conveys an explanation or scenario; it is not product evidence.
- Record generated illustration paths, creation prompts, producer and target `slide_id` in an internal `illustrations` register, separate from factual evidence assets. Check every illustration in the final rendered deck; record creation/crop checks internally.

### Create or revise a PPT from the manifest

1. Load the Presentations skill and validate the manifest with `--require-approved` first.
2. Sort slides by `order`; derive display page numbers after sorting.
3. Match an existing PPT slide by speaker-note `STORYBOARD_ID` only.
4. Implement the manifest's core expression, page content, and visual design as separate acceptance criteria. Default conceptual/scenario/strategic diagram areas to 创建图像 PNGs composed with separately typeset titles and body copy; use deterministic drawing for exact diagrams and numeric charts. Do not require diagram editability unless explicitly requested. Check referenced visuals against the user-designated source register and preserve attribution. A correct title alone is not sufficient.
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

- Treat pure rendering fixes (CSS class isolation, z-order, spacing, visibility or crop adjustments that preserve the approved visual intent and evidence) as implementation corrections. Do not demand renewed storyboard approval or change content revisions for them; record the artifact correction and reset/repeat affected visual checks. Update the manifest first if the fix changes approved wording, core expression, evidence meaning, chapter structure or visual intent; use existing authorization rather than asking again unnecessarily.

- Update the manifest before making content or visual-intent changes to a storyboard-controlled presentation; implementation-only fixes follow the rule above.
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
