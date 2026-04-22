#!/usr/bin/env python3
"""Generate a 3D topology view for the research stack."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SPEC_PATH = ROOT / "scripts" / "graph_topology.json"
OUTPUT_PATH = ROOT / "MARL_Graph_Topology.html"


def load_spec() -> dict:
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


def build_html(spec: dict) -> str:
    nodes = spec["nodes"]
    edges = spec["edges"]
    title = spec.get("title", "MARL Graph Topology")

    node_json = json.dumps(nodes, ensure_ascii=False, indent=2)
    edge_json = json.dumps(edges, ensure_ascii=False, indent=2)

    return f"""<!DOCTYPE html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{title}</title>
  <script src=\"https://cdn.plot.ly/plotly-2.35.2.min.js\"></script>
  <style>
    :root {{
      --bg: #0d1b1e;
      --panel: #13272b;
      --ink: #e7f4ef;
      --muted: #92b5ab;
      --accent: #79c7b7;
    }}
    body {{
      margin: 0;
      font-family: \"Helvetica Neue\", \"Noto Sans SC\", sans-serif;
      background:
        radial-gradient(circle at top left, rgba(121, 199, 183, 0.18), transparent 30%),
        linear-gradient(180deg, #081214 0%, var(--bg) 100%);
      color: var(--ink);
    }}
    header {{
      padding: 24px 28px 8px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 28px;
      letter-spacing: 0.02em;
    }}
    p {{
      margin: 0;
      color: var(--muted);
      max-width: 840px;
      line-height: 1.6;
    }}
    #graph {{
      width: 100%;
      height: 78vh;
    }}
  </style>
</head>
<body>
  <header>
    <h1>{title}</h1>
    <p>3D topology of environment encoding, graph representation learning, MARL control, dynamic graph stabilization, and LLM distillation pathways.</p>
  </header>
  <div id=\"graph\"></div>
  <script>
    const nodes = {node_json};
    const edges = {edge_json};

    const palette = {{
      env: \"#4cc9f0\",
      gnn: \"#90be6d\",
      marl: \"#f9c74f\",
      dynamic: \"#f9844a\",
      llm: \"#f94144\",
      deploy: \"#c77dff\"
    }};

    const edgeTraces = edges.map((edge) => {{
      const source = nodes.find((node) => node.id === edge.source);
      const target = nodes.find((node) => node.id === edge.target);
      return {{
        type: \"scatter3d\",
        mode: \"lines\",
        x: [source.x, target.x],
        y: [source.y, target.y],
        z: [source.z, target.z],
        line: {{
          color: \"rgba(231, 244, 239, 0.28)\",
          width: 3
        }},
        hoverinfo: \"text\",
        text: [`${{source.label}} -> ${{target.label}}<br>${{edge.relation}}`, `${{source.label}} -> ${{target.label}}<br>${{edge.relation}}`],
        showlegend: false
      }};
    }});

    const nodeTrace = {{
      type: \"scatter3d\",
      mode: \"markers+text\",
      x: nodes.map((node) => node.x),
      y: nodes.map((node) => node.y),
      z: nodes.map((node) => node.z),
      text: nodes.map((node) => node.label),
      textposition: \"top center\",
      hovertemplate: \"%{{text}}<br>%{{customdata}}<extra></extra>\",
      customdata: nodes.map((node) => `${{node.group}} | priority=${{node.priority}}`),
      marker: {{
        size: nodes.map((node) => 10 + node.priority * 4),
        color: nodes.map((node) => palette[node.group] || \"#79c7b7\"),
        line: {{ color: \"#f1faee\", width: 1.2 }},
        opacity: 0.92
      }},
      showlegend: false
    }};

    const layout = {{
      paper_bgcolor: \"rgba(0,0,0,0)\",
      plot_bgcolor: \"rgba(0,0,0,0)\",
      margin: {{ l: 0, r: 0, t: 8, b: 0 }},
      scene: {{
        xaxis: {{ title: \"Research Phase\", gridcolor: \"rgba(255,255,255,0.08)\", zerolinecolor: \"rgba(255,255,255,0.1)\" }},
        yaxis: {{ title: \"Model Depth\", gridcolor: \"rgba(255,255,255,0.08)\", zerolinecolor: \"rgba(255,255,255,0.1)\" }},
        zaxis: {{ title: \"Deployment Readiness\", gridcolor: \"rgba(255,255,255,0.08)\", zerolinecolor: \"rgba(255,255,255,0.1)\" }},
        bgcolor: \"rgba(0,0,0,0)\",
        camera: {{
          eye: {{ x: 1.6, y: 1.3, z: 1.05 }}
        }}
      }},
      font: {{
        color: \"#e7f4ef\"
      }}
    }};

    Plotly.newPlot(\"graph\", [...edgeTraces, nodeTrace], layout, {{ responsive: true, displaylogo: false }});
  </script>
</body>
</html>
"""


def main() -> None:
    spec = load_spec()
    html = build_html(spec)
    OUTPUT_PATH.write_text(html, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
