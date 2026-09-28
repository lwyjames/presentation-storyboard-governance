# PPT-to-storyboard audit contract

Use this contract when validating a PPT or migrating a legacy deck that lacks stable IDs.

## Match priority

1. Exact `STORYBOARD_ID` in speaker notes.
2. For legacy slides only: unique exact title plus compatible core expression, page content, and visual structure.
3. Human confirmation for every ambiguous or conflicting candidate.

Never use page number, neighboring slide, visual similarity alone, or current PPT wording as the identity key.

## Required audit checks

For each manifest slide, report:

| Check | Passing condition |
|---|---|
| Identity | One PPT slide has the exact notes ID |
| Title | PPT title represents the approved title without changing its claim |
| Core expression | Main takeaway matches the approved core expression |
| Page content | Required facts, labels, examples, and conclusions are present |
| Visual design | Required chart, diagram, hierarchy, or composition is implemented |
| Order | Derived PPT position matches manifest order |
| Lock | Locked content has not been rewritten without authorization |

Also report duplicate IDs, missing IDs, manifest slides absent from the PPT, and orphan PPT slides absent from the manifest.

## Status labels

- `PASS`: fully aligned.
- `PARTIAL`: recognizable but one or more requirements are incomplete.
- `FAIL`: contradicts or materially omits the storyboard.
- `UNMAPPED`: no reliable identity match.
- `BLOCKED`: source conflict or authorization is required.

## Legacy migration output

Before editing notes, produce a mapping table with PPT title, proposed `slide_id`, evidence, confidence, and action. Bind only unique high-confidence matches. Ask the user to resolve all others.

## Acceptance rule

A slide does not pass merely because its title is correct. Identity, core expression, page content, and visual design are independent acceptance criteria.
