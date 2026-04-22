# PAPER_SOP

## 1. Scouting & Acquisition

1. 运行 `scripts/stealth_scout.py` 做预扫描，默认关注：
   - `GraphSAGE`
   - `Multi-Agent Reinforcement Learning`
   - `QMIX`
   - `MAPPO`
   - `State Representation Learning`
   - `Dimensionality Reduction`
   - `Crowd Evacuation Simulation`
   - `LLM Knowledge Distillation`
   - `Dynamic Graphs`
2. 优先下载 PDF 到 `raw_papers/pdf/`。
3. PDF 下载失败时强制回退为 HTML 存档到 `raw_papers/html/`。

## 2. Triaging

- `L1 / Discard`
  - 环境过于简单，如基础 GridWorld。
  - 无法确认代码或实验设置。
  - 未解释高维表征或收敛改善机制。
- `L2 / Archive`
  - 有新颖聚合器、探索机制或动态图模块。
  - 计算开销过高，不适合 20+ 智能体实时推断。
- `L3 / Focus`
  - 明确压缩高维状态空间。
  - 对 MARL 收敛速度或稳定性有定量改善。
  - 具备源码、可复现实验或明确工程迁移路径。

## 3. Source Audit

- 检查图构建逻辑：
  - Node 物理量是否覆盖静态场、动态场、局部交互。
  - Edge 是否由距离阈值、可见性或拓扑邻接驱动。
- 检查 GNN 实现：
  - PyG 或 DGL 是否健康，是否存在硬编码 batch 假设。
  - 是否支持无监督预训练或与 RL 解耦。
- 检查 RL 环境：
  - Reward 塑形是否稳定。
  - Credit assignment 是否清晰。
  - 动态图更新频率与策略更新时间是否匹配。

## 4. 极致拆解模板

每篇深拆报告必须完整覆盖以下 11 章：

0. 基本信息  
1. 今日锐评  
2. 图构建与模型架构  
3. 核心创新  
4. Loss 函数详解  
5. 关键指标  
6. 状态空间降维策略  
7. 动态图与时序稳定性  
8. 长尾与局限  
9. 优缺点总结  
10. 落地建议

## 5. Engineering Hooks

- 必须显式审计静态场与动态场是否物理隔离嵌入。
- 必须记录无监督 GNN 能否脱离 Reward 预训练。
- 必须评估未来用 LLM 生成环境 embedding 的替换接口成本。

## 6. 同步要求

- 新增深拆后同步更新 `knowledge_graph.md`。
- 运行 `generate_agent_graph.py` 刷新 `MARL_Graph_Topology.html`。
- 如仓库已启用 Git，再执行提交与远端推送。
