<title>中鱼中层框架-逻辑模块与相互关系</title>

# 中鱼系统整体：

- **输入**

  - 鱼配置
  
    - 投鱼配置；
    - 鱼习性配置；
  - 环境条件
  
    - 课程表；
    - 钓场三维数据；一般在Unity中编辑；
  - 玩家策略
  
    - 钓具
    
      - 饵
      - 线、引线
    - 操作
    
      - 姿态
      - 饵点
      - 人物位置
- **输出**

  - 中鱼等待时间
  - 鱼种Species
- 此外，**中间**有2个非常重要的纽带数据：

  - 派生环境权重场（DEF 派生环境场）；
  - 圆桌权重表；

（大图放在这里）

<whiteboard token="E6TVw2q28h2D8BbpOW2cs7aTn6N"></whiteboard>





## 模块表

<table><colgroup><col/><col/><col/><col/><col/><col/><col/><col/></colgroup><tbody><tr><td vertical-align="top"><b>模块</b></td><td vertical-align="top"><b>所属模块</b></td><td vertical-align="top"><b>作用</b></td><td vertical-align="top"><b>触发条件/时机</b></td><td vertical-align="top"><b>运行频率</b></td><td vertical-align="top"><b>主要输入</b></td><td vertical-align="top"><b>主要输出</b></td><td vertical-align="top"><b>关系与说明</b></td></tr><tr><td vertical-align="top">数据输入</td><td vertical-align="top"></td><td vertical-align="top">提供中鱼系统所需的环境、投鱼和鱼习性相关数据。</td><td vertical-align="top">数据配置、编辑或运行时采样时。</td><td vertical-align="top"></td><td vertical-align="top"><ul><li>环境上下文</li><li>钓场投鱼配置</li><li>鱼的习性配置</li><li>玩家策略与操作数据</li></ul></td><td vertical-align="top">供烘焙、响应和后续抽鱼使用的输入数据。</td><td vertical-align="top">是其它模块的基础输入，不负责具体的因子计算。</td></tr><tr><td vertical-align="top">烘焙</td><td vertical-align="top"></td><td vertical-align="top">将相对低频变化的环境和鱼配置转化为可复用的中鱼相关结果。</td><td vertical-align="top"><ul><li>课程表滚动</li><li>修改配置</li><li>修改空间信息</li></ul></td><td vertical-align="top">低频：发生相关变化时重新烘焙。</td><td vertical-align="top"><ul><li>鱼配置</li><li>环境条件</li><li>适配条件 / 响应条件</li></ul></td><td vertical-align="top"><ul><li>派生环境权重场（DEF 派生环境场）</li><li>鱼空间结果（FishSpatialResult）</li><li>圆桌相关数据</li></ul></td><td vertical-align="top">为响应和圆桌抽鱼提供烘焙结果。内部计算细节不在本表展开。</td></tr><tr><td vertical-align="top">　├─ 烘焙因子运算</td><td vertical-align="top">烘焙</td><td vertical-align="top">针对单个因子，结合条件和鱼的行为模式进行评价。</td><td vertical-align="top">烘焙过程中。</td><td vertical-align="top">随烘焙执行。</td><td vertical-align="top"><ul><li>条件</li><li>因子</li></ul></td><td vertical-align="top"><ul><li>门控结果</li><li>亲和系数</li><li>因子结果</li></ul></td><td vertical-align="top">属于烘焙内部步骤，不单独构成对外模块。</td></tr><tr><td vertical-align="top">　├─ 烘焙通道聚合</td><td vertical-align="top">烘焙</td><td vertical-align="top">汇总同一条件组下多个因子的结果。</td><td vertical-align="top">相关因子计算完成后。</td><td vertical-align="top">随烘焙执行。</td><td vertical-align="top">多个因子结果。</td><td vertical-align="top">通道结果。</td><td vertical-align="top">属于烘焙内部步骤；具体聚合规则见烘焙专题。</td></tr><tr><td vertical-align="top">　├─ 行为模式结果集</td><td vertical-align="top">烘焙</td><td vertical-align="top">汇总同一条件组下多个 Engagement Mode 的空间结果，并协调不同模式之间的相对权重。</td><td vertical-align="top">条件组结果生成时。</td><td vertical-align="top">随烘焙执行。</td><td vertical-align="top">各 Engagement Mode 的通道结果。</td><td vertical-align="top">可复用的条件组与结果分桶。</td><td vertical-align="top">不按每个 x、y、z 位置重复保存相同条件组合。</td></tr><tr><td vertical-align="top">　├─ 烘焙结果输出</td><td vertical-align="top">烘焙</td><td vertical-align="top">整理并输出烘焙阶段生成的结果。</td><td vertical-align="top">一次烘焙完成后。</td><td vertical-align="top">低频：随烘焙结果更新。</td><td vertical-align="top">通道结果及其聚合结果。</td><td vertical-align="top"><ul><li>DEF 派生环境场</li><li>鱼空间结果</li><li>圆桌相关数据</li></ul></td><td vertical-align="top">供响应和圆桌抽鱼读取。</td></tr><tr><td vertical-align="top">响应</td><td vertical-align="top"></td><td vertical-align="top">结合烘焙结果和玩家当前策略，计算本次中鱼响应。</td><td vertical-align="top">持久响应和姿态响应分别在各自条件满足时触发。</td><td vertical-align="top">中频至高频，取决于响应类型。</td><td vertical-align="top"><ul><li>DEF 派生环境场</li><li>鱼空间结果</li><li>玩家操作信息</li><li>持久响应结果</li></ul></td><td vertical-align="top"><ul><li>响应结果</li><li>适配系数</li><li>中鱼等待时间</li><li>供圆桌抽鱼使用的结果</li></ul></td><td vertical-align="top">读取烘焙结果，不重新生成 DEF。</td></tr><tr><td vertical-align="top">├─ 持久响应</td><td vertical-align="top">响应</td><td vertical-align="top">计算持续生效的玩家行为对鱼情和中鱼结果的影响。</td><td vertical-align="top">玩家进行持久型操作时，例如打窝。</td><td vertical-align="top">中频：操作持续期间更新。</td><td vertical-align="top"><ul><li>玩家持久操作</li><li>DEF 派生环境场</li></ul></td><td vertical-align="top">持久响应场。</td><td vertical-align="top">为姿态响应提供持续生效的响应结果。位置移动是否属于本模块，暂不在此表裁定。</td></tr><tr><td vertical-align="top">　│　├─ 条件派生</td><td vertical-align="top">持久响应</td><td vertical-align="top">把持久操作数据整理为可供后续计算使用的条件。</td><td vertical-align="top">持久操作数据发生变化时。</td><td vertical-align="top">随持久响应更新。</td><td vertical-align="top"><ul><li>持久操作数据</li><li>已有派生结果</li></ul></td><td vertical-align="top"><ul><li>派生条件</li><li>必要的原始条件</li></ul></td><td vertical-align="top">这里使用“条件派生”，不把具体拆分算法作为模块名称。</td></tr><tr><td vertical-align="top">　│　├─ 因子运算</td><td vertical-align="top">持久响应</td><td vertical-align="top">根据持久响应条件评估相关因子。</td><td vertical-align="top">条件派生完成后。</td><td vertical-align="top">随持久响应更新。</td><td vertical-align="top">派生条件、因子和习性组件。</td><td vertical-align="top">持久响应因子结果。</td><td vertical-align="top">沿用统一的因子和习性组件语义。</td></tr><tr><td vertical-align="top">　│　└─ 系数聚合</td><td vertical-align="top">持久响应</td><td vertical-align="top">汇总持久响应中的相关因子结果。</td><td vertical-align="top">相关因子运算完成后。</td><td vertical-align="top">随持久响应更新。</td><td vertical-align="top">持久响应因子结果。</td><td vertical-align="top">持久响应场。</td><td vertical-align="top">具体系数和聚合规则见响应专题。</td></tr><tr><td vertical-align="top">　└─ 姿态响应</td><td vertical-align="top">响应</td><td vertical-align="top">根据当前姿态、饵和玩家操作计算即时响应结果。</td><td vertical-align="top">玩家姿态、饵或操作发生变化时。</td><td vertical-align="top">高频：随操作变化更新。</td><td vertical-align="top"><ul><li>持久响应数据</li><li>鱼空间结果</li><li>饵与姿态</li><li>玩家位置与操作</li><li>DEF 与圆桌相关数据</li></ul></td><td vertical-align="top"><ul><li>响应条件</li><li>适配系数</li><li>中鱼等待时间</li><li>鱼种</li></ul></td><td vertical-align="top">读取烘焙结果和持久响应结果，完成当前姿态下的即时计算。</td></tr><tr><td vertical-align="top">　　├─ 响应条件整理</td><td vertical-align="top">姿态响应</td><td vertical-align="top">将当前姿态、饵和操作整理为因子可使用的条件。</td><td vertical-align="top">姿态响应开始时。</td><td vertical-align="top">随姿态响应更新。</td><td vertical-align="top"><ul><li>鱼侧动态参数</li><li>饵</li><li>窝料</li><li>姿态</li><li>玩家位置与操作</li></ul></td><td vertical-align="top">原始条件与派生条件。</td><td vertical-align="top">使用“响应条件整理”作为人类可读名称；具体派生规则见响应专题。</td></tr><tr><td vertical-align="top">　　├─ 响应因子运算</td><td vertical-align="top">姿态响应</td><td vertical-align="top">根据响应条件评估当前相关因子。</td><td vertical-align="top">响应条件整理完成后。</td><td vertical-align="top">高频：随姿态响应更新。</td><td vertical-align="top">响应条件、因子、习性组件及 DEF 结果。</td><td vertical-align="top">响应因子结果。</td><td vertical-align="top">沿用统一的因子和习性组件语义，不另造一套响应因子体系。</td></tr><tr><td vertical-align="top">　　└─ 响应系数聚合</td><td vertical-align="top">姿态响应</td><td vertical-align="top">汇总响应因子结果，形成当前响应结果。</td><td vertical-align="top">响应因子运算完成后。</td><td vertical-align="top">高频：随姿态响应更新。</td><td vertical-align="top">响应因子结果及相关权重结果。</td><td vertical-align="top"><ul><li>空间分布权重</li><li>最终响应结果</li></ul></td><td vertical-align="top">环境系数、空间分布权重等公式不在本表展开。</td></tr><tr><td vertical-align="top">圆桌计算</td><td vertical-align="top"></td><td vertical-align="top">汇总响应和烘焙相关结果，为抽鱼提供统一的抽取依据。</td><td vertical-align="top">一次姿态响应完成后。</td><td vertical-align="top">按次执行。</td><td vertical-align="top"><ul><li>姿态响应结果</li><li>烘焙结果</li><li>投鱼配置</li></ul></td><td vertical-align="top">供抽鱼和生成使用的权重及控制结果。</td><td vertical-align="top">与响应汇合后进入抽鱼和生成。</td></tr><tr><td vertical-align="top">　├─ 权重组装</td><td vertical-align="top">圆桌计算</td><td vertical-align="top">汇总各路权重，形成抽鱼所需的权重结果。</td><td vertical-align="top">圆桌计算开始时。</td><td vertical-align="top">按次执行。</td><td vertical-align="top">烘焙和响应产生的权重结果。</td><td vertical-align="top">圆桌权重结果。</td><td vertical-align="top">具体权重算法见圆桌专题。</td></tr><tr><td vertical-align="top">　└─ 圆桌权重列表</td><td vertical-align="top">圆桌计算</td><td vertical-align="top">根据服务端规则对抽鱼权重进行额外调整。</td><td vertical-align="top">圆桌权重聚合后。</td><td vertical-align="top">按次执行。</td><td vertical-align="top">圆桌权重结果及服务端控制条件。</td><td vertical-align="top">调整后的抽鱼权重。</td><td vertical-align="top">仅服务端执行，具体规则另行定义。</td></tr><tr><td vertical-align="top">抽鱼和生成</td><td vertical-align="top"></td><td vertical-align="top">根据圆桌计算结果完成鱼种和鱼属性的抽取与生成。</td><td vertical-align="top">圆桌计算完成后。</td><td vertical-align="top">按次执行。</td><td vertical-align="top">抽鱼权重、投鱼配置及生成规则。</td><td vertical-align="top"><ul><li>鱼种</li><li>品质</li><li>大小</li><li>重量</li><li>生成的鱼对象</li></ul></td><td vertical-align="top">将生成结果交给 Fish AI 和后续玩法。</td></tr><tr><td vertical-align="top">Fish AI / 下游玩法</td><td vertical-align="top"></td><td vertical-align="top">处理刺鱼、博鱼以及鱼生成后的运行时行为。</td><td vertical-align="top">鱼对象生成后。</td><td vertical-align="top">运行时持续执行。</td><td vertical-align="top">生成的鱼对象及运行时状态。</td><td vertical-align="top">鱼的运行时行为。</td><td vertical-align="top">属于中鱼系统范围外的下游模块。</td></tr></tbody></table>

