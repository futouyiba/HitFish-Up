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

## Per-asset registration（实填）

实填值取自被审头 `7474d1b157af91b2ab0e24d6392366453e4e1982` 的 exact-head DESIGN／REVIEW 判词与 `asset-manifest.json`；字段名沿用上方模板。判词时点对拍时画布 `observedVersion`／`lastModified` 前后同值。

**批次级字段（16 资产共用，故不逐行重复）**

- Source document version：批次源文档锚＝下表四件离线设计稿 blob；**逐资产的离线源文档绑定＝待核** —— 本批只提供批次级锚，未提供逐帧绑定，故不以猜测补齐。
- Canvas read time and route：`2026-09-23T05:12:55Z`（fresh doc read）；路由＝Figma 只读盘点（inventory）＋逐帧 PNG 导出（3–4 帧批次）。
- Canvas object description：`Document`／`editorType=figma`／page `Current｜0.3.4.0-B 编辑器假图（W4B B Current）`。
- 画布文档版本（observed）：`2402269427359123151`；`lastModified=2026-09-23T04:56:15Z`。
- Image/live consistency：`consistent`（16/16 @ `2402269427359123151` / `lastModified=2026-09-23T04:56:15Z`）。
- Export time：`未落/待核；有界区间 [2026-09-23T05:12:55Z, 2026-09-23T05:13:32Z]`（下界＝本轮 fresh doc read；上界＝第二批逐帧导出请求时刻）—— 本地无精确日志，不猜测。
- Proof boundary：the PNG proves only static pixels at export time; it does not prove runtime behavior or persistence.

**批次源文档锚（离线设计稿 blob 版本）**

| 源文档 | blob |
|---|---|
| 0.3.4.0-B 共用N2 候选确认面板 | `124972455da74415d12ac02ff08a95a80c64f077` |
| 0.3.4.0-B A②-卡10 模板完整值编辑 | `69c98a321d1881e5fbd84c98be93e2a625d80916` |
| 0.3.4.0-B A②-卡11 Replace References | `ea55bd95374d064db6a0259de19e0965143bc350` |
| 0.3.4.0-B 冲突清单／待裁 | `d013f917c94997028d6213766861254c3859e323` |

**逐资产**

