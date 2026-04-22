#!/usr/bin/env python3
"""Pre-scan recent papers and generate an intelligence report."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import re
import textwrap
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_PDF_DIR = ROOT / "raw_papers" / "pdf"
RAW_HTML_DIR = ROOT / "raw_papers" / "html"
DEFAULT_LIMIT = 12
DEFAULT_KEYWORDS = [
    "GraphSAGE",
    "Multi-Agent Reinforcement Learning",
    "QMIX",
    "MAPPO",
    "State Representation Learning",
    "Dimensionality Reduction",
    "Crowd Evacuation Simulation",
    "LLM Knowledge Distillation",
    "Dynamic Graphs",
]

WEIGHTS = {
    "graphsage": 5,
    "gnn": 3,
    "graph neural": 3,
    "state representation": 5,
    "representation learning": 4,
    "dimensionality reduction": 4,
    "marl": 5,
    "multi-agent": 4,
    "qmix": 5,
    "qplex": 4,
    "mappo": 5,
    "credit assignment": 5,
    "crowd": 4,
    "evacuation": 5,
    "dynamic graph": 5,
    "temporal graph": 4,
    "distillation": 4,
    "world model": 4,
    "llm": 4,
    "simulator": 3,
}


def fetch_url(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "GraphSAGE-Scout/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def sanitize_filename(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9._-]+", "_", text)
    return text.strip("_")[:100] or "paper"


def arxiv_query(keyword: str, max_results: int) -> list[dict]:
    query = urllib.parse.quote(f'all:"{keyword}"')
    url = (
        "https://export.arxiv.org/api/query?"
        f"search_query={query}&start=0&max_results={max_results}"
        "&sortBy=submittedDate&sortOrder=descending"
    )
    xml_bytes = fetch_url(url)
    root = ET.fromstring(xml_bytes)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    items: list[dict] = []

    for entry in root.findall("atom:entry", ns):
        paper_id = normalize_whitespace(entry.findtext("atom:id", default="", namespaces=ns))
        title = normalize_whitespace(entry.findtext("atom:title", default="", namespaces=ns))
        summary = normalize_whitespace(entry.findtext("atom:summary", default="", namespaces=ns))
        published = normalize_whitespace(entry.findtext("atom:published", default="", namespaces=ns))
        updated = normalize_whitespace(entry.findtext("atom:updated", default="", namespaces=ns))
        authors = [normalize_whitespace(author.findtext("atom:name", default="", namespaces=ns)) for author in entry.findall("atom:author", ns)]
        pdf_url = ""
        html_url = paper_id

        for link in entry.findall("atom:link", ns):
            href = link.attrib.get("href", "")
            title_attr = link.attrib.get("title", "")
            if title_attr == "pdf":
                pdf_url = href
            elif link.attrib.get("rel") == "alternate" and href:
                html_url = href

        items.append(
            {
                "keyword": keyword,
                "id": paper_id,
                "title": title,
                "summary": summary,
                "published": published,
                "updated": updated,
                "authors": authors,
                "pdf_url": pdf_url,
                "html_url": html_url,
            }
        )

    return items


def score_paper(paper: dict) -> tuple[int, list[str]]:
    haystack = f"{paper['title']} {paper['summary']}".lower()
    score = 0
    hits: list[str] = []

    for token, weight in WEIGHTS.items():
        if token in haystack:
            score += weight
            hits.append(token)

    if "github" in haystack or "code" in haystack:
        score += 2
        hits.append("code")
    if "crowd" in haystack and "evacuation" in haystack:
        score += 2
    if "graphsage" in haystack and ("qmix" in haystack or "mappo" in haystack or "multi-agent" in haystack):
        score += 4
    if "state representation" in haystack and ("qmix" in haystack or "mappo" in haystack or "multi-agent" in haystack):
        score += 3

    return score, sorted(set(hits))


def detect_themes(paper: dict) -> set[str]:
    haystack = f"{paper['title']} {paper['summary']}".lower()
    themes: set[str] = set()

    if any(token in haystack for token in ("graphsage", "gnn", "graph neural", "gat", "vgae")):
        themes.add("graph")
    if any(token in haystack for token in ("state representation", "representation learning", "dimensionality reduction")):
        themes.add("state")
    if any(token in haystack for token in ("multi-agent", "marl", "qmix", "qplex", "mappo", "credit assignment")):
        themes.add("marl")
    if any(token in haystack for token in ("dynamic graph", "temporal graph", "evolving graph", "time-varying graph")):
        themes.add("dynamic")
    if any(token in haystack for token in ("llm", "distillation", "world model", "teacher", "student")):
        themes.add("distill")
    if any(token in haystack for token in ("crowd", "evacuation", "social force", "simulator")):
        themes.add("sim")

    return themes


def triage(score: int, paper: dict) -> str:
    themes = paper["themes"]
    has_representation_angle = bool(themes & {"graph", "state", "dynamic", "distill"})
    has_marl_angle = "marl" in themes

    if score >= 18 and has_marl_angle and has_representation_angle and len(themes) >= 2:
        return "L3"
    if score >= 10 or len(themes) >= 2:
        return "L2"
    return "L1"


def dedupe(items: list[dict]) -> list[dict]:
    seen: dict[str, dict] = {}
    for item in items:
        current = seen.get(item["id"])
        if current is None or len(item["summary"]) > len(current["summary"]):
            seen[item["id"]] = item
    return list(seen.values())


def attempt_download(paper: dict) -> tuple[str, str]:
    slug = sanitize_filename(f"{paper['published'][:10]}_{paper['title']}")
    pdf_target = RAW_PDF_DIR / f"{slug}.pdf"
    html_target = RAW_HTML_DIR / f"{slug}.html"

    if paper["pdf_url"]:
        try:
            pdf_bytes = fetch_url(paper["pdf_url"])
            pdf_target.write_bytes(pdf_bytes)
            return "pdf", str(pdf_target.relative_to(ROOT))
        except urllib.error.URLError:
            pass

    if paper["html_url"]:
        html_bytes = fetch_url(paper["html_url"])
        html_target.write_bytes(html_bytes)
        return "html", str(html_target.relative_to(ROOT))

    return "none", "not-downloaded"


def render_section(label: str, rows: list[dict]) -> str:
    if not rows:
        return f"## {label}\n\n- 无命中。\n"

    lines = [f"## {label}", ""]
    for idx, paper in enumerate(rows, start=1):
        authors = ", ".join(paper["authors"][:4]) or "Unknown"
        if len(paper["authors"]) > 4:
            authors += ", et al."
        lines.extend(
            [
                f"### {idx}. {paper['title']}",
                f"- Score: `{paper['score']}` | Bucket: `{paper['bucket']}` | Published: `{paper['published'][:10]}`",
                f"- Query: `{paper['keyword']}` | Themes: `{', '.join(sorted(paper['themes'])) or 'unclear'}` | Evidence: `{', '.join(paper['hits'][:8]) or 'weak-match'}`",
                f"- Authors: {authors}",
                f"- PDF: {paper['pdf_url'] or 'N/A'}",
                f"- HTML: {paper['html_url'] or 'N/A'}",
                f"- Local Cache: `{paper.get('download_mode', 'skip')} / {paper.get('download_path', 'not-requested')}`",
                f"- Note: {textwrap.shorten(paper['summary'], width=240, placeholder=' ...')}",
                "",
            ]
        )
    return "\n".join(lines)


def build_report(papers: list[dict], report_date: str) -> str:
    l1 = [paper for paper in papers if paper["bucket"] == "L1"]
    l2 = [paper for paper in papers if paper["bucket"] == "L2"]
    l3 = [paper for paper in papers if paper["bucket"] == "L3"]

    lines = [
        f"# PRE_SCAN_REPORT_{report_date}",
        "",
        "## Scope",
        "",
        "- Source: `arXiv Atom API` recent keyword scan",
        f"- Keywords: `{', '.join(DEFAULT_KEYWORDS)}`",
        "- Priority venues to verify manually in the next pass: `ICLR`, `NeurIPS`, `AAMAS`",
        "- Objective: locate papers that reduce high-dimensional state complexity, improve MARL convergence, or stabilize dynamic graph policies",
        "",
        "## Executive Summary",
        "",
        f"- Total candidates after dedupe: `{len(papers)}`",
        f"- L3 focus: `{len(l3)}`",
        f"- L2 archive: `{len(l2)}`",
        f"- L1 discard: `{len(l1)}`",
        "- Heuristic reminder: venue rank and code availability still require a manual confirmation pass before deep deconstruction.",
        "",
    ]

    if l3:
        lines.extend(
            [
                "## L3 Quick Recommendation",
                "",
            ]
        )
        for paper in l3[:5]:
            lines.append(
                f"- `{paper['title']}`: 优先检查图编码是否与 QMIX / MAPPO 耦合、是否支持无监督预训练、是否报告收敛步数或疏散效率。"
            )
        lines.append("")

    lines.append(render_section("L3 / Focus", l3))
    lines.append(render_section("L2 / Archive", l2))
    lines.append(render_section("L1 / Discard", l1))

    lines.extend(
        [
            "## Next Actions",
            "",
            "- 对 L3 候选补充 venue、代码仓库、数据集与 reward 设计确认。",
            "- 若进入深拆，将报告归档到 `archive/` 对应主题目录。",
            "- 源码可用时克隆到 `repos/` 并审计图构建、PyG 健康度与 reward 塑形。",
            "",
        ]
    )
    return "\n".join(lines)


def ensure_dirs() -> None:
    RAW_PDF_DIR.mkdir(parents=True, exist_ok=True)
    RAW_HTML_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan recent papers and build a markdown pre-report.")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="Max results fetched for each keyword.")
    parser.add_argument("--download-limit", type=int, default=0, help="How many top-ranked papers to cache locally.")
    args = parser.parse_args()

    ensure_dirs()
    report_date = dt.date.today().isoformat()
    candidates: list[dict] = []

    for keyword in DEFAULT_KEYWORDS:
        try:
            candidates.extend(arxiv_query(keyword, args.limit))
        except Exception as exc:  # noqa: BLE001
            print(f"[warn] query failed for {keyword!r}: {exc}")

    papers = dedupe(candidates)
    for paper in papers:
        paper["score"], paper["hits"] = score_paper(paper)
        paper["themes"] = detect_themes(paper)
        paper["bucket"] = triage(paper["score"], paper)

    bucket_rank = {"L3": 0, "L2": 1, "L1": 2}
    papers.sort(key=lambda item: (bucket_rank[item["bucket"]], -item["score"], item["published"]), reverse=False)

    for paper in papers[: args.download_limit]:
        try:
            mode, path = attempt_download(paper)
        except Exception as exc:  # noqa: BLE001
            mode, path = "error", f"download-error: {html.escape(str(exc))}"
        paper["download_mode"] = mode
        paper["download_path"] = path

    report = build_report(papers, report_date)
    out_path = ROOT / f"PRE_SCAN_REPORT_{report_date}.md"
    out_path.write_text(report, encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