<table><colgroup><col/><col/><col/><col/><col/><col/><col/><col/></colgroup><tbody><tr><td vertical-align="top"><b>模块</b></td><td vertical-align="top"><b>所属模块</b></td><td vertical-align="top"><b>作用</b></td><td vertical-align="top"><b>触发条件/时机</b></td><td vertical-align="top"><b>运行频率</b></td><td vertical-align="top"><b>主要输入</b></td><td vertical-align="top"><b>主要输出</b></td><td vertical-align="top"><b>关系与说明</b></td></tr><tr><td vertical-align="top">数据输入</td><td vertical-align="top"></td><td vertical-align="top">提供中鱼系统所需的环境、投鱼和鱼习性相关数据。</td><td vertical-align="top">数据配置、编辑或运行时采样时。</td><td vertical-align="top">按数据来源而定。</td><td vertical-align="top"><ul><li>环境上下文</li><li>钓场投鱼配置</li><li>鱼的习性配置</li><li>玩家策略与操作数据</li></ul></td><td vertical-align="top">供烘焙、响应和后续抽鱼使用的输入数据。</td><td vertical-align="top">是其它模块的基础输入，不负责具体的因子计算。</td></tr><tr><td vertical-align="top">烘焙</td><td vertical-align="top"></td><td vertical-align="top">将相对低频变化的环境和鱼配置转化为可复用的中鱼相关结果。</td><td vertical-align="top"><ul><li>课程表滚动</li><li>修改配置</li><li>修改空间信息</li></ul></td><td vertical-align="top">低频：发生相关变化时重新烘焙。</td><td vertical-align="top"><ul><li>鱼配置</li><li>环境条件</li><li>适配条件 / 响应条件</li></ul></td><td vertical-align="top"><ul><li>派生环境权重场（DEF 派生环境场）</li><li>鱼空间结果（FishSpatialResult）</li><li>圆桌相关数据</li></ul></td><td vertical-align="top">为响应和圆桌抽鱼提供烘焙结果。内部计算细节不在本表展开。</td></tr><tr><td vertical-align="top">　├─ 烘焙因子运算</td><td vertical-align="top">烘焙</td><td vertical-align="top">针对单个因子，结合条件和鱼的行为模式进行评价。</td><td vertical-align="top">烘焙过程中。</td><td vertical-align="top">随烘焙执行。</td><td vertical-align="top"><ul><li>条件</li><li>因子</li><li>鱼 × 行为模式对应的习性组件</li></ul></td><td vertical-align="top"><ul><li>门控结果</li><li>亲和系数</li><li>因子结果</li></ul></td><td vertical-align="top">属于烘焙内部步骤，不单独构成对外模块。</td></tr><tr><td vertical-align="top">　├─ 烘焙通道聚合</td><td vertical-align="top">烘焙</td><td vertical-align="top">汇总同一条件组下多个因子的结果。</td><td vertical-align="top">相关因子计算完成后。</td><td vertical-align="top">随烘焙执行。</td><td vertical-align="top">多个因子结果。</td><td vertical-align="top">通道结果。</td><td vertical-align="top">属于烘焙内部步骤；具体聚合规则见烘焙专题。</td></tr><tr><td vertical-align="top">　├─ 行为模式结果集</td><td vertical-align="top">烘焙</td><td vertical-align="top">汇总同一条件组下多个 Engagement Mode 的空间结果，并协调不同模式之间的相对权重。</td><td vertical-align="top">条件组结果生成时。</td><td vertical-align="top">随烘焙执行。</td><td vertical-align="top">各 Engagement Mode 的通道结果。</td><td vertical-align="top">可复用的条件组与结果分桶。</td><td vertical-align="top">不按每个 x、y、z 位置重复保存相同条件组合。</td></tr><tr><td vertical-align="top">　├─ 烘焙结果输出</td><td vertical-align="top">烘焙</td><td vertical-align="top">整理并输出烘焙阶段生成的结果。</td><td vertical-align="top">一次烘焙完成后。</td><td vertical-align="top">低频：随烘焙结果更新。</td><td vertical-align="top">通道结果及其聚合结果。</td><td vertical-align="top"><ul><li>DEF 派生环境场</li><li>鱼空间结果</li><li>圆桌相关数据</li></ul></td><td vertical-align="top">供响应和圆桌抽鱼读取。</td></tr><tr><td vertical-align="top">响应</td><td vertical-align="top"></td><td vertical-align="top">结合烘焙结果和玩家当前策略，计算本次中鱼响应。</td><td vertical-align="top">持久响应和姿态响应分别在各自条件满足时触发。</td><td vertical-align="top">中频至高频，取决于响应类型。</td><td vertical-align="top"><ul><li>DEF 派生环境场</li><li>鱼空间结果</li><li>玩家操作信息</li><li>持久响应结果</li></ul></td><td vertical-align="top"><ul><li>响应结果</li><li>适配系数</li><li>中鱼等待时间</li><li>供圆桌抽鱼使用的结果</li></ul></td><td vertical-align="top">读取烘焙结果，不重新生成 DEF。</td></tr><tr><td vertical-align="top">├─ 持久响应</td><td vertical-align="top">响应</td><td vertical-align="top">计算持续生效的玩家行为对鱼情和中鱼结果的影响。</td><td vertical-align="top">玩家进行持久型操作时，例如打窝。</td><td vertical-align="top">中频：操作持续期间更新。</td><td vertical-align="top"><ul><li>玩家持久操作</li><li>DEF 派生环境场</li></ul></td><td vertical-align="top">持久响应场。</td><td vertical-align="top">为姿态响应提供持续生效的响应结果。位置移动是否属于本模块，暂不在此表裁定。</td></tr><tr><td vertical-align="top">　│　├─ 条件派生</td><td vertical-align="top">持久响应</td><td vertical-align="top">把持久操作数据整理为可供后续计算使用的条件。</td><td vertical-align="top">持久操作数据发生变化时。</td><td vertical-align="top">随持久响应更新。</td><td vertical-align="top"><ul><li>持久操作数据</li><li>已有派生结果</li></ul></td><td vertical-align="top"><ul><li>派生条件</li><li>必要的原始条件</li></ul></td><td vertical-align="top">这里使用“条件派生”，不把具体拆分算法作为模块名称。</td></tr><tr><td vertical-align="top">　│　├─ 因子运算</td><td vertical-align="top">持久响应</td><td vertical-align="top">根据持久响应条件评估相关因子。</td><td vertical-align="top">条件派生完成后。</td><td vertical-align="top">随持久响应更新。</td><td vertical-align="top">派生条件、因子和习性组件。</td><td vertical-align="top">持久响应因子结果。</td><td vertical-align="top">沿用统一的因子和习性组件语义。</td></tr><tr><td vertical-align="top">　│　└─ 系数聚合</td><td vertical-align="top">持久响应</td><td vertical-align="top">汇总持久响应中的相关因子结果。</td><td vertical-align="top">相关因子运算完成后。</td><td vertical-align="top">随持久响应更新。</td><td vertical-align="top">持久响应因子结果。</td><td vertical-align="top">持久响应场。</td><td vertical-align="top">具体系数和聚合规则见响应专题。</td></tr><tr><td vertical-align="top">　└─ 姿态响应</td><td vertical-align="top">响应</td><td vertical-align="top">根据当前姿态、饵和玩家操作计算即时响应结果。</td><td vertical-align="top">玩家姿态、饵或操作发生变化时。</td><td vertical-align="top">高频：随操作变化更新。</td><td vertical-align="top"><ul><li>持久响应数据</li><li>鱼空间结果</li><li>饵与姿态</li><li>玩家位置与操作</li><li>DEF 与圆桌相关数据</li></ul></td><td vertical-align="top"><ul><li>响应条件</li><li>适配系数</li><li>中鱼等待时间</li><li>鱼种</li></ul></td><td vertical-align="top">读取烘焙结果和持久响应结果，完成当前姿态下的即时计算。</td></tr><tr><td vertical-align="top">　　├─ 响应条件整理</td><td vertical-align="top">姿态响应</td><td vertical-align="top">将当前姿态、饵和操作整理为因子可使用的条件。</td><td vertical-align="top">姿态响应开始时。</td><td vertical-align="top">随姿态响应更新。</td><td vertical-align="top"><ul><li>鱼侧动态参数</li><li>饵</li><li>窝料</li><li>姿态</li><li>玩家位置与操作</li></ul></td><td vertical-align="top">原始条件与派生条件。</td><td vertical-align="top">使用“响应条件整理”作为人类可读名称；具体派生规则见响应专题。</td></tr><tr><td vertical-align="top">　　├─ 响应因子运算</td><td vertical-align="top">姿态响应</td><td vertical-align="top">根据响应条件评估当前相关因子。</td><td vertical-align="top">响应条件整理完成后。</td><td vertical-align="top">高频：随姿态响应更新。</td><td vertical-align="top">响应条件、因子、习性组件及 DEF 结果。</td><td vertical-align="top">响应因子结果。</td><td vertical-align="top">沿用统一的因子和习性组件语义，不另造一套响应因子体系。</td></tr><tr><td vertical-align="top">　　└─ 响应系数聚合</td><td vertical-align="top">姿态响应</td><td vertical-align="top">汇总响应因子结果，形成当前响应结果。</td><td vertical-align="top">响应因子运算完成后。</td><td vertical-align="top">高频：随姿态响应更新。</td><td vertical-align="top">响应因子结果及相关权重结果。</td><td vertical-align="top"><ul><li>空间分布权重</li><li>最终响应结果</li></ul></td><td vertical-align="top">环境系数、空间分布权重等公式不在本表展开。</td></tr><tr><td vertical-align="top">圆桌计算</td><td vertical-align="top"></td><td vertical-align="top">汇总响应和烘焙相关结果，为抽鱼提供统一的抽取依据。</td><td vertical-align="top">一次姿态响应完成后。</td><td vertical-align="top">按次执行。</td><td vertical-align="top"><ul><li>姿态响应结果</li><li>烘焙结果</li><li>投鱼配置</li></ul></td><td vertical-align="top">供抽鱼和生成使用的权重及控制结果。</td><td vertical-align="top">与响应汇合后进入抽鱼和生成。</td></tr><tr><td vertical-align="top">　├─ 权重组装</td><td vertical-align="top">圆桌计算</td><td vertical-align="top">汇总各路权重，形成抽鱼所需的权重结果。</td><td vertical-align="top">圆桌计算开始时。</td><td vertical-align="top">按次执行。</td><td vertical-align="top">烘焙和响应产生的权重结果。</td><td vertical-align="top">圆桌权重结果。</td><td vertical-align="top">具体权重算法见圆桌专题。</td></tr><tr><td vertical-align="top">　└─ 圆桌权重列表</td><td vertical-align="top">圆桌计算</td><td vertical-align="top">根据服务端规则对抽鱼权重进行额外调整。</td><td vertical-align="top">圆桌权重聚合后。</td><td vertical-align="top">按次执行。</td><td vertical-align="top">圆桌权重结果及服务端控制条件。</td><td vertical-align="top">调整后的抽鱼权重。</td><td vertical-align="top">仅服务端执行，具体规则另行定义。</td></tr><tr><td vertical-align="top">抽鱼和生成</td><td vertical-align="top"></td><td vertical-align="top">根据圆桌计算结果完成鱼种和鱼属性的抽取与生成。</td><td vertical-align="top">圆桌计算完成后。</td><td vertical-align="top">按次执行。</td><td vertical-align="top">抽鱼权重、投鱼配置及生成规则。</td><td vertical-align="top"><ul><li>鱼种</li><li>品质</li><li>大小</li><li>重量</li><li>生成的鱼对象</li></ul></td><td vertical-align="top">将生成结果交给 Fish AI 和后续玩法。</td></tr><tr><td vertical-align="top">Fish AI / 下游玩法</td><td vertical-align="top"></td><td vertical-align="top">处理刺鱼、博鱼以及鱼生成后的运行时行为。</td><td vertical-align="top">鱼对象生成后。</td><td vertical-align="top">运行时持续执行。</td><td vertical-align="top">生成的鱼对象及运行时状态。</td><td vertical-align="top">鱼的运行时行为。</td><td vertical-align="top">属于中鱼系统范围外的下游模块。</td></tr></tbody></table>

