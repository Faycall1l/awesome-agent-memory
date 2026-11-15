#!/usr/bin/env python3
"""Regenerate data/entries.csv from the curation tables below.

data/entries.csv is the source of truth for README rendering; this script is
the record of *how* that CSV was curated: which arXiv papers were screened in,
in which section, and why each one is worth reading.

Paper titles and years are pinned in data/arxiv_meta.json so the build is
offline and deterministic. Regenerate the cache against the arXiv API with:

    python scripts/gen_entries.py --refresh

That call is slow (one request per 50 papers, with a 3 s pause between calls)
and is only needed when adding a new arXiv paper.

Usage:
    python scripts/gen_entries.py            # rebuild data/entries.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "arxiv_meta.json"
CSV_PATH = ROOT / "data" / "entries.csv"
FIELDS = [
    "section",
    "subsection",
    "title",
    "year",
    "link",
    "extra_label",
    "extra_url",
    "description",
    "kind",
]

from build_readme import SECTIONS  # noqa: E402  (single source of section order)

ATOM = "{http://www.w3.org/2005/Atom}"

PAPERS = {
"Surveys & SoKs": [
("2512.13564", "The current field map: forms (token, parametric, latent), functions (factual, experiential, working) and dynamics (formation, evolution, retrieval), plus benchmarks and frameworks.", None),
("2603.07670", "Formalizes memory as a write-manage-read loop, compares five mechanism families and names consolidation, forgetting and causally grounded retrieval as open problems.", None),
("2602.05665", "Graph memory from extraction to evolution: knowledge graphs, hierarchies, temporal graphs and hypergraphs, with a large benchmark and library index.", None),
("2602.06052", "A 2026 survey of the field's \"second half\": self-evolving, long-horizon memory that must accumulate and reuse experience across real tasks.", None),
("2404.13501", "Early systematic survey of memory sources, forms, operations and evaluation; its 28-system audit shows forgetting is called core but rarely implemented.", None),
("2504.15965", "Maps human memory constructs onto LLM and agent memory mechanisms; useful for vocabulary and design inspiration.", None),
("2504.02441", "Cognitive-architecture reading of memory in LLMs: encoding, storage, consolidation, retrieval and forgetting.", None),
("2607.10113", "Lifecycle survey of evolving skill libraries over 124 papers, with a shared vocabulary of ten update operators.", None),
("2602.20867", "Systematization of agentic skills as callable modules with applicability conditions, execution policies and termination criteria.", None),
("2605.07358", "Taxonomy of skill acquisition, representation, retrieval, composition and evolution, with techniques and applications.", None),
("2604.08224", "Treats memory, skills, protocols and harnesses as one story: capabilities externalized outside model weights.", None),
("2603.10062", "Position paper framing multi-agent memory as a computer-architecture problem: shared vs distributed memory, cache protocols and consistency.", None),
],
"Foundations & position papers": [
("2304.03442", "Observation stream, periodic reflection and recency/relevance/importance retrieval; the design most agent-memory papers still build on.", None),
("2303.11366", "Stores verbal self-critiques after failures and retries with them; a minimal experiential-learning loop.", None),
("2310.08560", "OS-inspired virtual context: pages information between main context, recall storage and archival storage.", "https://github.com/letta-ai/letta"),
("2305.16291", "Lifelong Minecraft agent that writes executable, self-verified skills into an ever-growing library.", None),
("2308.10144", "Compares successes and failures across tasks to extract reusable natural-language insights.", None),
("2309.02427", "Cognitive architecture for language agents with working, episodic, semantic and procedural memory, plus an explicit action space.", None),
("HATALIS", "Position paper: vector databases are not long-term memory; episodic, semantic and procedural stores need separate management.", None),
("2606.24775", "Asks what an agent-native memory system should be and argues end-to-end scores hide cost, module trade-offs and update robustness.", None),
("2606.14997", "Parametric view of memory: identifies manipulable \"engrams\" in network weights using specificity, reactivation, sufficiency and necessity.", None),
],
"Memory systems & architectures": [
("2504.19413", "Production memory layer: extracts salient facts, consolidates them and serves them from vector, graph and key-value stores.", "https://github.com/mem0ai/mem0"),
("2501.13956", "Temporal knowledge graph memory with bi-temporal edge invalidation; the paper behind Graphiti.", "https://github.com/getzep/graphiti"),
("2502.12110", "Zettelkasten-style notes with LLM-generated keywords, links and in-place evolution of neighbouring memories.", "https://github.com/WujiangXu/A-mem"),
("2510.15966", "Piaget-inspired Pool-Bucket-Schema memory with update/evolve/create modes and hybrid symbolic + neural retrieval.", None),
("2604.22085", "Typed semantic memory with 13 categories, versioning and conflict handling, built on a zero-ingestion-cost information-theoretic retriever.", None),
("2506.06326", "OS-style memory with short-, mid- and long-term tiers, segmented paging and heat-based eviction.", "https://github.com/BAI-LAB/MemoryOS"),
("2507.03724", "Memory operating system unifying plaintext, activation and parameter memory under a scheduling layer.", "https://github.com/MemTensor/MemOS"),
("2410.14052", "MemTree: hierarchical memory that clusters and abstracts conversations into a dynamic tree of schema-like nodes.", None),
("2305.10250", "Long-term dialogue memory with daily summarisation and Ebbinghaus-style decay of memory strength.", None),
("2606.09900", "Engram: dual-process memory with a cheap append-only write path, asynchronous bi-temporal consolidation and hybrid retrieval.", None),
("2607.13157", "Oracle Agent Memory as a database-native substrate: lifecycle, scoping, latency-bounded retrieval and revision/removal.", None),
("2507.07957", "MIRIX: multi-agent memory with six typed memory components coordinated by a meta-manager.", "https://github.com/Mirix-AI/MIRIX"),
("2605.28773", "FluxMem: treats memory as continuously evolving connectivity rather than a static store with fixed retrieval.", None),
("2605.23986", "MemForest: parallel, write-efficient extraction with hierarchical temporal indexing for low-latency updates.", None),
("2607.13591", "Learns when to retrieve, retrieve again or reuse a plan instead of applying one fixed memory heuristic.", None),
],
"Graph, temporal & structured memory": [
("2407.04363", "AriGraph: online triplet extraction plus episodic hyperedges, giving an agent a plannable graph world model.", "https://github.com/AIRI-Institute/AriGraph"),
("2405.14831", "HippoRAG: hippocampus-inspired graph index over a corpus for multi-hop, single-step retrieval.", "https://github.com/OSU-NLP-Group/HippoRAG"),
("2502.14802", "HippoRAG 2: adds dense retrieval and passage-level evidence to the graph index for continual non-parametric learning.", "https://github.com/OSU-NLP-Group/HippoRAG"),
("2404.16130", "GraphRAG: entity graph plus community summaries for global, query-focused summarisation.", "https://github.com/microsoft/graphrag"),
("2410.05779", "LightRAG: lightweight dual-level graph retrieval with incremental updates.", "https://github.com/HKUDS/LightRAG"),
("2401.18059", "RAPTOR: recursively clusters and summarises text into a tree for multi-level retrieval.", "https://github.com/parthsarthi03/raptor"),
("2507.06229", "Agent KB: cross-domain experience library with retrieval and reranking of reusable problem-solving strategies.", None),
("2608.12476", "GPM: source-bound bi-temporal state transitions with executable admission, conflict-isolation and release contracts.", None),
("2606.06240", "TOKI: types contradiction-resolution heuristics as bi-temporal operators with explicit isolation levels and audit rows.", None),
("2607.26520", "Neo4j + HNSW memory store separating identity from versions for point-in-time retrieval without overwriting history.", None),
("2608.16114", "HyperSkill: hypergraph-structured skill memory that preserves compositional relations among procedures.", None),
("2609.08228", "SE-GoS: distils execution traces into a self-evolving graph of skills for dependency-aware retrieval at scale.", None),
("2608.05604", "SkillZip: compresses skill graphs while preserving procedural contracts to fit a bounded context budget.", None),
("2609.02217", "SkillGLoW: groups related procedures into families and consolidates them for long-horizon task streams.", None),
],
"Consolidation, forgetting & pruning": [
("2601.18642", "FadeMem: differential Ebbinghaus decay across two layers, with LLM-guided conflict resolution and fusion; 45% smaller store.", None),
("2604.20300", "FSFM: selective forgetting that combines hippocampal indexing with forgetting curves.", None),
("2607.08032", "Rate-distortion account of memory compaction, unifying KV-cache eviction, context compression and agent-store pruning.", None),
("2610.12124", "Hippocam: hierarchical memory where use reinforces experience and disuse decays it, with intent-structured consolidation.", None),
("2608.22215", "Fast write routing plus slow background consolidation to avoid monotonic memory growth and retrieval decay.", None),
("2605.09315", "Measures non-monotonic capability degradation in self-evolving agents across skills, workflows, weights and memory.", None),
("2609.33013", "Shifts evaluation from how much is remembered to whether consolidation decisions and their authority are sound.", None),
("2504.13171", "Sleep-time compute: moves consolidation and reasoning into idle time so the critical path stays cheap.", None),
("2608.21964", "Shows repository-specific skills silently go stale and measures how to detect and repair them.", None),
("2609.10750", "34k-skill router study: synthetic fine-tuning improves in-distribution retrieval but causes catastrophic forgetting.", None),
("2606.15390", "Separates generating a skill from deciding whether it helps; measures and repairs harmful accumulated knowledge.", None),
("2605.12978", "Finds that repeatedly rewriting consolidated abstractions with an LLM can make them less reliable than raw episodic traces.", None),
],
"Procedural memory, skills & experience": [
("2409.07429", "Agent Workflow Memory: induces reusable workflows from past trajectories and injects them into future tasks.", None),
("2508.06433", "Memp: distils trajectories into step-level instructions and higher-level scripts for learnable procedural memory.", None),
("2512.10696", "ReMe: dynamic procedural memory that refines, recombines and retires knowledge instead of accumulating it passively.", "https://github.com/agentscope-ai/ReMe"),
("2603.25158", "Trace2Skill: consolidates many trajectories in parallel into a transferable skill directory.", None),
("2604.04804", "SkillX: automatically builds a shared, cross-agent skill knowledge base from experience.", None),
("2602.08234", "SkillRL: extracts reusable behavioural patterns and feeds them back into recursive skill-augmented RL.", None),
("2602.02474", "MemSkill: makes memory operations themselves learnable skills instead of fixed extraction prompts.", None),
("2605.06614", "SkillOS: learns a curation policy for streaming tasks -- when to add, merge, keep or prune skills.", None),
("2610.19386", "STRATA: typed multi-level experience graph separating trajectories, distilled workflows and reasoning items.", None),
("2611.04003", "WASP-Mem: lets the agent organise its own procedural memory while humans focus on diagnosis.", None),
("2610.27377", "REM: jointly decides what to store, when to recall and what to forget for coding agents.", None),
("2611.01386", "Zep Agent Skills: compiles verified traces into curated, deployable skills in a production service.", None),
("2602.01869", "Skill-Pro: non-parametric PPO that learns reusable skills from interaction without weight updates.", None),
("2610.05303", "ASCENT: online test-time training by self-distilling verified experience into future attempts.", None),
("2610.08048", "DAEDALUS: bootstraps operational memory from self-generated tasks when no human guidance is available.", None),
("2608.22533", "CONTRAMEM: learns procedural memory by contrasting trajectories from multiple models.", None),
("2605.27366", "MUSE-Autoskill: unified skill creation, memory, management and evaluation lifecycle.", None),
("2311.05997", "JARVIS-1: memory-augmented multimodal agent with self-check and an accumulating skill library.", None),
("2407.15325", "Odyssey: open-world Minecraft skill library with composable routines and a skill-management pipeline.", None),
("2605.18401", "SkillsVote: lifecycle governance for open skill ecosystems -- collection, recommendation and evolution.", None),
],
"Control, triggering & self-evolution": [
("2610.23574", "Darwin-Claw: environment-adaptive consolidation instead of indiscriminate injection of raw trajectories.", None),
("2610.00704", "SkillSpec: consensus-gated skill evolution with representation specialisation.", None),
("2609.36746", "EASE: behaviour-adaptive skill curation modelled against the downstream executor.", None),
("2605.29668", "GRASP: accepts a proposed skill only when it improves the target task without regressing earlier ones.", None),
("2605.08386", "SkillLens: adaptive multi-granularity skill reuse to cut injected context while keeping relevance.", None),
("2609.02253", "APEx: distils procedural experience and couples it to policy adaptation for deep-research QA.", None),
("2611.05636", "Route to Remember: learns when to use text memory and when to move knowledge into weights.", None),
("2610.21791", "RSIFlow: adaptive self-improvement workflows with an evolving meta-agent.", None),
("2610.18807", "SkillScaffold: policy-adaptive credit assignment and selective skill injection for agentic RL.", None),
("2603.09716", "AutoAgent: evolving cognition plus elastic memory orchestration for non-stationary environments.", None),
],
"Trust, governance & security": [
("2608.01679", "Benchmark for authority collapse: consolidated memory later consumed as instruction rather than testimony.", None),
("2603.11768", "SSGM: governance framework for semantic drift, privacy and stability in evolving memory.", None),
("2606.25161", "TRUSTMEM: learns trustworthy write/revise/delete operations and guards against omission and hallucinated consolidation.", None),
("2607.27080", "MemSecBench: tracks memory poisoning from persistence through consequence to repair.", None),
("2605.27825", "MRMMIA: membership-inference attacks against chat-agent memory, with privacy implications.", None),
("2610.05176", "AECG: asymmetric consolidation and governance to stop polluted procedures spreading in multi-agent systems.", None),
("2611.04299", "Shows that benign skills can compose into harmful capabilities; argues for skill-level safety evaluation.", None),
],
"Benchmarks: memory & long-horizon evaluation": [
("2402.17753", "LoCoMo: very long multi-session conversations with single-hop, multi-hop, temporal and adversarial recall questions.", "https://github.com/snap-research/locomo"),
("2410.10813", "LongMemEval: five long-term abilities -- information extraction, multi-session reasoning, temporal reasoning, knowledge updates and abstention.", "https://github.com/xiaowu0162/LongMemEval"),
("2507.05257", "MemoryAgentBench: incremental multi-turn evaluation of retrieval, test-time learning, long-range understanding and conflict resolution.", "https://github.com/HUST-AI-HYZ/MemoryAgentBench"),
("2506.21605", "MemBench: effectiveness and efficiency evaluation across participation, multi-turn, multi-session and multi-scenario settings.", "https://github.com/import-myself/Membench"),
("2511.03506", "HaluMem: operation-level hallucination evaluation for memory extraction, update and retrieval, not just final answers.", "https://github.com/MemTensor/HaluMem"),
("2602.16313", "MemoryArena: interdependent multi-session agentic tasks where memory must support later actions, not just recall.", None),
("2604.20006", "From Recall to Forgetting: evaluates consolidation and knowledge updates as personal circumstances change.", None),
("2608.02613", "MemArena: on-device, ego-centric personal-memory benchmark at scale, with trustworthiness dimensions.", None),
("2505.11942", "LifelongAgentBench: evaluates agents as lifelong learners across sequential tasks and domains.", None),
("2406.08747", "StreamBench: benchmarks continuous improvement from feedback over task streams.", None),
("2502.09597", "PrefEval: tests whether models discover, track and apply user preferences over long interactions.", None),
("2504.14225", "PersonaMem: dynamic user profiling and personalised response benchmark at scale.", None),
("2605.20833", "MemGym: a long-horizon memory environment for training and evaluating agents.", None),
("2608.13883", "Matched system-level comparison of memory backends on MemoryArena with the same harness and scorer.", None),
("2412.15204", "LongBench v2: realistic long-context multitasks; a stress test for any context-management strategy.", None),
("2404.06654", "RULER: measures effective context length and shows nominal windows overstate usable context.", None),
],
"Benchmarks: skills & procedural memory": [
("2605.24117", "SkillEvolBench: 180 tasks testing whether episodic experience can become reusable procedural skill.", None),
("2605.18693", "SkillGenBench: isolates the quality of generated skills from downstream task execution.", None),
("2604.20087", "SkillLearnBench: continual skill learning across 20 skill-dependent real-world tasks.", None),
("2606.23127", "AFTER: 382 enterprise tasks across six roles for measuring skill transfer across tasks, roles and backbones.", None),
("2604.17308", "SkillFlow: tests whether agents discover, repair and maintain skills over a lifelong stream.", None),
("2605.12015", "SkillSafetyBench: safety evaluation for attacks delivered through skill guidance, artifacts and execution environments.", None),
("2609.39284", "EngramBench: capability-grounded evaluation of skill-evolution harnesses, separating abstraction from memorisation.", None),
("2608.05573", "SkillTV-Bench: evaluates judges on full skill-augmented executions rather than final answers.", None),
("2607.01874", "SkillCoach: self-evolving rubrics for fine-grained evaluation of skill selection and use.", None),
("2606.11435", "Frameworks and benchmarks for evaluation-driven skill evolution.", None),
("2511.21730", "Isolates procedural-memory retrieval: recognising functionally equivalent procedures across unseen object vocabularies.", None),
],
"Retrieval & context engineering": [
("2307.03172", "Shows performance depends on where relevant information sits in the context, not just how much fits.", None),
("2310.05736", "LLMLingua: coarse-to-fine prompt compression for long contexts.", None),
("2310.06839", "LongLLMLingua: question-aware compression that improves long-context retrieval and reduces cost.", None),
("2310.11511", "Self-RAG: learns when to retrieve and critiques retrieved evidence and generations.", None),
("2401.15884", "Corrective RAG: detects poor retrieval and corrects it with web search or refined queries.", None),
],
}

# Non-arXiv entries: (section, subsection, title, year, link, extra_label, extra_url, description, kind)
MANUAL = [
# Tools
("Frameworks, libraries & tools", "Memory layers & agent runtimes", "Mem0", 2025, "https://github.com/mem0ai/mem0", "", "", "Open-source memory layer: fact extraction, consolidation, vector/graph storage and a hosted API.", "tool"),
("Frameworks, libraries & tools", "Memory layers & agent runtimes", "Letta", 2024, "https://github.com/letta-ai/letta", "", "", "Stateful-agent runtime from the MemGPT team; editable memory blocks and tool-based memory management.", "tool"),
("Frameworks, libraries & tools", "Memory layers & agent runtimes", "LangMem", 2025, "https://github.com/langchain-ai/langmem", "", "", "LangChain SDK for long-term memory: extraction, hot-path updates and background consolidation.", "tool"),
("Frameworks, libraries & tools", "Memory layers & agent runtimes", "LangGraph memory", 2025, "https://langchain-ai.github.io/langgraph/concepts/memory/", "", "", "Checkpointed thread state plus a namespaced long-term memory store.", "tool"),
("Frameworks, libraries & tools", "Memory layers & agent runtimes", "LlamaIndex memory", 2024, "https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/memory/", "", "", "Composable short- and long-term memory modules over vector, graph and document stores.", "tool"),
("Frameworks, libraries & tools", "Memory layers & agent runtimes", "Cognee", 2024, "https://github.com/topoteretes/cognee", "", "", "Memory and knowledge-graph pipeline with typed schemas, ingestion and graph/vector retrieval.", "tool"),
("Frameworks, libraries & tools", "Memory layers & agent runtimes", "MemOS", 2025, "https://github.com/MemTensor/MemOS", "", "", "Memory OS with plaintext, activation and parameter memory under a scheduling layer.", "tool"),
("Frameworks, libraries & tools", "Memory layers & agent runtimes", "MemoryOS", 2025, "https://github.com/BAI-LAB/MemoryOS", "", "", "Tiered memory implementation with segmented paging and heat-based eviction.", "tool"),
("Frameworks, libraries & tools", "Memory layers & agent runtimes", "A-MEM", 2025, "https://github.com/WujiangXu/A-mem", "", "", "Reference implementation of Zettelkasten-style linked notes and memory evolution.", "tool"),
("Frameworks, libraries & tools", "Memory layers & agent runtimes", "Memobase", 2025, "https://github.com/memodb-io/memobase", "", "", "User-profile memory service with structured profiles and event timelines.", "tool"),
("Frameworks, libraries & tools", "Memory layers & agent runtimes", "Memary", 2024, "https://github.com/kingjulio8238/Memary", "", "", "Open-source memory layer combining knowledge-graph and vector retrieval.", "tool"),
("Frameworks, libraries & tools", "Memory layers & agent runtimes", "ReMe", 2025, "https://github.com/agentscope-ai/ReMe", "", "", "Memory management kit for agents; procedural memory refinement and reuse.", "tool"),
("Frameworks, libraries & tools", "Memory layers & agent runtimes", "Memori", 2025, "https://github.com/MemoriLabs/Memori", "", "", "Agent-native memory infrastructure that turns execution and conversation into persistent structured state.", "tool"),
("Frameworks, libraries & tools", "Memory layers & agent runtimes", "Supermemory", 2025, "https://github.com/supermemoryai/supermemory", "", "", "Memory API and app for personal and agent knowledge.", "tool"),
("Frameworks, libraries & tools", "Memory layers & agent runtimes", "MemU", 2025, "https://github.com/NevaMind-AI/memU", "", "", "Memory framework for proactive, long-running agents.", "tool"),
("Frameworks, libraries & tools", "Memory layers & agent runtimes", "OpenMemory", 2025, "https://github.com/mem0ai/openmemory", "", "", "Self-hosted local memory service for MCP-compatible agents.", "tool"),
("Frameworks, libraries & tools", "Memory layers & agent runtimes", "MCP Memory Server", 2024, "https://github.com/modelcontextprotocol/servers/tree/main/src/memory", "", "", "Reference MCP server implementing knowledge-graph memory (entities, relations, observations).", "tool"),
("Frameworks, libraries & tools", "Graph & retrieval engines", "Graphiti (Zep)", 2025, "https://github.com/getzep/graphiti", "", "", "Bi-temporal knowledge graph engine for agent memory; the open-source core behind Zep.", "tool"),
("Frameworks, libraries & tools", "Graph & retrieval engines", "HippoRAG", 2024, "https://github.com/OSU-NLP-Group/HippoRAG", "", "", "Graph-indexed retrieval for multi-hop memory.", "tool"),
("Frameworks, libraries & tools", "Graph & retrieval engines", "GraphRAG", 2024, "https://github.com/microsoft/graphrag", "", "", "Graph-based RAG with community summaries and local/global search.", "tool"),
("Frameworks, libraries & tools", "Graph & retrieval engines", "LightRAG", 2024, "https://github.com/HKUDS/LightRAG", "", "", "Lightweight dual-level graph RAG with incremental updates.", "tool"),
("Frameworks, libraries & tools", "Storage backends", "pgvector", 2021, "https://github.com/pgvector/pgvector", "", "", "Vector similarity search in PostgreSQL.", "tool"),
("Frameworks, libraries & tools", "Storage backends", "Qdrant", 2021, "https://github.com/qdrant/qdrant", "", "", "Vector database with payload filtering and hybrid search.", "tool"),
("Frameworks, libraries & tools", "Storage backends", "Weaviate", 2021, "https://github.com/weaviate/weaviate", "", "", "Vector database with built-in hybrid and generative modules.", "tool"),
("Frameworks, libraries & tools", "Storage backends", "Milvus", 2019, "https://github.com/milvus-io/milvus", "", "", "Distributed vector database for large-scale retrieval.", "tool"),
("Frameworks, libraries & tools", "Storage backends", "Chroma", 2022, "https://github.com/chroma-core/chroma", "", "", "Embeddable open-source vector store.", "tool"),
("Frameworks, libraries & tools", "Storage backends", "Neo4j", 2007, "https://github.com/neo4j/neo4j", "", "", "Graph database commonly used for temporal and knowledge-graph memory.", "tool"),
("Frameworks, libraries & tools", "Storage backends", "FAISS", 2017, "https://github.com/facebookresearch/faiss", "", "", "Library for efficient similarity search and clustering.", "tool"),
# Articles
("Articles, blogs & talks", "Overviews & context engineering", "LLM Powered Autonomous Agents", 2023, "https://lilianweng.github.io/posts/2023-06-23-agent/", "", "", "The post that popularised planning, memory and tool use as the three pillars of an agent.", "article"),
("Articles, blogs & talks", "Overviews & context engineering", "Effective context engineering for AI agents", 2025, "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents", "", "", "Practical treatment of context as a finite resource: selection, compression, isolation and memory.", "article"),
("Articles, blogs & talks", "Overviews & context engineering", "Building effective AI agents", 2024, "https://www.anthropic.com/engineering/building-effective-agents", "", "", "Workflows vs agents, with memory and tool use as design choices.", "article"),
("Articles, blogs & talks", "Overviews & context engineering", "Context Engineering for Agents", 2025, "https://blog.langchain.com/context-engineering-for-agents/", "", "", "Write, select, compress and isolate: a useful four-part taxonomy.", "article"),
("Articles, blogs & talks", "Overviews & context engineering", "How Long Contexts Fail", 2025, "https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html", "", "", "Poisoning, distraction, confusion and clash; the failure modes memory design must avoid.", "article"),
("Articles, blogs & talks", "Overviews & context engineering", "How to Fix Your Context", 2025, "https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html", "", "", "Concrete techniques for selecting, compressing and isolating context.", "article"),
("Articles, blogs & talks", "Overviews & context engineering", "Context Inertia: When Agents Won't Let Go", 2026, "https://www.dbreunig.com/2026/10/14/context-inertia.html", "", "", "Why stale context persists and how to design for forgetting.", "article"),
("Articles, blogs & talks", "Memory systems & practice", "LangMem SDK for agent long-term memory", 2025, "https://blog.langchain.com/langmem-sdk-launch/", "", "", "Hot-path vs background memory formation, and the API design behind LangMem.", "article"),
("Articles, blogs & talks", "Memory systems & practice", "Launching Long-Term Memory Support in LangGraph", 2024, "https://blog.langchain.com/launching-long-term-memory-support-in-langgraph/", "", "", "Namespaced long-term memory store for graph-based agents.", "article"),
("Articles, blogs & talks", "Memory systems & practice", "Memory Blocks: The Key to Agentic Context Management", 2025, "https://www.letta.com/blog/memory-blocks", "", "", "Editable, labelled blocks that keep core state in the context window.", "article"),
("Articles, blogs & talks", "Memory systems & practice", "Agent Memory: How to Build Agents That Learn and Remember", 2025, "https://www.letta.com/blog/agent-memory", "", "", "Memory types and lifecycle in the Letta/MemGPT architecture.", "article"),
("Articles, blogs & talks", "Memory systems & practice", "Dream: Background Memory Consolidation for AI Agents", 2026, "https://mem0.ai/blog/dream-background-memory-consolidation-for-ai-agents", "", "", "Background consolidation, staleness and forgetting in production memory.", "article"),
("Articles, blogs & talks", "Memory systems & practice", "Benchmarked OpenAI Memory vs LangMem vs MemGPT vs Mem0", 2025, "https://mem0.ai/blog/benchmarked-openai-memory-vs-langmem-vs-memgpt-vs-mem0-for-long-term-memory-here-s-how-they-stacked-up", "", "", "A vendor comparison; read for harness choices as much as for scores.", "article"),
("Articles, blogs & talks", "Memory systems & practice", "Announcing Zep Agent Skills", 2026, "https://blog.getzep.com/blog/introducing-zep-agent-skills/", "", "", "Packaging verified traces into deployable skills.", "article"),
("Articles, blogs & talks", "Memory systems & practice", "Context Graphs: Two Timelines for Every Fact", 2026, "https://blog.getzep.com/blog/context-graphs-two-timelines-every-fact/", "", "", "Bi-temporal modelling explained for practitioners.", "article"),
# Related lists
("Related lists & communities", "", "Agent Memory Paper List", 2025, "https://github.com/Shichun-Liu/Agent-Memory-Paper-List", "", "", "Companion list to the Forms-Functions-Dynamics survey.", "list"),
("Related lists & communities", "", "Awesome Graph Memory", 2026, "https://github.com/DEEP-PolyU/Awesome-GraphMemory", "", "", "Graph-based agent memory papers, benchmarks and libraries.", "list"),
("Related lists & communities", "", "LLM Agent Memory Survey", 2024, "https://github.com/nuster1128/LLM_Agent_Memory_Survey", "", "", "Companion repository to the ACM TOIS memory survey.", "list"),
("Related lists & communities", "", "Awesome Agent Memory (TeleAI)", 2026, "https://github.com/TeleAI-UAGI/Awesome-Agent-Memory", "", "", "Broad, continuously updated agent-memory reading list.", "list"),
("Related lists & communities", "", "Awesome AI Memory", 2026, "https://github.com/IAAR-Shanghai/Awesome-AI-Memory", "", "", "Papers and resources on memory in LLMs and agents.", "list"),
]

HATALIS = {
    "title": "Memory Matters: The Need to Improve Long-Term Memory in LLM-Agents",
    "year": 2024,
    "link": "https://ojs.aaai.org/index.php/AAAI-SS/article/view/27688",
}

# Manual overrides where the arXiv API title is abbreviated or hyphenated oddly.
FULL_TITLES = {
    "Memory in the Age of AI Agents": (
        "Memory in the Age of AI Agents: A Survey — Forms, Functions and Dynamics"
    ),
    "Memory for Autonomous LLM Agents:Mechanisms, Evaluation, and Emerging Frontiers": (
        "Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers"
    ),
    "What to Keep, What to Forget: A Rate-Distortion View of Memory Compaction in "
    "LLMs and Agents": (
        "What to Keep, What to Forget: A Rate–Distortion View of Memory Compaction "
        "in LLMs and Agents"
    ),
}


def drop_redundant_name(title: str, description: str) -> str:
    """Remove a leading "Name: " when the name is already in the title.

    Descriptions used to open by repeating the system name ("FadeMem: ...").
    The README already prints the title next to the description, so the name
    is pure noise unless the title spells it differently (acronym vs long form).
    """
    match = re.match(r"^([\w][\w\-.+ ]{0,40}):\s+(\S.*)$", description)
    if not match:
        return description
    name, rest = match.group(1).strip(), match.group(2)
    if name.lower() not in title.lower():
        return description
    return rest[0].upper() + rest[1:]


def paper_ids() -> list[str]:
    return sorted({aid for items in PAPERS.values() for aid, _, _ in items if aid != "HATALIS"})


def fetch_arxiv(ids: list[str]) -> list[dict]:
    """Query the arXiv API in batches and return id/title/published records."""
    records: list[dict] = []
    for i in range(0, len(ids), 50):
        batch = ids[i : i + 50]
        url = (
            "https://export.arxiv.org/api/query?id_list="
            + ",".join(batch)
            + "&max_results=" + str(len(batch))
        )
        print(f"fetching {len(batch)} records from arXiv ...", file=sys.stderr)
        with urllib.request.urlopen(url, timeout=60) as response:
            root = ET.fromstring(response.read())
        for entry in root.findall(f"{ATOM}entry"):
            raw_id = entry.findtext(f"{ATOM}id") or ""
            records.append(
                {
                    "id": raw_id.rsplit("/", 1)[-1],
                    "title": " ".join((entry.findtext(f"{ATOM}title") or "").split()),
                    "published": entry.findtext(f"{ATOM}published") or "",
                }
            )
        if i + 50 < len(ids):
            time.sleep(3)
    found = {r["id"].split("v")[0] for r in records}
    missing = [aid for aid in ids if aid not in found]
    if missing:
        raise SystemExit(f"arXiv API did not return: {', '.join(missing)}")
    return records


def load_meta(refresh: bool) -> dict[str, dict]:
    if refresh or not CACHE.exists():
        records = fetch_arxiv(paper_ids())
        CACHE.write_text(
            json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"wrote {CACHE.relative_to(ROOT)} with {len(records)} records", file=sys.stderr)
    else:
        records = json.loads(CACHE.read_text(encoding="utf-8"))
    return {record["id"].split("v")[0]: record for record in records}


def build_rows(meta: dict[str, dict]) -> list[dict]:
    rows: list[dict] = []
    seen: set[str] = set()

    for section, items in PAPERS.items():
        for aid, desc, code in items:
            if aid == "HATALIS":
                title, year, link = HATALIS["title"], HATALIS["year"], HATALIS["link"]
            else:
                record = meta.get(aid)
                if record is None:
                    raise SystemExit(
                        f"{aid} is missing from {CACHE.name}; rerun with --refresh"
                    )
                title = " ".join(record["title"].split())
                title = (
                    title.replace(":Mechanisms", ": Mechanisms")
                    .replace("SkillFlow:Benchmarking", "SkillFlow: Benchmarking")
                    .replace("Rate--Distortion", "Rate-Distortion")
                    .replace("Skills -- Beyond", "Skills — Beyond")
                )
                year = int(record["published"][:4])
                link = f"https://arxiv.org/abs/{aid}"
            if title in seen:
                raise SystemExit(f"duplicate title: {title}")
            seen.add(title)
            rows.append(
                {
                    "section": section,
                    "subsection": "",
                    "title": title,
                    "year": year,
                    "link": link,
                    "extra_label": "Code" if code else "",
                    "extra_url": code or "",
                    "description": desc,
                    "kind": "paper",
                }
            )

    for section, sub, title, year, link, label, url, desc, kind in MANUAL:
        if title in seen:
            raise SystemExit(f"duplicate title: {title}")
        seen.add(title)
        rows.append(
            {
                "section": section,
                "subsection": sub,
                "title": title,
                "year": year,
                "link": link,
                "extra_label": label,
                "extra_url": url,
                "description": desc,
                "kind": kind,
            }
        )

    for row in rows:
        row["title"] = FULL_TITLES.get(row["title"], row["title"])
        row["description"] = drop_redundant_name(row["title"], row["description"])

    order = {name: i for i, (name, _) in enumerate(SECTIONS)}
    suborder: dict[tuple[str, str], int] = {}
    for row in rows:
        key = (row["section"], row["subsection"])
        suborder.setdefault(key, len(suborder))
    unknown = {row["section"] for row in rows} - set(order)
    if unknown:
        raise SystemExit(f"unknown sections: {', '.join(sorted(unknown))}")
    rows.sort(key=lambda r: (order[r["section"]], suborder[(r["section"], r["subsection"])]))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="re-query the arXiv API and rewrite data/arxiv_meta.json",
    )
    args = parser.parse_args()

    rows = build_rows(load_meta(args.refresh))
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    from collections import Counter

    kinds = Counter(row["kind"] for row in rows)
    print(f"wrote {CSV_PATH.relative_to(ROOT)}: {len(rows)} entries")
    for name, _ in SECTIONS:
        print(f"{sum(1 for r in rows if r['section'] == name):3d}  {name}")
    print(", ".join(f"{count} {kind}s" for kind, count in kinds.most_common()))


if __name__ == "__main__":
    main()
