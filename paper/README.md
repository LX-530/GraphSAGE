# GraphSAGE Research Pipeline

面向图表示学习、多智能体强化学习与大模型蒸馏的研究流水线骨架。

## 目标

- 工作日 08:00 自动预扫描最新论文与源码线索。
- 用户唤醒后进入 L2/L3 深度拆解与源码审计。
- 统一沉淀到 `archive/`、`knowledge_graph.md` 与 `MARL_Graph_Topology.html`。

## 目录

- `archive/`: 深拆报告归档。
- `repos/`: L3 论文源码审计镜像目录。
- `raw_papers/`: 原始 PDF/HTML 存档。
- `scripts/`: 预扫描与流水线脚本。
- `generate_agent_graph.py`: 3D 拓扑生成器。
- `knowledge_graph.md`: 技术演化索引。
- `PAPER_SOP.md`: 拆解与审计标准。

## 常用命令

```bash
python3 scripts/stealth_scout.py --limit 12 --download-limit 3
python3 generate_agent_graph.py
python3 scripts/run_pipeline.py --limit 12 --download-limit 3
```

## 运行结果

- 预扫描报告输出到 `PRE_SCAN_REPORT_YYYY-MM-DD.md`
- 下载素材落到 `raw_papers/pdf/` 或 `raw_papers/html/`
- 可视化更新到 `MARL_Graph_Topology.html`

## 当前实现说明

当前版本使用 arXiv Atom API 做预扫描，并对 GraphSAGE、MARL、动态图、状态表征学习和 LLM 蒸馏相关关键词做启发式分级。后续可接入 OpenReview、Semantic Scholar 或手工白名单 venue feed。
