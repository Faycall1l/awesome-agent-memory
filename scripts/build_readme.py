#!/usr/bin/env python3
"""Build README.md from data/entries.csv and README.template.md.

The output is deterministic: same CSV in, same README out, so CI can verify
that the committed README matches the data.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SECTIONS = [
    ("Surveys & SoKs", "The maps. Start with these if you are new to the area."),
    ("Foundations & position papers", "The papers that defined the problems, vocabulary and design space."),
    ("Memory systems & architectures", "End-to-end memory layers, runtimes and stores."),
    ("Graph, temporal & structured memory", "Knowledge graphs, trees, hypergraphs, bi-temporal stores and provenance."),
    ("Consolidation, forgetting & pruning", "What to merge, compress, decay, supersede or delete — and why."),
    ("Procedural memory, skills & experience", "Turning trajectories into reusable procedures, workflows and skills."),
    ("Control, triggering & self-evolution", "When to remember, when to recall and when to change the memory policy."),
    ("Trust, governance & security", "Provenance, authority, poisoning, privacy and safe consolidation."),
    ("Benchmarks: memory & long-horizon evaluation", "Datasets and harnesses that test memory over sessions and tasks."),
    ("Benchmarks: skills & procedural memory", "Evaluation of skill discovery, transfer, maintenance and safety."),
    ("Retrieval & context engineering", "Foundational results on what fits, what gets attended to and how to compress it."),
    ("Frameworks, libraries & tools", "Open-source software you can run today."),
    ("Articles, blogs & talks", "Practitioner writing that explains the design choices."),
    ("Related lists & communities", "Other curated collections worth following."),
]

START_HERE = [
    ("Memory in the Age of AI Agents: A Survey — Forms, Functions and Dynamics",
     "Start with the field map: forms, functions and dynamics."),
    ("Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers",
     "Then the write–manage–read formalism and the evaluation stack."),
    ("A Survey on the Memory Mechanism of Large Language Model based Agents",
     "The earlier taxonomy, and the audit that exposed the forgetting gap."),
    ("MemGPT: Towards LLMs as Operating Systems",
     "The OS analogy that made tiered memory mainstream."),
    ("Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory",
     "How a production memory layer extracts, consolidates and serves facts."),
    ("Zep: A Temporal Knowledge Graph Architecture for Agent Memory",
     "Temporal graphs and bi-temporal invalidation in practice."),
    ("FadeMem: Biologically-Inspired Forgetting for Efficient Agent Memory",
     "A concrete, reusable recipe for decay, promotion and fusion."),
    ("Evaluating Very Long-Term Conversational Memory of LLM Agents",
     "LoCoMo: the benchmark most memory systems still report on."),
]


def slug(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    return s.strip().replace(" ", "-")


def clean(text: str) -> str:
    return text.replace(" -- ", " — ")


def render_entry(row: dict) -> str:
    title = row["title"]
    link = row["link"]
    year = row["year"]
    desc = clean(row["description"])
    kind = row["kind"]

    if kind == "tool":
        line = f"- **[{title}]({link})** — {desc}"
    elif kind == "article":
        line = f"- **[{title}]({link})** ({year}) — {desc}"
    elif kind == "list":
        line = f"- **[{title}]({link})** — {desc}"
    else:
        line = f"- **[{title}]({link})** ({year}) — {desc}"

    if row["extra_url"]:
        line += f" · [{row['extra_label']}]({row['extra_url']})"
    return line


def main() -> None:
    with (ROOT / "data" / "entries.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    by_title = {r["title"]: r for r in rows}
    section_order = {name: i for i, (name, _) in enumerate(SECTIONS)}
    rows.sort(key=lambda r: section_order[r["section"]])

    counts = {name: sum(1 for r in rows if r["section"] == name) for name, _ in SECTIONS}
    kinds = {k: sum(1 for r in rows if r["kind"] == k) for k in ("paper", "tool", "article", "list")}
    stats = (
        f"{len(rows)} entries · {kinds['paper']} papers · {kinds['tool']} tools "
        f"· {kinds['article']} articles · {kinds['list']} related lists"
    )

    toc = "\n".join(
        f"- [{name}](#{slug(name)}) ({counts[name]})" for name, _ in SECTIONS
    )

    start = []
    for i, (title, why) in enumerate(START_HERE, 1):
        row = by_title[title]
        start.append(f"{i}. **[{title}]({row['link']})** ({row['year']}) — {why}")
    start_here = "\n".join(start)

    blocks: list[str] = []
    for name, blurb in SECTIONS:
        section_rows = [r for r in rows if r["section"] == name]
        if not section_rows:
            continue
        blocks.append(f"## {name}\n\n{blurb}\n")
        current_sub = None
        started = False
        for row in section_rows:
            sub = row["subsection"]
            if sub and sub != current_sub:
                if started:
                    blocks.append("")
                blocks.append(f"### {sub}\n")
                current_sub = sub
            blocks.append(render_entry(row))
            started = True
        blocks.append("")

    template = (ROOT / "README.template.md").read_text(encoding="utf-8")
    readme = (
        template.replace("{{STATS}}", stats)
        .replace("{{TOC}}", toc)
        .replace("{{START_HERE}}", start_here)
        .replace("{{SECTIONS}}", "\n".join(blocks).rstrip())
    )
    (ROOT / "README.md").write_text(readme, encoding="utf-8")
    print(f"wrote README.md with {len(rows)} entries")


if __name__ == "__main__":
    main()
