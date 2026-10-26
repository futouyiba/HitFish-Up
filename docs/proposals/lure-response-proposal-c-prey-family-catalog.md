# Proposal C｜Prey Family Catalog

状态：Working Closure / Candidate。不是 Current，不是生产参数。

## 1. 结论

Prey Family Catalog 第一版采用**分层 catalog**，而不是单层枚举。

目标同时服务三个消费者：

```text
Presentation / prey interpretation
BaseDietAffinity
DietaryShift
```

Catalog 主轴回答“吃的是什么”，不编码水层、底栖/表层、运动状态或当前可获得性。这些事实继续由 prey-state / presentation context / spatial ecology 等 owner 负责。

## 2. 为什么不能单层做得很细

如果每个猎物都直接成为独立 family，例如：

```text
shad
minnow
bluegill
crayfish
shrimp
mayfly
caddis
worm
snail
frog
...
```

则会导致：

- 约 200 个鱼种的 BaseDietAffinity authoring 迅速膨胀；
- DietaryShift 需要维护大量小粒度 delta；
- lure interpretation 必须输出过细且证据不足的 prey identity；
- 同一生态事实在多个系统重复配置。

因此首版使用父级 family 提供默认关系，只有玩家策略、资料证据和 response 行为确实需要区分时才下钻子类。

## 3. 推荐一级 Catalog

第一版建议从以下一级节点开始：

```text
AnimalPrey
├─ Finfish
├─ Crustacean
├─ Insect
├─ AnnelidWorm
├─ Mollusk
├─ Amphibian
├─ OtherSmallVertebrate
├─ MicroPrey
└─ EggRoe

NonAnimalFood
├─ PlantAlgae
└─ Detritus
```

说明：

- `Finfish`：鱼类猎物；
- `Crustacean`：虾、螯虾、蟹及其它较大甲壳类；
- `Insect`：水生或陆生昆虫；是否 aquatic / terrestrial 不写进 family id，而作为独立 trait / context；
- `AnnelidWorm`：寡毛类、多毛类等 worm-like prey；
- `Mollusk`：螺、蚌等；
- `Amphibian`：蛙、蝌蚪等两栖类；必要时 life-stage 作为独立 trait；
- `OtherSmallVertebrate`：小型爬行类、哺乳类等低频但真实的小型脊椎猎物；
- `MicroPrey`：以 zooplankton / microcrustacean / larvae 等微型动物性食物为主的 operational family；
- `EggRoe`：鱼卵 / roe 等具有独立策略意义的食物；
- `PlantAlgae`、`Detritus` 用于全游戏 FoodValue / Diet profile，不要求所有 lure-response path 消费。

这些是 production taxonomy 的 Working 起点，不是自然界完整分类。

## 4. 允许的二级下钻

只有出现明确策略差异时才增加二级节点。首批候选：

```text
Finfish
├─ BaitfishLike
└─ OtherFinfish

Crustacean
├─ CrayfishCrabLike
├─ ShrimpPrawnLike
└─ OtherCrustacean

Insect
├─ AquaticInsect
└─ TerrestrialInsect
```

这里的二级节点仍应满足至少一个 admission 条件：

1. 玩家能通过饵 / 手法明确针对该分支；
2. 多个鱼种在 DietAffinity 或 DietaryShift 上稳定表现出不同关系；
3. Presentation 能获得足够证据区分；
4. 该区分会改变 response 排序，而不只是换名字。

不满足这些条件的细分继续留在外部证据 / explain metadata，不进入 production catalog。

## 5. 不把 habitat / state 编进 Family

拒绝这种 catalog：

```text
BenthicCrustacean
SurfaceInsect
PelagicBaitfish
DistressedBaitfish
BottomWorm
```

因为：

```text
prey family
→ 吃的是什么

prey-state / presentation context
→ 当前在什么位置、怎么动、呈现什么状态
```

Crustacean 是否 near-bottom、Insect 是否 surface、Finfish 是否 distressed，应由现有 prey-conditioned state 解释，不复制到 family id。

## 6. Catalog 与 BaseDietAffinity

Diet Archetype 可以只配置父节点：

```text
Piscivore:
  Finfish = Preferred
  Crustacean = Good
  Insect = Marginal
```

