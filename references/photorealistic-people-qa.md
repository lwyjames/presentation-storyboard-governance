# Photorealistic people: output acceptance

Apply this gate whenever a slide, PNG, PDF, background asset or photography-direction sample promises photographic human realism. Do not apply photographic-skin requirements to an explicitly approved illustration or stylized character.

## Inspect the actual output

1. Inspect the complete image/slide at its intended viewing size for believable human presence, flattering but natural light and consistency with the scene.
2. Inspect each visible person's forehead, cheeks, eye area, jaw, neck and hands at 100% of the actual source pixels. Use 200% only to locate artifacts; an enlarged crop is diagnostic, not new image detail. Do not accept a thumbnail alone.
3. Repeat inspection on the final slide crop and exported PNG/PPT/PDF rendering. Scaling, sharpening, compression and later edits can introduce or amplify defects. Check a background-only deliverable independently.
4. Keep crop evidence and pass/fail notes in the internal asset register keyed by `slide_id`; do not add diagnostics to the audience-facing slide or default review Manifest. Require visual inspection, not a fabricated automated realism score.

## Reject these defects

- Crosshatched, polygonal, triangular, mesh-like or crack/scratch networks over the face, forehead or neck; repetitive pores/dots or etched lines that do not follow human anatomy.
- Hard varnish-like highlights, wax/plastic or CGI skin, excessively smoothed facial surfaces, crunchy HDR microcontrast, halos or artificial sharpening.
- Implausible skin color patches, inconsistent face/neck/hand lighting, or a face whose surface detail and sharpness do not match the photograph's scale and focal plane.

Allow natural age lines, scars, freckles, stubble, pores and tonal variation. Do not treat normal human features as defects, change age or identity to pass, or require visible pores at a resolution where real photography would not resolve them.

## Repair and recheck

### Protect the photographic master before editing

- Apply this workflow by default when the user requests a revision; do not require repeated prompt wording or approval for routine local corrections. Define the smallest editable region and necessary adjoining anatomy, contact shadows or lighting transitions. Identify protected regions/layers before choosing the edit method; do not enlarge the scope merely for convenience.
- Keep the original source and the last visually accepted photographic master unchanged. Record the chosen base, editable region, protected elements and outstanding changes in the internal asset register. Do not automatically use the latest output as the next input. If it regresses, discard that branch and return to the last passing base; carry forward the complete current requirements, including previously accepted hand/device changes.
- Keep titles, logos, crops and darkening gradients in separate layout/adjustment layers where feasible; preserve approved photographic pixels instead of sending the whole photograph through generation for these changes. Use available supported production tools; do not silently switch image-generation tools or models.
- Check actual tool capabilities. Use a supplied region/mask when supported, but treat it as editing guidance rather than a guarantee of unchanged outside pixels. When only text instructions are supported, specify the edit region and preservation constraints explicitly and treat the result as unprotected until inspected. Never claim a prompt, mask, high-fidelity setting or seed has locked pixels.
- For precise local corrections, prefer retaining the untouched master outside the edit region and compositing only an accepted generated patch using supported tools. Match perspective, light and contact edges; rerun seam/occlusion checks. Do not promise exact preservation when the available workflow cannot provide it.
- Compare each candidate against the chosen base at the same pixel scale, not just against the immediately preceding output: check the requested change, protected identity/pose/gaze/device/UI, and native-pixel face/neck/hands for relative skin or lighting degradation. Compare protected pixels directly when layers/alignment permit; otherwise perform visual comparisons and disclose the limitation. Reject a candidate even if its absolute appearance seems plausible when it worsens previously accepted skin or changes protected content without authorization.
- Stop inheriting degraded output. After two focused failures, return to a passing master and consolidate the current brief or rebuild the affected human layer from clean photographic direction. Preserve approved identity and visual intent; use existing change control if either must change. Keep these rules and diagnostic evidence in production records, not audience copy.

### Correct skin defects

- Ask for a genuine photographic result with subtle irregular skin detail, coherent soft light and restrained microcontrast. Do not equate “more pores,” “more texture” or “ultra-sharp detail” with realism.
- Preserve approved identity, expression, gaze, pose, layout, device geometry, screen evidence and hand contacts during skin repair. Protect approved device and UI layers; fix the human/lighting layers.
- Inspect after every repair. If artifacts persist after two focused attempts, stop reusing the defective skin texture: reconstruct the affected human layer from a clean photographic direction while preserving approved identity and composition, then composite protected device layers again. If a necessary repair changes approved visual intent or identity, follow existing change control; do not silently claim it is the same asset.
- Do not hide defects by shrinking the face, heavy blur, darkening the person or adding a stylized effect. After repair, rerun skin, gaze, hand-contact and device checks so one correction cannot regress another.

## Delivery gate

Deliver only after the person looks photographically plausible at intended size and native-pixel inspection, with no synthetic pattern or plastic material response in the inspected regions. Report only measured output dimensions; a requested native resolution or larger interpolated file is not proof of newly resolved photographic detail. Do not claim perfect realism or a completed repair when artifacts remain.