## 模块主线与数据流

中鱼系统的主要模块和数据流可以概括为：

```text
因子列表
  ↓
构造条件组
  ↓
条件组鱼筛选
  ↓
逐个计算当前条件组中的 Engagement Mode
  ↓
各 Engagement Mode 内逐项评估因子
  ↓
Engagement Mode 空间结果集
  ↓
写入 DEF 派生环境权重场

DEF ───────────────┐
                  ├─→ 响应
玩家策略与操作数据 ──┘
                  ↓
               适配系数
                  ↓
               圆桌抽鱼
                  ↓
               权重组装
                  ↓
            圆桌权重列表
                  ↓
               抽鱼和生成
                  ↓
            Fish AI / 下游玩法
```

烘焙阶段先根据因子列表构造条件组，再对每个条件组进行条件组鱼筛选，并计算需要保存的 Engagement Mode 空间结果集，最后写入 DEF。响应阶段读取 DEF，并结合玩家策略与操作数据计算适配系数。圆桌抽鱼使用适配系数和其它抽鱼输入组装最终权重，形成圆桌权重列表；抽鱼和生成再根据该列表完成抽鱼、生成等待时间和鱼对象生成。Fish AI / 下游玩法属于中鱼系统范围外的下游模块。

## 核心中间数据：DEF 派生环境权重场

### DEF 的作用

DEF（Derived Environment Field，派生环境权重场）是烘焙阶段生成的按条件组组织的结果 Map。它不为每个空间位置单独保存一份结果，而是将相同条件组合归并到同一个条件组，并在条件组下保存需要参与计算的 Engagement Mode 空间结果。

### DEF 的结构

```text
DEF 派生环境权重场
└── 条件组
    └── Engagement Mode 条目
        └── Engagement Mode 空间结果
```

一个条件组对应当前条件下需要保存的多条 Engagement Mode 条目，而不是只保存一个鱼种的几个模式。条件组鱼筛选会先从全部候选条目中筛出当前条件组需要计算和存储的条目，以额外判断时间换取 DEF 的存储空间。

示例：

```text
条件组 A
├── 鲤鱼 / 伏击模式
│   └── Engagement Mode 空间结果
├── 鲤鱼 / 开放游弋模式
│   └── Engagement Mode 空间结果
├── 草鱼 / 开放游弋模式
│   └── Engagement Mode 空间结果
└── 鲈鱼 / 伏击模式
    └── Engagement Mode 空间结果
```

### Engagement Mode 与因子计算

Engagement Mode 是烘焙计算的主要对象。当前过渡阶段，一个 Engagement Mode 条目仍可能通过“鱼种 + Engagement Mode”确定，但这属于输入组织方式，不改变 Engagement Mode 作为主要计算对象的定义。

