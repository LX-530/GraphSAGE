# [Paper Title]

## 0. 基本信息

- 时间:
- Venue:
- 单位:
- 任务:
- 代码:
- Tags:

## 1. 🔪 今日锐评

用不少于 200 字说明该工作是否真正缓解了高维状态空间、局部观测缺失和 MARL 收敛困难的问题。

## 2. 🏗️ 图构建与模型架构 (Graph & Architecture)

- Node 物理量:
- Edge 连接规则:
- 邻域采样策略:
- GNN -> RL Tensor Shape:
- 静态场 / 动态场是否解耦:

## 3. 💡 核心创新 (Math & Pseudo-code)

- GNN 聚合公式:
- RL 更新公式:
- 物理量纲解释:
- PyTorch 风格伪代码:

## 4. 📉 Loss 函数详解

- GNN 无监督目标:
- RL TD / Policy Loss:
- 联合训练还是解耦训练:

## 5. 📊 关键指标 (SOTA Compare)

- Timesteps to Converge:
- Evacuation Time:
- Survival / Escape Rate:
- 与 GraphSAGE-QMIX / MAPPO / G2RL 对比:

## 6. 📂 状态空间降维策略

说明如何把密度场、火灾场、静态障碍物和邻居交互压缩成低维 embedding。

## 7. 🧩 动态图与时序稳定性 (Dynamic Topology)

说明边断连/重连、时序缓存、消息滞后与稳定化策略。

## 8. ⚠️ 长尾与局限 (Corner Cases)

- 死锁:
- 冷启动:
- Oversmoothing:
- 稀疏奖励:

## 9. ⚖️ 优缺点总结

- 表征精度:
- 推断延迟:
- 可扩展性:
- 向 LLM 蒸馏迁移潜力:

## 10. 🛠️ 落地建议 (Deployment)

- AnyLogic / 自研仿真引擎接入难度:
- Neighbor Sampling 工程成本:
- 预训练与在线微调策略:
