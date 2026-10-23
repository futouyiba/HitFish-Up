# CXR9-BASELINE-01 窄重核（2026-09-21）

本记录回应 [#33](https://github.com/futouyiba/HitFish-Up/issues/33) 与 [PR #9 原 finding](https://github.com/futouyiba/HitFish-Up/pull/9#issuecomment-5757689891)：固定原实现，重判契约基线变化影响的两项。它是版本化验证结果，不是现行规则 Owner，也不是今日实现完成证明。

## 目标与证据边界

| 对象 | exact target 与用途 |
|---|---|
| 旧契约投影 | `b054473752f24769bf80b643866ff3eb6860bdf2`：原报告实际使用的判据 |
| 契约修正点 | `ed2fde0d3c011ceb87495d788d410fa9ff02216e`：原报告声称升级到的基线 |
| 重核契约投影 | `efa727e944d3dc6b9fdd18e934f0e1cdbde0013d`：确认上述两项在当前已合并投影中的含义仍成立 |
| 被核实现 | `preCompute` 的 `bae6e6fbddca04a7d94a1e814ec5ea23af1c7c97`；全文代码锚均绑定此 commit，路径相对其 `FishHabitEditor-0.3.4.0-b/` |
| 原报告快照 | [fde61e3 的报告](https://github.com/futouyiba/HitFish-Up/blob/fde61e3d3da68f1f2181c4fd37d1e76c348a098f/docs/offset-check-0.3.4.0-B-20260921.md) |
| 原落仓说明快照 | [42c6968 的说明](https://github.com/futouyiba/HitFish-Up/blob/42c6968adb02c78e853dfd40d7055b2676cddeab/docs/offset-check-0.3.4.0-B-20260921.LANDING-NOTE.md) |

依据为固定的仓内 Markdown 投影与上述本地 Git 对象。上游 Current／Owner 原页本次**未核**；不把仓内投影升级为 Product Authority。原报告、落仓说明均不修改。未检查后续实现 commit，不推断这些偏移今天仍存在。

## R1：Source Override 身份分层

**Before → after（契约）**：旧 `OPEN-ITEMS.md` 的能力表将 Engagement Mode 写成 owner identity；`ed2fde0` 将该行改为 authoring 粒度与物理 durable key 两层。旧版 ADJ-08 主条目已存在物理键要求，因此这不是首次引入新机制，而是消除旧投影的混写。复核 [b054 → ed2 diff](https://github.com/futouyiba/HitFish-Up/compare/b054473752f24769bf80b643866ff3eb6860bdf2...ed2fde0d3c011ceb87495d788d410fa9ff02216e) 的 `OPEN-ITEMS.md`；完整身份边界以 [efa §16](https://github.com/futouyiba/HitFish-Up/blob/efa727e944d3dc6b9fdd18e934f0e1cdbde0013d/docs/review/ui-component-contract-r2/component-contract-consolidated.md#identity-boundaries) 为固定判据。

**实现证据**：`src/editor/refConsumers.ts:53,62–64` 的两个分支只接收 `speciesId/scope`，分别返回 `row:${scope}` 与 `species:${speciesId}/${scope}`；`src/editor/sourceOverride.ts:50–57` 拼接 `owner|component`，并委托上述 helper。不同物种同为 `mature` 时，前一分支均返回 `row:mature`。它既没有接收也没有解析物理 row ref，选择 `affinity-row` 分支不能使它成为 `FishEnvAffinityRef`。

限定搜索 `src/` 内 `ownerOf(`、`ownerKeyOf(`、`sourceOverrideKeyOf(` 的调用式文本，只命中三个声明及 wrapper 内一次调用；未见这些 helper 的 UI／持久化调用者。此搜索不证明整套 Source 流程都不存在，也不排除别名调用。

**重核结论**：原报告第 1 项“部分偏移”保留，但理由收敛为**历史 helper 未表达物理键，且未证明接入 durable 路径**。原 §2／§7(2) 把 ADJ-06 与 ADJ-08 当待裁冲突、并建议固定为 `row:${scope}` 的解释，不能作为修复依据；两种粒度不处于同一层，旧最小修法也不足以对齐。此结论与原落仓说明 §5 的纠偏相容，没有新增产品裁决。

## R2：TimePeriod Preset 覆盖护栏

**Before → after（契约）**：旧汇编 §15 将时段批量预设列入统一 staged 路径；`ed2fde0` 将它分为无覆盖与覆盖已有 local ops 两支。完整条件以 [efa §15 的 Batch Overwrite Guard](https://github.com/futouyiba/HitFish-Up/blob/efa727e944d3dc6b9fdd18e934f0e1cdbde0013d/docs/review/ui-component-contract-r2/component-contract-consolidated.md#timeperiod-batch-guard) 为固定判据，本记录只报告实现对照，不另维护规范。

| 检查支路 | `bae6e6f` 证据 | 重核结果 |
|---|---|---|
| 无 local ops 被覆盖 | `src/ui/app.ts:864–885` 首次应用一律设置 pending 并返回，未按现有 ops 分支；空 Map 探针第一次 0 次 commit，第二次才 1 次 | 不对齐无覆盖时不强制确认的判据；两步按钮路径见 `src/ui/render/authoring.ts:1001–1013` |
| 覆盖已有 local ops | 同一 handler；预置一个 SET 的探针也须第二次应用。`src/ui/render/authoring.ts:626–657` 列五字段 before/after 与确认／取消按钮 | 显式确认与五字段比较可核；该 preset 预览块未列被替换的 local ops 或新增 Error／Warning，不能判完整 Guard 已对齐 |
| 写入与取消的局部行为 | handler 循环五个键写 SET，然后调用一次 `commitWorkingCopy()`；取消仅清 pending 与 render | 探针验证 handler 层的五次写入／一次提交调用及取消不提交；**不证明持久化原子性、重载正确性或真实浏览器交互** |

原报告将 handler 写作 `src/ui/app.ts:870–891`，该锚不属于所标 `bae6e6f`；本次按 exact blob 使用 **864–885**，不把不同实现版本的行号混用。

**重核结论**：原主表第 6 项、§3 及 §7(3) 的“六条全部成立／已对齐”，在修正后的契约基线上**不成立**；本次覆盖护栏范围判为**未对齐**。只替代该总体通过结论及无条件两阶段的判据，不重判 target layer、Source、不持久化 presetId 等其余条目，也不把一次函数调用升级为 durable atomic commit 证明。

## 可复现检查

环境：Node.js `v22.23.2`。在持有上述历史对象的 `preCompute` 仓根，将以下代码存为临时 `probe.cjs` 后运行 `node probe.cjs .`。从 exact blob 提取原 handler／helper 函数体；五个键和预设值为夹具，渲染与 commit 为计数替身，`setPatchFor` 为 SET 替身。测试的是控制流，不是真实配置值、patch 编码或端到端保存。无需修改实现 checkout 或安装依赖。

```js
const {execFileSync}=require('node:child_process');
const assert=require('node:assert/strict');
const repo=process.argv[2], rev='bae6e6fbddca04a7d94a1e814ec5ea23af1c7c97';
const root='FishHabitEditor-0.3.4.0-b/';
const read=p=>execFileSync('git',['-C',repo,'show',`${rev}:${root}${p}`],{encoding:'utf8'});
const app=read('src/ui/app.ts');
const match=app.match(/onApplyPeriodPreset: \(presetKey\) => \{([\s\S]*?)\n          \},/);
assert(match);
const keys=['A','B','C','D','E'];
const make=new Function('TIME_PERIOD_KEYS','TIME_PERIOD_PRESETS','setPatchFor',`return function(presetKey){${match[1]}\n}`);
const handler=make(keys,[{key:'probe',values:Object.fromEntries(keys.map(k=>[k,2]))}],(c,k,v)=>({op:'SET',value:v}));
const cases=[];
for(const overwrite of [false,true]) {
 const state={periodPresetPending:null,expressedCells:new Map(overwrite?[['TIME_PERIOD|A',{op:'SET',value:1}]]:[]),renders:0,commits:0,render(){this.renders++},commitWorkingCopy(){this.commits++}};
 handler.call(state,'probe');
 assert.equal(state.commits,0); assert.equal(state.periodPresetPending,'probe');
 const first={commits:state.commits,cells:state.expressedCells.size,pending:state.periodPresetPending};
 handler.call(state,'probe'); assert.equal(state.commits,1);assert.equal(state.expressedCells.size,5);
 cases.push({overwrite,first,second:{commits:state.commits,cells:state.expressedCells.size,pending:state.periodPresetPending}});
}
const cancel={periodPresetPending:'probe',expressedCells:new Map(),render(){},commitWorkingCopy(){throw Error('unexpected commit')}};
handler.call(cancel,null);assert.equal(cancel.periodPresetPending,null);assert.equal(cancel.expressedCells.size,0);
const ref=read('src/editor/refConsumers.ts');
const body=ref.match(/export function ownerOf\([^\n]+\n([\s\S]*?)\n\}/);assert(body);
const owner=new Function('e','granularity',body[1]);
const owners=[1,2].map(speciesId=>({speciesId,row:owner({speciesId,scope:'mature'},'affinity-row'),bucket:owner({speciesId,scope:'mature'},'species-bucket')}));
assert.equal(owners[0].row,owners[1].row);
console.log(JSON.stringify({implementation:rev,cases,cancel:'no commit; no cell write',owners},null,2));
```

实际输出：两组首击分别保留 0／1 个 cell，均为 `commits=0, pending=probe`；第二击均为 `cells=5, commits=1, pending=null`；取消不写 cell、不提交。两个物种的 row 分支均为 `row:mature`，bucket 分支分别为 `species:1/mature`、`species:2/mature`。全部断言通过；这是偏移的可重复观测，**不是 Contract 验收通过**。

静态回读在实现仓执行（输出行号均属于固定 commit）：

```sh
rev=bae6e6fbddca04a7d94a1e814ec5ea23af1c7c97
root=FishHabitEditor-0.3.4.0-b
 git show "$rev:$root/src/ui/app.ts" | nl -ba | sed -n '858,885p'
 git show "$rev:$root/src/ui/render/authoring.ts" | nl -ba | sed -n '626,657p;1001,1013p'
 git show "$rev:$root/src/editor/refConsumers.ts" | nl -ba | sed -n '53,64p'
 git show "$rev:$root/src/editor/sourceOverride.ts" | nl -ba | sed -n '50,57p'
 git grep -n -E 'ownerKeyOf\(|ownerOf\(|sourceOverrideKeyOf\(' "$rev" -- "$root/src"
```

## 收口范围

`CXR9-BASELINE-01` 所要求的两项基线差异已分别给出 before/after、绑定实现锚及替代结论；是否关闭该 finding 由独立审核确认。没有宣称原 PR #9 全部遗留、原报告其他 ADJ 项或当前实现通过。ADJ-03 不在重核范围：行级 `rules` 仍不能证明物种层 `policyRecipe` 中 `INHERIT` 与同原值 `SET` 的记录态，未实测仍未实测。
