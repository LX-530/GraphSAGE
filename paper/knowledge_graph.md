# Knowledge Graph

## Evolution Spine

1. `Static / Dynamic Field Encoding`
2. `Unsupervised GNN Compression`
3. `MARL Credit Assignment`
4. `Dynamic Topology Stabilization`
5. `LLM World Modeling & Distillation`
6. `Simulation Deployment`

## Lineage Map

| Layer | Core Methods | What It Solves | Next Hop |
| --- | --- | --- | --- |
| Env Sim | Cellular Automata, Social Force, CrowdNav | 将墙体、出口、火势、人流转成可计算状态 | GNN encoder |
| GNN Encoder | GraphSAGE, GAT, VGAE, contrastive SRL | 压缩高维局部邻域与场变量 | QMIX / MAPPO |
| MARL Policy | VDN, QMIX, QTRAN, QPLEX, MAPPO | 多智能体协同与 credit assignment | Dynamic graph policy |
| Dynamic Graph | EvolveGCN, TGN, DyRep, temporal attention | 处理边实时断连与重连 | Distillation |
| LLM Distill | World model distillation, trajectory summarization, simulator teacher | 将复杂图状态迁移到高层语义模型 | Deployment |
| Deployment | RLlib, SB3, PyG, AnyLogic bridge | 接入仿真引擎与在线推断 | Continuous audit |

## Priority Nodes

- `GraphSAGE -> QMIX`: 适合做局部邻域聚合后再混合个体 Q 值，优先检查是否存在 oversmoothing 与 credit leakage。
- `GraphSAGE -> MAPPO`: 适合做共享编码器，优先检查 centralized critic 对动态图的鲁棒性。
- `Dynamic Graph -> MAPPO/QMIX`: 关注边更新频率、邻居采样与时序稳定性。
- `GNN Pre-train -> RL Fine-tune`: 优先寻找可脱离 reward 的表征预训练路径。
- `LLM Distiller -> Simulator`: 预留把图 embedding 映射成文本或 latent token 的接口。

## Audit Questions

- 是否显式解耦静态场与动态场？
- 是否提供无监督重构、对比学习或 next-state 预测目标？
- 是否给出 timesteps to converge、evacuation time、survival rate？
- 是否具备 20+ agent 的实时推断可能性？

## Next Updates

- 将 L3 论文挂到对应层并标注代码仓库路径。
- 为每一篇深拆补充“降维收益 / 延迟成本 / 蒸馏友好度”三元标签。
