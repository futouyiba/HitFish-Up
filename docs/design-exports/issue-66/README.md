# Issue #66｜最终投影导出与登记提案

**状态：proposal，等待独立 DESIGN review；本批不写 Figma。**

## 来源与读数

- fresh Figma read: `Document`／`figma`／`Current｜0.3.4.0-B 编辑器假图（W4B B Current）`，`skipInvisibleInstanceChildren=false`，pageNodeCount 2510。
- inventory read time: 2026-09-22T11:46:50Z，observedVersion 2402018176087182650；inventory is a locator list, not a registration record. Formal use must recheck the current `lastModified` and labels.
- public proposal contains no fileKey, node IDs, internal URLs, or credentials.

## Asset range

| Group | Frames | Assets | Boundary |
|---|---|---:|---|
| A①-Card5 Provenance Display | `proj_pv_1`–`proj_pv_5` | 5 | Static export; implementation state follows each frame’s UNIMPL/UNVERIFIED marking |
| A②-Card8 Template Library List | `proj_tl_1`–`proj_tl_4` | 4 | Static export; examples are not production readings |
| A②-Card12 Reference List | `proj_rl_1`–`proj_rl_3` | 3 | Static export; candidate statistics remain distinct from the no-candidate list |
| A①-RoleControl 两入口／记录态／行级操作 | `proj_role_1`–`proj_role_4` | 4 | Target-state static export; does not prove runtime or persistence |

Total: 16 PNG assets.

## Per-asset registration fields

The eventual registration record must fill actual values for:

```text
Group/frame/label: <fresh frame label>
Source document version: <actual consumed source blob or commit>
Canvas read time and route: <ISO-8601 + route>
Canvas object description: <name/editorType/page description>
Frame range: <one frame only>
Image dimensions: <width × height>
PNG SHA-256: <hash>
Export time: <ISO-8601>
Image/live consistency: <consistent / unverified / not applicable>
UNIMPL/UNVERIFIED boundary: <per-frame status>
Proof boundary: the PNG proves only static pixels at export time; it does not prove runtime behavior or persistence.
```

Previous evidence is not rewritten: old screenshot/report versions remain separately attributed. Missing, expired, or unreadable assets must be marked unproduced; never invent a size or hash.

## Current local evidence

`asset-manifest.json` records the 16 downloaded PNG dimensions and SHA-256 hashes. The PNGs are local export evidence, not runtime proof. The initial 16-at-once URL batch expired for 11 assets; the assets in this commit were recovered through 3–4-frame batches with immediate download and image-open validation.

## Acceptance

1. All 16 frames are located by fresh segment/frame/label intake.
2. Each PNG opens and its dimensions and SHA-256 match `asset-manifest.json`.
3. Registration covers all 16 assets without duplicates or omissions.
4. Each asset states image/live consistency and its UNIMPL/UNVERIFIED boundary.
5. No static export is presented as proof of runtime or persistence.
6. Exact-head DESIGN review and Integrator review occur against the final commit; any new commit requires re-review.

## Out of scope

- No Figma node, annotation, section, label, or layout changes.
- No rewriting historical screenshots, reports, or prior registrations.
- No automatic closure of #43 or substitution for G4 final acceptance.