对每个条件组，系统逐个计算经过条件组鱼筛选的 Engagement Mode。对某个 Engagement Mode，系统逐项处理因子：读取该因子对应的条件，索引该 Engagement Mode 对应的习性组件，再得到门控结果、亲和系数和因子结果。

```text
因子列表
  ↓
条件组合 → 条件组
  ↓
条件组鱼筛选
  ↓
Engagement Mode
  ↓
对应习性组件 × 因子条件
  ↓
因子结果
  ↓
Engagement Mode 空间结果
```

因子在 DEF 烘焙中承担两种角色：一方面，因子列表参与条件组合和条件组构造；另一方面，因子在每个 Engagement Mode 内被逐项评估。

### 结果层次

- **Engagement Mode 空间结果**：一个条件组下，一个 Engagement Mode 完成各因子计算和聚合后的空间相关结果。
- **Engagement Mode 空间结果集**：同一条件组下多个 Engagement Mode 的空间结果，以及模式之间的相对权重协调结果。多个模式结果保留，不压缩成单一结果。

模式之间可以进行整体平衡调整。例如某个模式的权重显著提高时，其他模式的权重可以适当降低，但各模式的空间结果仍保留在结果集中。

### 结果字段

单个 Engagement Mode 空间结果可以包含：

- 环境权重 / 空间分布强度
- Fish Conditions

