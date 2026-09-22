# 目标态离线设计稿｜共用N2 ＋ A②-卡10 ＋ A②-卡11（0.3.4.0-B）

**修订记录（供复核方对拍版本）**：
- 2026-09-22 修订三（#78 审核阻塞 B1，已修）：卡11 态3 `[n2]` 与态3 annotation 的 Policy 句补回 §14 限定词——由无条件的「Policy 直接引用…一并改绑」改为条件形「若 A 为 Policy 模板：其直接引用＝Species policy binding 与 SpeciesPreset policy binding（属本次写集）」；态2 说明句「以否定句钉住」→「以条件句钉住（仅当 A 为 Policy 模板）」。§3 映射表引文本已含限定词、无需同步。
- 2026-09-22 修订四（#78 审核阻塞 B2，已裁）：`▾` 读作**字面字形（U+25BE）**——只读探针实测：card3 档位 chip（`Custom ▾`）、card2（`SUBOPTIMAL ▾`）、card1 来源 picker（`未选 ▾`）的下拉值全部为字面 `▾` 文本；矢量 `roleCaret` 仅 Role 角标一族。卡10 判据 2 据此改写为「`[p6]` 值段文本以字面 `▾`（U+25BE）结尾」；`[p6]` 帧串本身不动。
- 2026-09-22 修订一（主代理指出的自相抵，已修）：N2 态3 `[n2]` 与卡10 态3 `[n2]` 删去「保存 I/O 失败」串词（卡7 状态词不跨卡进帧文案）；该规则短摘要移入各自态3 annotation；两侧验收判据 6 收紧为「探针面＝帧文本节点、不含 annotation」。修后全稿帧文案「保存 I/O 失败／保存失败」0 命中。
- 2026-09-22 修订二（480 横距之裁，已翻）：列位默认＝同既有 A② 组网格（组内左列 100／右列 1230、240 横距，即各册「同卡8 布局」原句）；480 出自顶层栅格实测、不适用 PROJECTION 组。已写入 conflicts P5；若 writer fresh intake 实测长 annotation 悬停展开压右列帧，报实测（截图＋几何）再单独裁本批三组列位。

**角色与边界**：本目录是 **Figma 目标态离线设计稿**——只出帧清单、逐字文案、annotation 计划、契约映射、验收判据与冲突清单；**零画布写入、零 GitHub 写入、零 Notion 写入**。落画由 `#43` 编排线在写租约下派唯一 writer 执行；本稿不含任何新行为裁定（有卡必引、无卡必标待裁）。

## 文件

| 文件 | 内容 | 消费批次 |
|---|---|---|
| [0.3.4.0-B-n2-shared-panel.md](0.3.4.0-B-n2-shared-panel.md) | 共用N2 候选确认面板（四态） | `#54`／`#62` |
| [0.3.4.0-B-card10-template-value.md](0.3.4.0-B-card10-template-value.md) | A②-卡10 模板完整值编辑（四态） | `#54`／`#62` |
| [0.3.4.0-B-card11-replace-references.md](0.3.4.0-B-card11-replace-references.md) | A②-卡11 Replace References（三态） | `#54`／`#63`（复用 N2） |
| [0.3.4.0-B-conflicts-pending.md](0.3.4.0-B-conflicts-pending.md) | 冲突清单 C1–C8／待裁 P1–P5／防撞区核对 | 全批 |

## 输入与版本锚（设计依据）

- **契约卡（行为权威）**：`docs/review/ui-component-contract-r2/`（`component-contract-consolidated.md`、`contract-cards.md`、`README.md`、`figma-current.md`、`OPEN-ITEMS.md`），基线 **main @ `8f60ed4c`**。
- **裁定**：《变更与裁决记录》（Notion Current，读数 2026-09-22）§392 ADJ-09（两正交判据／两档 Preview／FOLLOW_PARENT 不留例外）、§394（ADJ-11 第三臂已落《编辑器持久层契约》§3.7）、§331①（双入口单 Truth＝前层 Source Selector ↔ 卡 Source 下拉，焦点栏不设 Source 选择器）；`#43` 评论 Owner 裁定（2026-09-22）：`#30` 并进 `#60`，Setup 链归 `#60`、`#61` 与本批不吸收 Setup。
- **画布现状（只读，2026-09-22）**：PROJECTION 区版式范式＝`PROJECTION｜…` section＋`proj_*` 裸帧（890 宽）＋`态N｜…` 画布标签＋逐帧 annotation 四段结构（态说明／规则直链／规则链接版本／图注取证，`#57-after` 起、经 `#71` 收敛的现行形态）；annotation 链接约定按 `#73`（默认分支稳定锚点＋独立短 SHA）。
- **文档侧**：issues `#54`／`#62`／`#63` 正文；防撞预读 `#59`／`#60`／`#61`。

## Writer 通用要求（三册共用，落画时逐条执行）

1. **门槛**（沿 `#62`/`#63` 正文）：approved/merged 文档与 G2、前批独立 PASS、显式单 writer 租约；fresh live intake＋私有写前快照；双 skill（官方 `figma-use`＋仓内 `figma-mockup-write`）必读。
2. **写入**：整组读→只改目标→整组写→整组回读；annotation 用 `label` 型单字段、读源 `labelMarkdown || label`、写前 unescape；新 section 全部为新宿主——回归探针必须含**按区域枚举**的覆盖（基线清单天然看不见新增宿主）。
3. **证据**：同通路比较；字段／转义（`&`=0）计数、几何（`absoluteBoundingBox`）、节点数 Δ（frame 与 text 每件各计 1）、`figma.skipInvisibleInstanceChildren` 实读值，随探针报告原始数；截图＋raw 证据；独立 live reviewer PASS/BLOCK。
4. **标记**：三组全部 `⚑UNIMPL（GAP 号待补）`（依 `#54` 指令）；示例数据＝示意，不构成产品读数；静态画面不证明任何运行／持久化实现。
5. **公开边界**：不写内部 URL、Notion 页面 id、fileKey、节点 id 清单、凭据（本目录已按此自查）。
