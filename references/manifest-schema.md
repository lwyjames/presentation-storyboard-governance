# Storyboard Manifest schema

Use this schema from draft through approval in one Manifest file.

## Document front matter

Required fields:

| Field | Meaning |
|---|---|
| `schema_version` | Manifest schema version |
| `document_type` | Must be `storyboard_manifest` |
| `project_id` | Stable project identifier |
| `title` | Project title |
| `storyboard_version` | Current draft or approved revision |
| `status` | `draft` during review; `approved` only after explicit approval |
| `source_of_truth` | Must be `true` for the single canonical file; does not imply approval |
| `source_reference` | User-provided source or the explicitly approved draft revision |
| `effective_date` | `未批准` during drafting; fill the approval date on approval |
| `slide_count` | Number of slide entries |
| `page_numbers_are_derived` | Must be `true` |
| `ppt_notes_marker` | Must define `STORYBOARD_ID: <slide_id>` |

## User-designated sources

Default to registering designated sources in the internal project register, linked by stable `slide_id`. Include a visible `## 用户指定来源` section and separate `### 视频来源` / `### 官网来源` tables only when the user explicitly requests sources. Each source record has `source_id`, user-designated URL, purpose and designation context. Use `未指定` for a missing category. Do not substitute search results for a user-designated source.

For saved assets, record the source ID, video timestamp when applicable, visible subject, relevant `slide_id`, and saved file path. Link the IDs to each relevant `slide_id` in the internal register rather than in default review-facing `视觉设计` or `可用来源`. Official-site corrections require evidence and a revision increment on affected slides; a URL registration alone does not imply a page was verified.

## Slide entry

Use a level-two Markdown heading followed immediately by a fenced YAML block:

````markdown
## SB-MARKET-WINNING-PATHS｜三家厂商选择了不同的胜利路径

```yaml
slide_id: "SB-MARKET-WINNING-PATHS"
section_id: "SEC-MARKET"
order: 600
source_page_reference: 6
type: "content"
title: "三家厂商选择了不同的胜利路径"
status: "approved"
revision: 1
locked: false
```
````

The content after the YAML block remains human-readable Markdown. Preserve the source's semantic labels and wording. Default to `核心表达`, `页面内容`, `视觉设计` and optional `讲解重点`. Omit evidence locators, claim classifications, source conflicts, judgment-boundary sections and capture diagnostics from the review body; retain those internally. Integrate material product qualifiers into page content.

Required slide fields:

| Field | Rule |
|---|---|
| `slide_id` | Unique, stable, semantic, uppercase hyphenated ID |
| `section_id` | Stable semantic section ID |
| `order` | Unique positive integer; leave gaps for insertion |
| `source_page_reference` | Provenance only; never an identity key. Default review value: `内部登记`; keep exact locators in the internal project register |
| `type` | `cover`, `section_divider`, `content`, or `content_locked` |
| `title` | Current draft or approved title; must match the heading text |
| `status` | `approved`, `draft`, or `deprecated` |
| `revision` | Positive integer, incremented after approved changes |
| `locked` | Boolean protection against unintended rewriting |

## Default visual implementation

For conceptual, scenario and strategic illustration pages, write `视觉设计` around the explanatory subject, layout and a 创建图像 PNG composed with the slide's title and viewpoint/body copy. The illustration need not be editable. For numeric charts or precise process/relationship diagrams, specify deterministic drawing and optional PNG embedding. Keep exact text, values and relationships readable; keep source product/UI imagery genuine. Apply this default while drafting or implementing approved visual intent; do not silently change an already approved argument or visual structure.

## Stable ID rules

- Describe the slide's enduring meaning, not its current position.
- Good: `SB-PURA-HARMONYOS-VALUE`.
- Bad: `PAGE-10`, `SLIDE-10`, `PURA-SECOND-SLIDE`.
- Reordering changes `order`; it never changes `slide_id`.
- A newly inserted chapter page gets its own new ID and an order value between adjacent entries.

## Agenda and chapter structure

Use `内容目录` or a thematic agenda title without counting questions or pages in the title. Each substantive chapter has a dedicated cover entry with `type: section_divider`, its own semantic ID, and that chapter's `section_id`. Describe its visual intent in the entry. Use the existing `content` type for the agenda when needed; do not introduce an unsupported type.

Record the page budget before the entries: content pages by chapter, overall cover, agenda, chapter covers and total active pages. Keep `slide_count` equal to the actual entry count, not the content-only budget. Unless the user's fixed-total instruction says otherwise, chapter covers are additional structural pages. Resolve any conflicting fixed total during drafting. Preserve existing approved IDs when adding authorized chapter covers.

Record planned/saved/final-crop-reviewed asset readiness in the linked internal asset register, not in the default review body or as slide approval status. A saved asset is not automatically crop-reviewed. Store source attribution in notes/registers; omit visible image-source labels, captions and footers.

## Page map

Derive page numbers by sorting active entries by `order`. A page map is output, never input. After insertion, existing IDs remain constant while their derived page numbers may change.

## PPT binding

Add exactly one line to each slide's speaker notes:

```text
STORYBOARD_ID: SB-PURA-HARMONYOS-VALUE
```

The marker is authoritative. Human-readable notes may coexist with it.