Fish Conditions 包括：

- 进食动机（feeding motivation）
- 活跃度 / 活性（activity）
- 警戒度（wariness）
- 食性偏移（diet shift）

食性偏移不是鱼的基础食性范围，而是当前条件下，鱼在多个可接受饵种之间产生的相对偏向变化。

## 模块主线与数据流

中鱼系统的主要模块和数据流可以概括为：

```text
数据输入
  ├─ 环境上下文
  ├─ 投鱼配置
  └─ 鱼习性配置
        ↓
      烘焙
        ├─ 派生环境权重场（DEF）
        ├─ 鱼空间结果
        └─ 圆桌相关数据
                ↓
玩家策略与操作数据 ─→ 响应
                         ├─ 持久响应
                         └─ 姿态响应
                                  ↓
                             圆桌计算
                                  ↓
                             抽鱼和生成
                                  ↓
                           Fish AI / 下游玩法
```

环境上下文、投鱼配置和鱼习性配置主要在烘焙阶段进入计算；玩家策略与操作数据主要在响应阶段进入计算。烘焙结果由响应读取，持久响应结果继续供姿态响应使用。姿态响应完成后进入圆桌计算，圆桌结果再交给抽鱼和生成。Fish AI / 下游玩法属于中鱼系统范围外的下游模块。