若某物种确实对某子类有特殊关系，则做最窄 override：

```text
SpeciesOverride:
  CrayfishCrabLike = Preferred
```

未 override 的子节点继承最近父节点。

因此 authoring 不要求每个 species 填满所有 leaf。

## 7. Catalog 与 DietaryShift

Dietary Shift 同样使用分层 key：

```text
SeasonalShift:
  Crustacean = +delta
  Finfish = -delta
```

若证据只支持 crayfish 而不支持 shrimp，则允许：

```text
CrayfishCrabLike = +delta
```

但不允许同一 lineage 在父子层同时重复结算：

```text
Crustacean +0.1
CrayfishCrabLike +0.2
```

必须定义为“子节点 override 父节点”或“先继承后替换”，不能默认相加。

第一版推荐 **most-specific override wins**。

## 8. Catalog 与 Presentation Interpretation

Presentation 可以返回一个或多个不同分支的 prey interpretations：

```text
BaitfishLike support = 0.90
CrayfishCrabLike support = 0.75
```

这两个是 alternative sibling interpretations，可以进入现有 max composition。

但若输出：

```text
CrayfishCrabLike = 0.80
Crustacean = 0.80
```

它们属于同一 lineage，不能当成两份独立 prey opportunity。

第一版规则：

> 同一 lineage 只保留最具体、已解析且被消费方支持的节点；父节点作为 fallback / inheritance source，不另生成 sibling response。

因此：

```text
CrayfishCrabLike
→ lookup CrayfishCrabLike override
→ 若缺失则向上继承 Crustacean
```

而不是：

```text
C_crayfish
C_crustacean
→ max(C_crayfish, C_crustacean)
```

## 9. Source / Habitat Traits 分离

如果策略需要区分 aquatic / terrestrial、benthic / pelagic、surface-associated 等来源，不进入 Family 主树，而使用独立 trait：

```text
PreyTraits {
  origin: aquatic | terrestrial | mixed
  typical_zone: benthic | water_column | surface | variable
  scale: micro | macro
  ...
}
```

这些 trait 只有在某 consumer 有明确 owner 时才生产化。

这样避免把分类树变成笛卡尔积：

```text
AquaticInsect
TerrestrialInsect
SurfaceTerrestrialInsect
BenthicAquaticInsect
...
```

## 10. 与外部资料的关系

外部 trophic 数据通常同时存在粗 guild 与更细 food-item taxonomy。FishBase 分开维护 species food items、diet composition 等数据；生态研究也常先按 piscivore / invertivore / omnivore / detritivore 等 guild 做粗分类，再在需要时细分 crustacean、insect、mollusk 等 prey。

本项目因此不直接照搬某一自然分类表，而采用：

```text
外部 food-item evidence
→ map 到本项目稳定 prey family
→ DietArchetype / species sparse override
```

映射过程保留 provenance。无法稳定映射时标 `Unknown`，不强塞 `Other` 后继续当已知。

## 11. Admission / Split Rule

新增一个 prey subfamily 前必须回答：

```text
它是否购买了新的策略表达能力？
```

至少应满足以下之一，并最好满足两个以上：

- 玩家有独立饵型 / 操作策略；
- 多鱼种的 affinity 排序会因此变化；
- DietaryShift 会对它和兄弟节点产生不同方向；
- Presentation 有可靠可识别线索；
- 现有父 family 无法表达受控案例。

否则不拆。

## 12. 当前 OPEN

- 是否真的需要 `EggRoe` 独立于 Finfish / other animal food；
- `MicroPrey` 是否应拆成 zooplankton / microcrustacean / larvae；
- `OtherSmallVertebrate` 是否需要进入首版 catalog，还是只留 extension slot；
- Insect 是否在首版就拆 aquatic / terrestrial；
- prey family id 与项目现有术语 / schema 的最终命名；
- 基于当前约 200 鱼种做一次 coverage test，验证一级节点是否足够、override 是否稀疏；
- lure/bait authoring 是否能稳定映射到同一 catalog。

在 coverage test 前，本页只冻结层级原则、inheritance / override 语义与“不把 state/habitat 编进 family”的边界，不冻结最终节点集合。