| Group（组／层） | Frame（帧名） | Label（画布标签） | Frame range | Image dimensions | PNG SHA-256 | Export time | Image/live | UNIMPL/UNVERIFIED boundary |
|---|---|---|---|---|---|---|---|---|
| A①-卡5 Provenance Display | `proj_pv_1` | 待核 | 单帧 | 890×150 | `b5df97402d2a36a65aca0c8b993215c6d7a9a7ce696068d476e55dc6f1648703` | 未落/待核 | consistent | 无标记 |
| A①-卡5 Provenance Display | `proj_pv_2` | 待核 | 单帧 | 890×150 | `a0397f186d7ac87d9c7264fd69b032bb5dc92c9d92626b7a3edf07e921e2573c` | 未落/待核 | consistent | `⚑UNIMPL` |
| A①-卡5 Provenance Display | `proj_pv_3` | 待核 | 单帧 | 890×150 | `90bc928f40ac2cbaf22955e04f2a0ea9d50d46b4b6899db37de1a11524a87672` | 未落/待核 | consistent | `⚑UNIMPL` |
| A①-卡5 Provenance Display | `proj_pv_4` | 待核 | 单帧 | 890×204 | `1e7939275ed9b20e783ad9528ddc798ee78b9939f721bbfc7a72e288ee4e12f9` | 未落/待核 | consistent | `⚐UNVERIFIED` |
| A①-卡5 Provenance Display | `proj_pv_5` | 待核 | 单帧 | 890×150 | `6a9aa59cab0490e3d486e09b4e0a3330c87f21182dff4bb663fef10f94f7a760` | 未落/待核 | consistent | 无标记 |
| A②-卡8 Template Library List | `proj_tl_1` | 待核 | 单帧 | 890×150 | `8225c67fda798334374a05fd7aa7525327e37e8fa62a57e43239e187f0f34e39` | 未落/待核 | consistent | 无标记 |
| A②-卡8 Template Library List | `proj_tl_2` | 待核 | 单帧 | 890×150 | `9b7b6c9fa7d4ad9d92f50539773f307661daed762d491ade6005058c0830a5e5` | 未落/待核 | consistent | 无标记 |
| A②-卡8 Template Library List | `proj_tl_3` | 待核 | 单帧 | 890×150 | `8c46918bf0445955076d787680c92ccd6cc76560e9d5ba22bb8bd5dd678df931` | 未落/待核 | consistent | 无标记 |
| A②-卡8 Template Library List | `proj_tl_4` | 待核 | 单帧 | 890×188 | `9de07b4f93a20b4666efbf596657782475795eadf15326a207e11e76af6b11e8` | 未落/待核 | consistent | 无标记 |
| A②-卡12 Reference List | `proj_rl_1` | 待核 | 单帧 | 890×150 | `689ecf5dbf9518b8065bbbba53d7fc16cf0fd2e95dcdd8cdc08de79c47f63293` | 未落/待核 | consistent | 无标记 |
| A②-卡12 Reference List | `proj_rl_2` | 待核 | 单帧 | 890×150 | `a39f42060cee7a4c427c4f8a99774408804363e48f2c0e5aed21a5d0c366e478` | 未落/待核 | consistent | 无标记 |
| A②-卡12 Reference List | `proj_rl_3` | 待核 | 单帧 | 890×150 | `560c3706ca0b999f47e28c344684717fd201cebd1220adf8b5b95ce5de7bfb92` | 未落/待核 | consistent | 无标记 |
| A①-RoleControl 两入口／记录态／行级操作 | `proj_role_1` | 待核 | 单帧 | 890×176 | `dc04725b027a1e37eab48635c2cfd2ba8fa5aadb53f681a1ec522df32853f9c3` | 未落/待核 | consistent | `⚑UNIMPL` |
| A①-RoleControl 两入口／记录态／行级操作 | `proj_role_2` | 待核 | 单帧 | 890×176 | `1edc439857fe6284b562cf9a77bb1c5e0dcdb56d7c9ba8f5a3a017dbde8c54c9` | 未落/待核 | consistent | `⚑UNIMPL` |
| A①-RoleControl 两入口／记录态／行级操作 | `proj_role_3` | 待核 | 单帧 | 890×176 | `d9e015de87e568ae67a573ca85838398c73518d6fb0cb708cc14909f7c36e587` | 未落/待核 | consistent | `⚑UNIMPL` |
| A①-RoleControl 两入口／记录态／行级操作 | `proj_role_4` | 待核 | 单帧 | 890×176 | `053917b5097d1cdaebc085dfdd3dbd0603adc7a2e343128ad85f4ae70d344612` | 未落/待核 | consistent | `⚑UNIMPL` |

覆盖自检（**射程逐条写明**）：16 行＝16 资产，无重复、无遗漏；尺寸多重集 = {150×10, 176×4, 188×1, 204×1}——**本句「与 `asset-manifest.json` 逐条一致」的射程仅到「尺寸多重集」这一列**，**不含逐行 hash**；标记分布 `⚑UNIMPL`×6（`proj_pv_2`／`proj_pv_3`／`proj_role_1`–`4`）＋`⚐UNVERIFIED`×1（`proj_pv_4`）＋无标记×9。**逐行内容自检（2026-09-23 补）**：本表 `PNG SHA-256` 列 16 行**逐行**与 `asset-manifest.json` 及仓库实物 blob 核过（7 帧重导后）。`Label` 为画布标签文本节点、不在 PNG 像素内，本批未提供逐帧标签串，故记 `待核`。

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