# 因子、条件、习性、系数

一个因子是一个对中鱼产生影响的维度；条件、习性、系数都按照因子维度进行组织；

## 核心术语与数据结构

本节约定因子、条件、习性组件、派生环境权重场和鱼空间结果之间的关系。

### 因子与条件

- **因子**：代表一个中鱼运算中的影响因素，是系统进行独立评估、计算和聚合的对象。
- **条件**：代表鱼之外输入的数据。条件可以来自环境、配置、玩家策略或运行时状态，并作为因子运算的输入。

因此，条件是输入数据，因子是计算对象。例如，当前饵的速度值属于条件；“饵速度因子”是对该条件进行独立评估的运算对象。

### 习性组件

习性组件按两个维度组织：

- 行对应一个因子；
- 列对应一个鱼行为模式。

一个习性组件就是“鱼种 × 行为模式 × 因子”的交叉配置。它可以包含门控规则、亲和度规则、响应曲线以及参与聚合所需的参数。

例如，饵速度、震动、闪光都可以作为因子。它们的当前值属于条件；不同鱼种在不同鱼行为模式下如何评价这些值，则由对应的习性组件定义。

### 条件分类

为避免“一级条件 / 二级条件”只表达层级而不表达语义，本文采用以下名称：

- **原始条件**：直接配置、编辑、采样或运行时得到的数据。
- **派生条件**：由原始条件经过预处理、烘焙、采样或组合得到的可计算特征。

饵种、饵 ID、玩家操作轨迹、姿态、人物位置等通常是原始条件；饵速度、震动、闪光、饵轮廓、饵味型、线透明度等通常是派生条件。派生条件仍可继续生成更高阶特征，因此不强制限制为只有“第二级”。

### 派生环境权重场（DEF 派生环境场）

“派生环境场”是“派生环境权重场”的简称。英文为 **Derived Environment Field**，简称 **DEF**。

DEF 不是按每个 x、y、z 位置分别保存一份结果，而是把不同位置上相同的条件组合归并成条件组，再保存这些条件组对应的派生环境权重结果。因此，DEF 是一种按条件组合分桶和复用的派生环境场。

其结构可以理解为：

```text
DEF 派生环境场
└── 条件组：鱼情 Map
    └── 鱼种
        └── 鱼空间结果 struct
```

这里的“鱼情 Map”不表示每个空间坐标，而表示一个条件组下各鱼种的结果集合。空间位置通过条件组归并间接关联到这些结果。

### 鱼空间结果与 Fish Conditions

本文不使用“Fish Situation”或“鱼情参数”作为名称；该 Bake 结果结构称为**鱼空间结果**（**FishSpatialResult**），供 Response 模块作为输入。它按条件组归并不同空间位置上相同的条件组合，不逐个保存 x、y、z 位置。

除环境权重之外，鱼空间结果中的其它字段统称为 **Fish Conditions**：

- 进食动机（feeding motivation）
- 活跃度 / 活性（activity）
- 警戒度（wariness）
- 饵偏好偏移（baitPreferenceShift）

食性偏向可以继续表示为一个 Map：

```text
baitPreferenceShift map
└── 饵种 → 偏向度
```

### 环境系数与空间分布权重

**环境权重**不是适配度。表示适配度的是**环境系数**。

- 环境系数：表示当前环境对特定鱼种或计算对象的适配程度；
- 基础权重：表示不考虑当前环境适配结果时的基础权重；
- 环境权重 / 空间分布权重：由基础权重和环境系数共同得到。

**空间分布权重 = 基础权重 × 环境系数**

因此，“环境权重”与“环境系数”不能互相替换：前者是最终权重结果，后者是环境适配修正量。

## 概述

在处理数据的运算时，围绕着多个因子进行。

- 各个因子基本各自处理和计算
- 再对多个因子进行聚合

因子举例：

- 水温
- 气压
- 溶氧
- 食物浓度

因子、条件、习性组件三者关系见上方“核心术语与数据结构”。

- 一个因子（影响因子），指的是一个中鱼影响因素

  - 大部分情况下，因子和因子之间独立
  - 小部分情况下，因子之间关联无法避免，例如水温和溶氧
- 条件，指的是从外界，例如环境、当中来的因子数据
- 习性组件，是鱼的行为模式对于一个因子和条件的评价规则与结果

## 条件：

分类：

- 从数据推算顺序上来讲，可分为原始条件和派生条件。
- 从数据来源上来讲，可分为环境条件和适配条件。



### 条件分级

- 原始条件，指的是直接配置、编辑、采样或运行时得到的数据。包括：

  - 环境条件
  
    - 时段
    - 天气
    
      - 水表温度
      - 风力、风向
      - 气温
      - 天光强度
      - 气压
    - 结构体类型
    - 掩蔽物类型
    - 底质类型
    - 钓场水底温度
    - 深度
    - 到附近结构距离
    - 离岸距离
    - 季节/月份/日期
    - 特殊事件，例如 果树掉落、大量洄游等
  - 适配条件/响应条件
  
    - 饵
    
      - 饵种
      - 饵id
    - 姿态
    
      - 分为原子姿态和分子姿态
      - 包含姿态种类和姿态得分
    - 窝料
    - 线/引线
    - （玩家位置、声音）
- 派生条件，指的是由原始条件预处理、预烘焙、采样或组合出来的数据。包括：（如无特殊说明，这些条件数据指的都是特定饵点&特定策划选择下的数据）

  - 环境条件
  
    - 水温
    - 觅食生态水层
    - 光照
    - 溶氧
    - 水流流速
    - 浮游生物含量
    - 历史、未来天气序列摘要
  - 适配条件/响应条件
  
    - 饵轮廓
    - 饵味型
    - 饵速度
    - 闪光
    - 颜色
    - 震动
    - 声音
    - 线透明度、线颜色
    - 受伤、停顿
    - 等等……



# 习性模式

一个鱼种在本质上行为由其脑部神经网络驱动，不同情况下会做不同的取舍，过于复杂。为解决此问题，我们将鱼的习性分为几种习性模式，从而简化问题。

例如：

- 伏击模式下……
- 开放游弋模式下……
- 护巢护卵模式下……
- 





有一个默认模式











命名和语义讨论：

- 掩蔽物/遮蔽物
- 一级条件、二级条件，是否应当更名，例如：基础/衍生 派生 等等
- 因子、条件、习性组件的命名
- 响应内容 加入/不加入 因子/条件
