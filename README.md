<div align="center">

# Awesome Agent Memory

**A curated map of memory for AI agents: papers, systems, benchmarks, tools and articles.**

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

<sub>179 entries · 131 papers · 28 tools · 15 articles · 5 related lists</sub>

</div>

Memory is the layer that turns a stateless model into an agent that accumulates facts, procedures and experience over time. This list maps the landscape: surveys, foundational papers, memory architectures, graph and temporal stores, consolidation and forgetting, procedural memory and skills, evaluation, open-source frameworks and practitioner writing.

**Scope.** Papers and tools about persistent state *outside the model weights* that an LLM or foundation-model agent writes, manages and reads across tasks or sessions. Static-corpus RAG is included only where it informs agent-memory design. General vector and graph databases appear as infrastructure, not as memory systems. Papers are mostly arXiv preprints because the field moves faster than review cycles; publication venues are therefore omitted rather than guessed.

> **How this list is built.** It grew out of a systematic review of the agent-memory and agent-skill literature (2,000+ screened records, a 93-paper core reading set) and the reference set of a PhD on cognitive distillation and schema formation. Every entry has a link, and descriptions are written to be useful rather than to paraphrase abstracts. The protocol, inclusion criteria and known biases are documented in [docs/methodology.md](docs/methodology.md).

## Contents

- [Surveys & SoKs](#surveys--soks) (12)
- [Foundations & position papers](#foundations--position-papers) (9)
- [Memory systems & architectures](#memory-systems--architectures) (15)
- [Graph, temporal & structured memory](#graph-temporal--structured-memory) (14)
- [Consolidation, forgetting & pruning](#consolidation-forgetting--pruning) (12)
- [Procedural memory, skills & experience](#procedural-memory-skills--experience) (20)
- [Control, triggering & self-evolution](#control-triggering--self-evolution) (10)
- [Trust, governance & security](#trust-governance--security) (7)
- [Benchmarks: memory & long-horizon evaluation](#benchmarks-memory--long-horizon-evaluation) (16)
- [Benchmarks: skills & procedural memory](#benchmarks-skills--procedural-memory) (11)
- [Retrieval & context engineering](#retrieval--context-engineering) (5)
- [Frameworks, libraries & tools](#frameworks-libraries--tools) (28)
- [Articles, blogs & talks](#articles-blogs--talks) (15)
- [Related lists & communities](#related-lists--communities) (5)

## Start here

If you read eight things, read these:

1. **[Memory in the Age of AI Agents: A Survey — Forms, Functions and Dynamics](https://arxiv.org/abs/2512.13564)** (2025) — Start with the field map: forms, functions and dynamics.
2. **[Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/abs/2603.07670)** (2026) — Then the write–manage–read formalism and the evaluation stack.
3. **[A Survey on the Memory Mechanism of Large Language Model based Agents](https://arxiv.org/abs/2404.13501)** (2024) — The earlier taxonomy, and the audit that exposed the forgetting gap.
4. **[MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560)** (2023) — The OS analogy that made tiered memory mainstream.
5. **[Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory](https://arxiv.org/abs/2504.19413)** (2025) — How a production memory layer extracts, consolidates and serves facts.
6. **[Zep: A Temporal Knowledge Graph Architecture for Agent Memory](https://arxiv.org/abs/2501.13956)** (2025) — Temporal graphs and bi-temporal invalidation in practice.
7. **[FadeMem: Biologically-Inspired Forgetting for Efficient Agent Memory](https://arxiv.org/abs/2601.18642)** (2026) — A concrete, reusable recipe for decay, promotion and fusion.
8. **[Evaluating Very Long-Term Conversational Memory of LLM Agents](https://arxiv.org/abs/2402.17753)** (2024) — LoCoMo: the benchmark most memory systems still report on.

Then pick a path: [building an agent](docs/reading-paths.md#building-an-agent) · [researching architectures](docs/reading-paths.md#researching-architectures) · [forgetting and consolidation](docs/reading-paths.md#forgetting-and-consolidation) · [procedural memory and skills](docs/reading-paths.md#procedural-memory-and-skills) · [evaluation](docs/reading-paths.md#evaluation).

## The landscape at a glance

| Lens | Question | What to look for |
|---|---|---|
| **Forms** | What carries the memory? | Token-level (flat logs, trees, graphs, hierarchies), parametric (weights, adapters), latent (KV cache, activations) |
| **Functions** | Why does the agent keep it? | Factual (user, environment), experiential (cases, strategies, skills), working (condensation, planning state) |
| **Dynamics** | How does it change? | Formation, consolidation, update, forgetting, retrieval |
| **Lifecycle** | Who acts, and when? | Write path, background consolidation, read path, governance and deletion |
| **Evaluation** | Did it actually help? | Task success, memory quality, cost and latency, compactness, transfer, safety |

Most design disagreements reduce to five tensions: **utility** vs **efficiency**, **adaptivity** vs **faithfulness**, and **governance** over all of them (Du, 2026). The taxonomy is expanded in [docs/taxonomy.md](docs/taxonomy.md).

## Surveys & SoKs

The maps. Start with these if you are new to the area.

- **[Memory in the Age of AI Agents: A Survey — Forms, Functions and Dynamics](https://arxiv.org/abs/2512.13564)** (2025) — The current field map: forms (token, parametric, latent), functions (factual, experiential, working) and dynamics (formation, evolution, retrieval), plus benchmarks and frameworks.
- **[Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/abs/2603.07670)** (2026) — Formalizes memory as a write-manage-read loop, compares five mechanism families and names consolidation, forgetting and causally grounded retrieval as open problems.
- **[Graph-based Agent Memory: Taxonomy, Techniques, and Applications](https://arxiv.org/abs/2602.05665)** (2026) — Graph memory from extraction to evolution: knowledge graphs, hierarchies, temporal graphs and hypergraphs, with a large benchmark and library index.
- **[A Survey of Agent Memory in the Second Half: Towards Self-Evolving and Long-Horizon Agents](https://arxiv.org/abs/2602.06052)** (2026) — A 2026 survey of the field's "second half": self-evolving, long-horizon memory that must accumulate and reuse experience across real tasks.
- **[A Survey on the Memory Mechanism of Large Language Model based Agents](https://arxiv.org/abs/2404.13501)** (2024) — Early systematic survey of memory sources, forms, operations and evaluation; its 28-system audit shows forgetting is called core but rarely implemented.
- **[From Human Memory to AI Memory: A Survey on Memory Mechanisms in the Era of LLMs](https://arxiv.org/abs/2504.15965)** (2025) — Maps human memory constructs onto LLM and agent memory mechanisms; useful for vocabulary and design inspiration.
- **[Cognitive Memory in Large Language Models](https://arxiv.org/abs/2504.02441)** (2025) — Cognitive-architecture reading of memory in LLMs: encoding, storage, consolidation, retrieval and forgetting.
- **[Dynamic Agent Skills: A Lifecycle Survey and Taxonomy of Evolving Skill Libraries](https://arxiv.org/abs/2607.10113)** (2026) — Lifecycle survey of evolving skill libraries over 124 papers, with a shared vocabulary of ten update operators.
- **[SoK: Agentic Skills — Beyond Tool Use in LLM Agents](https://arxiv.org/abs/2602.20867)** (2026) — Systematization of agentic skills as callable modules with applicability conditions, execution policies and termination criteria.
- **[A Comprehensive Survey on Agent Skills: Taxonomy, Techniques, and Applications](https://arxiv.org/abs/2605.07358)** (2026) — Taxonomy of skill acquisition, representation, retrieval, composition and evolution, with techniques and applications.
- **[Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering](https://arxiv.org/abs/2604.08224)** (2026) — Treats memory, skills, protocols and harnesses as one story: capabilities externalized outside model weights.
- **[Multi-Agent Memory from a Computer Architecture Perspective: Visions and Challenges Ahead](https://arxiv.org/abs/2603.10062)** (2026) — Position paper framing multi-agent memory as a computer-architecture problem: shared vs distributed memory, cache protocols and consistency.

## Foundations & position papers

The papers that defined the problems, vocabulary and design space.

- **[Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)** (2023) — Observation stream, periodic reflection and recency/relevance/importance retrieval; the design most agent-memory papers still build on.
- **[Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)** (2023) — Stores verbal self-critiques after failures and retries with them; a minimal experiential-learning loop.
- **[MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560)** (2023) — OS-inspired virtual context: pages information between main context, recall storage and archival storage. · [Code](https://github.com/letta-ai/letta)
- **[Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)** (2023) — Lifelong Minecraft agent that writes executable, self-verified skills into an ever-growing library.
- **[ExpeL: LLM Agents Are Experiential Learners](https://arxiv.org/abs/2308.10144)** (2023) — Compares successes and failures across tasks to extract reusable natural-language insights.
- **[Cognitive Architectures for Language Agents](https://arxiv.org/abs/2309.02427)** (2023) — Cognitive architecture for language agents with working, episodic, semantic and procedural memory, plus an explicit action space.
- **[Memory Matters: The Need to Improve Long-Term Memory in LLM-Agents](https://ojs.aaai.org/index.php/AAAI-SS/article/view/27688)** (2024) — Position paper: vector databases are not long-term memory; episodic, semantic and procedural stores need separate management.
- **[Are We Ready For An Agent-Native Memory System?](https://arxiv.org/abs/2606.24775)** (2026) — Asks what an agent-native memory system should be and argues end-to-end scores hide cost, module trade-offs and update robustness.
- **[AI Engram: In Search of Memory Traces in Artificial Intelligence](https://arxiv.org/abs/2606.14997)** (2026) — Parametric view of memory: identifies manipulable "engrams" in network weights using specificity, reactivation, sufficiency and necessity.

## Memory systems & architectures

End-to-end memory layers, runtimes and stores.

- **[Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory](https://arxiv.org/abs/2504.19413)** (2025) — Production memory layer: extracts salient facts, consolidates them and serves them from vector, graph and key-value stores. · [Code](https://github.com/mem0ai/mem0)
- **[Zep: A Temporal Knowledge Graph Architecture for Agent Memory](https://arxiv.org/abs/2501.13956)** (2025) — Temporal knowledge graph memory with bi-temporal edge invalidation; the paper behind Graphiti. · [Code](https://github.com/getzep/graphiti)
- **[A-MEM: Agentic Memory for LLM Agents](https://arxiv.org/abs/2502.12110)** (2025) — Zettelkasten-style notes with LLM-generated keywords, links and in-place evolution of neighbouring memories. · [Code](https://github.com/WujiangXu/A-mem)
- **[PISA: A Pragmatic Psych-Inspired Unified Memory System for Enhanced AI Agency](https://arxiv.org/abs/2510.15966)** (2025) — Piaget-inspired Pool-Bucket-Schema memory with update/evolve/create modes and hybrid symbolic + neural retrieval.
- **[Memanto: Typed Semantic Memory with Information-Theoretic Retrieval for Long-Horizon Agents](https://arxiv.org/abs/2604.22085)** (2026) — Typed semantic memory with 13 categories, versioning and conflict handling, built on a zero-ingestion-cost information-theoretic retriever.
- **[Memory OS of AI Agent](https://arxiv.org/abs/2506.06326)** (2025) — OS-style memory with short-, mid- and long-term tiers, segmented paging and heat-based eviction. · [Code](https://github.com/BAI-LAB/MemoryOS)
- **[MemOS: A Memory OS for AI System](https://arxiv.org/abs/2507.03724)** (2025) — Memory operating system unifying plaintext, activation and parameter memory under a scheduling layer. · [Code](https://github.com/MemTensor/MemOS)
- **[From Isolated Conversations to Hierarchical Schemas: Dynamic Tree Memory Representation for LLMs](https://arxiv.org/abs/2410.14052)** (2024) — MemTree: hierarchical memory that clusters and abstracts conversations into a dynamic tree of schema-like nodes.
- **[MemoryBank: Enhancing Large Language Models with Long-Term Memory](https://arxiv.org/abs/2305.10250)** (2023) — Long-term dialogue memory with daily summarisation and Ebbinghaus-style decay of memory strength.
- **[Less Context, More Accuracy: A Bi-Temporal Memory Engine for LLM Agents Where a Lean Retrieved Context Beats the Full History](https://arxiv.org/abs/2606.09900)** (2026) — Engram: dual-process memory with a cheap append-only write path, asynchronous bi-temporal consolidation and hybrid retrieval.
- **[Oracle Agent Memory as an Enterprise Memory Substrate for Long-Horizon AI Agents](https://arxiv.org/abs/2607.13157)** (2026) — Oracle Agent Memory as a database-native substrate: lifecycle, scoping, latency-bounded retrieval and revision/removal.
- **[MIRIX: Multi-Agent Memory System for LLM-Based Agents](https://arxiv.org/abs/2507.07957)** (2025) — Multi-agent memory with six typed memory components coordinated by a meta-manager. · [Code](https://github.com/Mirix-AI/MIRIX)
- **[Rethinking Memory as Continuously Evolving Connectivity](https://arxiv.org/abs/2605.28773)** (2026) — FluxMem: treats memory as continuously evolving connectivity rather than a static store with fixed retrieval.
- **[MemForest: An Efficient Agent Memory System with Hierarchical Temporal Indexing](https://arxiv.org/abs/2605.23986)** (2026) — Parallel, write-efficient extraction with hierarchical temporal indexing for low-latency updates.
- **[Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents](https://arxiv.org/abs/2607.13591)** (2026) — Learns when to retrieve, retrieve again or reuse a plan instead of applying one fixed memory heuristic.

## Graph, temporal & structured memory

Knowledge graphs, trees, hypergraphs, bi-temporal stores and provenance.

- **[AriGraph: Learning Knowledge Graph World Models with Episodic Memory for LLM Agents](https://arxiv.org/abs/2407.04363)** (2024) — Online triplet extraction plus episodic hyperedges, giving an agent a plannable graph world model. · [Code](https://github.com/AIRI-Institute/AriGraph)
- **[HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models](https://arxiv.org/abs/2405.14831)** (2024) — Hippocampus-inspired graph index over a corpus for multi-hop, single-step retrieval. · [Code](https://github.com/OSU-NLP-Group/HippoRAG)
- **[From RAG to Memory: Non-Parametric Continual Learning for Large Language Models](https://arxiv.org/abs/2502.14802)** (2025) — HippoRAG 2: adds dense retrieval and passage-level evidence to the graph index for continual non-parametric learning. · [Code](https://github.com/OSU-NLP-Group/HippoRAG)
- **[From Local to Global: A Graph RAG Approach to Query-Focused Summarization](https://arxiv.org/abs/2404.16130)** (2024) — GraphRAG: entity graph plus community summaries for global, query-focused summarisation. · [Code](https://github.com/microsoft/graphrag)
- **[LightRAG: Simple and Fast Retrieval-Augmented Generation](https://arxiv.org/abs/2410.05779)** (2024) — Lightweight dual-level graph retrieval with incremental updates. · [Code](https://github.com/HKUDS/LightRAG)
- **[RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval](https://arxiv.org/abs/2401.18059)** (2024) — Recursively clusters and summarises text into a tree for multi-level retrieval. · [Code](https://github.com/parthsarthi03/raptor)
- **[Agent KB: Leveraging Cross-Domain Experience for Agentic Problem Solving](https://arxiv.org/abs/2507.06229)** (2025) — Cross-domain experience library with retrieval and reranking of reusable problem-solving strategies.
- **[Governed Persistent Memory: Source-Bound State Semantics and Fail-Closed Release for Long-Horizon Agents](https://arxiv.org/abs/2608.12476)** (2026) — GPM: source-bound bi-temporal state transitions with executable admission, conflict-isolation and release contracts.
- **[TOKI: A Bitemporal Operator Algebra for Contradiction Resolution in LLM-Agent Persistent Memory](https://arxiv.org/abs/2606.06240)** (2026) — Types contradiction-resolution heuristics as bi-temporal operators with explicit isolation levels and audit rows.
- **[A Graph-Native Bitemporal Memory Store for Conversational AI Agents](https://arxiv.org/abs/2607.26520)** (2026) — Neo4j + HNSW memory store separating identity from versions for point-in-time retrieval without overwriting history.
- **[HyperSkill: Self-Evolving LLM Agents via Hypergraph-Structured Skill Memory](https://arxiv.org/abs/2608.16114)** (2026) — Hypergraph-structured skill memory that preserves compositional relations among procedures.
- **[SE-GoS: Self-Evolving Graph-of-Skills for Skill Library at Scale](https://arxiv.org/abs/2609.08228)** (2026) — Distils execution traces into a self-evolving graph of skills for dependency-aware retrieval at scale.
- **[SkillZip: Contract-Preserving Graph Compression for Scalable Agent Skill Libraries](https://arxiv.org/abs/2608.05604)** (2026) — Compresses skill graphs while preserving procedural contracts to fit a bounded context budget.
- **[SkillGLoW: Procedural-Family Skill Consolidation for Self-Improving Agents on Long-Horizon Task Streams](https://arxiv.org/abs/2609.02217)** (2026) — Groups related procedures into families and consolidates them for long-horizon task streams.

## Consolidation, forgetting & pruning

What to merge, compress, decay, supersede or delete — and why.

- **[FadeMem: Biologically-Inspired Forgetting for Efficient Agent Memory](https://arxiv.org/abs/2601.18642)** (2026) — Differential Ebbinghaus decay across two layers, with LLM-guided conflict resolution and fusion; 45% smaller store.
- **[FSFM: A Biologically-Inspired Framework for Selective Forgetting of Agent Memory](https://arxiv.org/abs/2604.20300)** (2026) — Selective forgetting that combines hippocampal indexing with forgetting curves.
- **[What to Keep, What to Forget: A Rate–Distortion View of Memory Compaction in LLMs and Agents](https://arxiv.org/abs/2607.08032)** (2026) — Rate-distortion account of memory compaction, unifying KV-cache eviction, context compression and agent-store pruning.
- **[Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents](https://arxiv.org/abs/2610.12124)** (2026) — Hippocam: hierarchical memory where use reinforces experience and disuse decays it, with intent-structured consolidation.
- **[Dual-Layer Agentic Memory with Fast Write Routing and Slow Consolidation](https://arxiv.org/abs/2608.22215)** (2026) — Fast write routing plus slow background consolidation to avoid monotonic memory growth and retrieval decay.
- **[Do Self-Evolving Agents Forget? Capability Degradation and Preservation in Lifelong LLM Agent Adaptation](https://arxiv.org/abs/2605.09315)** (2026) — Measures non-monotonic capability degradation in self-evolving agents across skills, workflows, weights and memory.
- **[The Epistemics of Agent Memory: Measuring, and Governing, the Consolidation Decision in Long-Horizon LLM Agents](https://arxiv.org/abs/2609.33013)** (2026) — Shifts evaluation from how much is remembered to whether consolidation decisions and their authority are sound.
- **[Sleep-time Compute: Beyond Inference Scaling at Test-time](https://arxiv.org/abs/2504.13171)** (2025) — Moves consolidation and reasoning into idle time so the critical path stays cheap.
- **[Repo2Skill-Evo: Repository Skills Go Stale in Silence](https://arxiv.org/abs/2608.21964)** (2026) — Shows repository-specific skills silently go stale and measures how to detect and repair them.
- **[When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents](https://arxiv.org/abs/2609.10750)** (2026) — 34k-skill router study: synthetic fine-tuning improves in-distribution retrieval but causes catastrophic forgetting.
- **[Not All Skills Help: Measuring and Repairing Agent Knowledge](https://arxiv.org/abs/2606.15390)** (2026) — Separates generating a skill from deciding whether it helps; measures and repairs harmful accumulated knowledge.
- **[Useful Memories Become Faulty When Continuously Updated by LLMs](https://arxiv.org/abs/2605.12978)** (2026) — Finds that repeatedly rewriting consolidated abstractions with an LLM can make them less reliable than raw episodic traces.

## Procedural memory, skills & experience

Turning trajectories into reusable procedures, workflows and skills.

- **[Agent Workflow Memory](https://arxiv.org/abs/2409.07429)** (2024) — Induces reusable workflows from past trajectories and injects them into future tasks.
- **[Memp: Exploring Agent Procedural Memory](https://arxiv.org/abs/2508.06433)** (2025) — Distils trajectories into step-level instructions and higher-level scripts for learnable procedural memory.
- **[Remember Me, Refine Me: A Dynamic Procedural Memory Framework for Experience-Driven Agent Evolution](https://arxiv.org/abs/2512.10696)** (2025) — Dynamic procedural memory that refines, recombines and retires knowledge instead of accumulating it passively. · [Code](https://github.com/agentscope-ai/ReMe)
- **[Trace2Skill: Distill Trajectory-Local Lessons into Transferable Agent Skills](https://arxiv.org/abs/2603.25158)** (2026) — Consolidates many trajectories in parallel into a transferable skill directory.
- **[SkillX: Automatically Constructing Skill Knowledge Bases for Agents](https://arxiv.org/abs/2604.04804)** (2026) — Automatically builds a shared, cross-agent skill knowledge base from experience.
- **[SkillRL: Evolving Agents via Recursive Skill-Augmented Reinforcement Learning](https://arxiv.org/abs/2602.08234)** (2026) — Extracts reusable behavioural patterns and feeds them back into recursive skill-augmented RL.
- **[MemSkill: Learning and Evolving Memory Skills for Self-Evolving Agents](https://arxiv.org/abs/2602.02474)** (2026) — Makes memory operations themselves learnable skills instead of fixed extraction prompts.
- **[SkillOS: Learning Skill Curation for Self-Evolving Agents](https://arxiv.org/abs/2605.06614)** (2026) — Learns a curation policy for streaming tasks — when to add, merge, keep or prune skills.
- **[STRATA: Self-Maintaining Structured Experience Graphs for Self-Evolving Language Agents](https://arxiv.org/abs/2610.19386)** (2026) — Typed multi-level experience graph separating trajectories, distilled workflows and reasoning items.
- **[WASP-Mem: Let Agent Organize Procedural Memory. Human Spend Effort on Diagnosis](https://arxiv.org/abs/2611.04003)** (2026) — Lets the agent organise its own procedural memory while humans focus on diagnosis.
- **[REM: What to Store, When to Recall, What to Forget in Experience Memory for Coding Agents](https://arxiv.org/abs/2610.27377)** (2026) — Jointly decides what to store, when to recall and what to forget for coding agents.
- **[Learning by Doing: Autonomously Compiling and Curating Agent Skills from Verified Traces](https://arxiv.org/abs/2611.01386)** (2026) — Zep Agent Skills: compiles verified traces into curated, deployable skills in a production service.
- **[Skill-Pro: Learning Reusable Skills from Experience via Non-Parametric PPO for LLM Agents](https://arxiv.org/abs/2602.01869)** (2026) — Non-parametric PPO that learns reusable skills from interaction without weight updates.
- **[ASCENT: Online Test-Time Training of Long-Horizon Agents via Self-Distillation of Verified Experience](https://arxiv.org/abs/2610.05303)** (2026) — Online test-time training by self-distilling verified experience into future attempts.
- **[DAEDALUS: Bootstrapping Agent Memory from Self-Generated Tasks](https://arxiv.org/abs/2610.08048)** (2026) — Bootstraps operational memory from self-generated tasks when no human guidance is available.
- **[CONTRAMEM: Learning Self-Evolving Procedural Memory from Contrasting Multi-Model Trajectories](https://arxiv.org/abs/2608.22533)** (2026) — Learns procedural memory by contrasting trajectories from multiple models.
- **[MUSE-Autoskill: Self-Evolving Agents via Skill Creation, Memory, Management, and Evaluation](https://arxiv.org/abs/2605.27366)** (2026) — Unified skill creation, memory, management and evaluation lifecycle.
- **[JARVIS-1: Open-World Multi-task Agents with Memory-Augmented Multimodal Language Models](https://arxiv.org/abs/2311.05997)** (2023) — Memory-augmented multimodal agent with self-check and an accumulating skill library.
- **[Odyssey: Empowering Minecraft Agents with Open-World Skills](https://arxiv.org/abs/2407.15325)** (2024) — Open-world Minecraft skill library with composable routines and a skill-management pipeline.
- **[SkillsVote: Lifecycle Governance of Agent Skills from Collection, Recommendation to Evolution](https://arxiv.org/abs/2605.18401)** (2026) — Lifecycle governance for open skill ecosystems — collection, recommendation and evolution.

## Control, triggering & self-evolution

When to remember, when to recall and when to change the memory policy.

- **[Darwin-Claw: Environment-Adaptive Experience Consolidation for Recursively Self-Evolving Agents](https://arxiv.org/abs/2610.23574)** (2026) — Environment-adaptive consolidation instead of indiscriminate injection of raw trajectories.
- **[SkillSpec: Consensus-Gated Agent Skill Evolution via Representation Specialization](https://arxiv.org/abs/2610.00704)** (2026) — Consensus-gated skill evolution with representation specialisation.
- **[EASE: Behavior-Adaptive Skill Curation for Self-Evolving Agents](https://arxiv.org/abs/2609.36746)** (2026) — Behaviour-adaptive skill curation modelled against the downstream executor.
- **[GRASP: Gated Regression-Aware Skill Proposer for Self-Improving LLM Agents](https://arxiv.org/abs/2605.29668)** (2026) — Accepts a proposed skill only when it improves the target task without regressing earlier ones.
- **[SkillLens: Adaptive Multi-Granularity Skill Reuse for Cost-Efficient LLM Agents](https://arxiv.org/abs/2605.08386)** (2026) — Adaptive multi-granularity skill reuse to cut injected context while keeping relevance.
- **[APEx: Distillation of Agent Procedural Experience for Adaptive Deep Research Question Answering](https://arxiv.org/abs/2609.02253)** (2026) — Distils procedural experience and couples it to policy adaptation for deep-research QA.
- **[Route to Remember: Adaptive Memory Selection for LLM Agents](https://arxiv.org/abs/2611.05636)** (2026) — Learns when to use text memory and when to move knowledge into weights.
- **[RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent](https://arxiv.org/abs/2610.21791)** (2026) — Adaptive self-improvement workflows with an evolving meta-agent.
- **[SkillScaffold: Scaffolding Agentic Reinforcement Learning with Policy-Adaptive Skill Credit Assignment and Selective Injection](https://arxiv.org/abs/2610.18807)** (2026) — Policy-adaptive credit assignment and selective skill injection for agentic RL.
- **[AutoAgent: Evolving Cognition and Elastic Memory Orchestration for Adaptive Agents](https://arxiv.org/abs/2603.09716)** (2026) — Evolving cognition plus elastic memory orchestration for non-stationary environments.

## Trust, governance & security

Provenance, authority, poisoning, privacy and safe consolidation.

- **[When Memory Becomes Authority: Benchmarking Authority Collapse at the Memory Consolidation Boundary](https://arxiv.org/abs/2608.01679)** (2026) — Benchmark for authority collapse: consolidated memory later consumed as instruction rather than testimony.
- **[Governing Evolving Memory in LLM Agents: Risks, Mechanisms, and the Stability and Safety Governed Memory (SSGM) Framework](https://arxiv.org/abs/2603.11768)** (2026) — Governance framework for semantic drift, privacy and stability in evolving memory.
- **[TRUSTMEM: Learning Trustworthy Memory Consolidation for LLM Agents with Long-Term Memory](https://arxiv.org/abs/2606.25161)** (2026) — Learns trustworthy write/revise/delete operations and guards against omission and hallucinated consolidation.
- **[MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and Repair](https://arxiv.org/abs/2607.27080)** (2026) — Tracks memory poisoning from persistence through consequence to repair.
- **[MRMMIA: Membership Inference Attacks on Memory in Chat Agents](https://arxiv.org/abs/2605.27825)** (2026) — Membership-inference attacks against chat-agent memory, with privacy implications.
- **[AECG: Asymmetric Experience Consolidation and Governance In Multi-Agent Systems](https://arxiv.org/abs/2610.05176)** (2026) — Asymmetric consolidation and governance to stop polluted procedures spreading in multi-agent systems.
- **[Can Benign Skills Induce Misaligned Behavior in LLM Agents?](https://arxiv.org/abs/2611.04299)** (2026) — Shows that benign skills can compose into harmful capabilities; argues for skill-level safety evaluation.

## Benchmarks: memory & long-horizon evaluation

Datasets and harnesses that test memory over sessions and tasks.

- **[Evaluating Very Long-Term Conversational Memory of LLM Agents](https://arxiv.org/abs/2402.17753)** (2024) — LoCoMo: very long multi-session conversations with single-hop, multi-hop, temporal and adversarial recall questions. · [Code](https://github.com/snap-research/locomo)
- **[LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/abs/2410.10813)** (2024) — Five long-term abilities — information extraction, multi-session reasoning, temporal reasoning, knowledge updates and abstention. · [Code](https://github.com/xiaowu0162/LongMemEval)
- **[Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions](https://arxiv.org/abs/2507.05257)** (2025) — MemoryAgentBench: incremental multi-turn evaluation of retrieval, test-time learning, long-range understanding and conflict resolution. · [Code](https://github.com/HUST-AI-HYZ/MemoryAgentBench)
- **[MemBench: Towards More Comprehensive Evaluation on the Memory of LLM-based Agents](https://arxiv.org/abs/2506.21605)** (2025) — Effectiveness and efficiency evaluation across participation, multi-turn, multi-session and multi-scenario settings. · [Code](https://github.com/import-myself/Membench)
- **[HaluMem: Evaluating Hallucinations in Memory Systems of Agents](https://arxiv.org/abs/2511.03506)** (2025) — Operation-level hallucination evaluation for memory extraction, update and retrieval, not just final answers. · [Code](https://github.com/MemTensor/HaluMem)
- **[MemoryArena: Benchmarking Agent Memory in Interdependent Multi-Session Agentic Tasks](https://arxiv.org/abs/2602.16313)** (2026) — Interdependent multi-session agentic tasks where memory must support later actions, not just recall.
- **[From Recall to Forgetting: Benchmarking Long-Term Memory for Personalized Agents](https://arxiv.org/abs/2604.20006)** (2026) — Evaluates consolidation and knowledge updates as personal circumstances change.
- **[MemArena: An Ego-Centric Benchmark for On-Device Agentic Personal Memory Assistants at Scale](https://arxiv.org/abs/2608.02613)** (2026) — On-device, ego-centric personal-memory benchmark at scale, with trustworthiness dimensions.
- **[LifelongAgentBench: Evaluating LLM Agents as Lifelong Learners](https://arxiv.org/abs/2505.11942)** (2025) — Evaluates agents as lifelong learners across sequential tasks and domains.
- **[StreamBench: Towards Benchmarking Continuous Improvement of Language Agents](https://arxiv.org/abs/2406.08747)** (2024) — Benchmarks continuous improvement from feedback over task streams.
- **[Do LLMs Recognize Your Preferences? Evaluating Personalized Preference Following in LLMs](https://arxiv.org/abs/2502.09597)** (2025) — PrefEval: tests whether models discover, track and apply user preferences over long interactions.
- **[Know Me, Respond to Me: Benchmarking LLMs for Dynamic User Profiling and Personalized Responses at Scale](https://arxiv.org/abs/2504.14225)** (2025) — PersonaMem: dynamic user profiling and personalised response benchmark at scale.
- **[MemGym: a Long-Horizon Memory Environment for LLM Agents](https://arxiv.org/abs/2605.20833)** (2026) — A long-horizon memory environment for training and evaluating agents.
- **[MemoryLake on MemoryArena: A Matched Study of Agent Memory Backends](https://arxiv.org/abs/2608.13883)** (2026) — Matched system-level comparison of memory backends on MemoryArena with the same harness and scorer.
- **[LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks](https://arxiv.org/abs/2412.15204)** (2024) — Realistic long-context multitasks; a stress test for any context-management strategy.
- **[RULER: What's the Real Context Size of Your Long-Context Language Models?](https://arxiv.org/abs/2404.06654)** (2024) — Measures effective context length and shows nominal windows overstate usable context.

## Benchmarks: skills & procedural memory

Evaluation of skill discovery, transfer, maintenance and safety.

- **[SkillEvolBench: Benchmarking the Evolution from Episodic Experience to Procedural Skills](https://arxiv.org/abs/2605.24117)** (2026) — 180 tasks testing whether episodic experience can become reusable procedural skill.
- **[SkillGenBench: Benchmarking Skill Generation Pipelines for LLM Agents](https://arxiv.org/abs/2605.18693)** (2026) — Isolates the quality of generated skills from downstream task execution.
- **[SkillLearnBench: Benchmarking Continual Learning Methods for Agent Skill Generation on Real-World Tasks](https://arxiv.org/abs/2604.20087)** (2026) — Continual skill learning across 20 skill-dependent real-world tasks.
- **[Managing Procedural Memory in LLM Agents: Control, Adaptation, and Evaluation](https://arxiv.org/abs/2606.23127)** (2026) — AFTER: 382 enterprise tasks across six roles for measuring skill transfer across tasks, roles and backbones.
- **[SkillFlow: Benchmarking Lifelong Skill Discovery and Evolution for Autonomous Agents](https://arxiv.org/abs/2604.17308)** (2026) — Tests whether agents discover, repair and maintain skills over a lifelong stream.
- **[SkillSafetyBench: Evaluating Agent Safety under Skill-Facing Attack Surfaces](https://arxiv.org/abs/2605.12015)** (2026) — Safety evaluation for attacks delivered through skill guidance, artifacts and execution environments.
- **[EngramBench: A Capability-Grounded Benchmark for Skill-Evolution Harnesses](https://arxiv.org/abs/2609.39284)** (2026) — Capability-grounded evaluation of skill-evolution harnesses, separating abstraction from memorisation.
- **[SkillTV-Bench: Benchmarking How Well Judges Perform on Skill-Augmented Agentic Execution](https://arxiv.org/abs/2608.05573)** (2026) — Evaluates judges on full skill-augmented executions rather than final answers.
- **[SkillCoach: Self-Evolving Rubrics for Evaluating and Enhancing Agentic Skill-Use](https://arxiv.org/abs/2607.01874)** (2026) — Self-evolving rubrics for fine-grained evaluation of skill selection and use.
- **[Agent Skill Evaluation and Evolution: Frameworks and Benchmarks](https://arxiv.org/abs/2606.11435)** (2026) — Frameworks and benchmarks for evaluation-driven skill evolution.
- **[A Benchmark for Procedural Memory Retrieval in Language Agents](https://arxiv.org/abs/2511.21730)** (2025) — Isolates procedural-memory retrieval: recognising functionally equivalent procedures across unseen object vocabularies.

## Retrieval & context engineering

Foundational results on what fits, what gets attended to and how to compress it.

- **[Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172)** (2023) — Shows performance depends on where relevant information sits in the context, not just how much fits.
- **[LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models](https://arxiv.org/abs/2310.05736)** (2023) — Coarse-to-fine prompt compression for long contexts.
- **[LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression](https://arxiv.org/abs/2310.06839)** (2023) — Question-aware compression that improves long-context retrieval and reduces cost.
- **[Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection](https://arxiv.org/abs/2310.11511)** (2023) — Learns when to retrieve and critiques retrieved evidence and generations.
- **[Corrective Retrieval Augmented Generation](https://arxiv.org/abs/2401.15884)** (2024) — Corrective RAG: detects poor retrieval and corrects it with web search or refined queries.

## Frameworks, libraries & tools

Open-source software you can run today.

### Memory layers & agent runtimes

- **[Mem0](https://github.com/mem0ai/mem0)** — Open-source memory layer: fact extraction, consolidation, vector/graph storage and a hosted API.
- **[Letta](https://github.com/letta-ai/letta)** — Stateful-agent runtime from the MemGPT team; editable memory blocks and tool-based memory management.
- **[LangMem](https://github.com/langchain-ai/langmem)** — LangChain SDK for long-term memory: extraction, hot-path updates and background consolidation.
- **[LangGraph memory](https://langchain-ai.github.io/langgraph/concepts/memory/)** — Checkpointed thread state plus a namespaced long-term memory store.
- **[LlamaIndex memory](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/memory/)** — Composable short- and long-term memory modules over vector, graph and document stores.
- **[Cognee](https://github.com/topoteretes/cognee)** — Memory and knowledge-graph pipeline with typed schemas, ingestion and graph/vector retrieval.
- **[MemOS](https://github.com/MemTensor/MemOS)** — Memory OS with plaintext, activation and parameter memory under a scheduling layer.
- **[MemoryOS](https://github.com/BAI-LAB/MemoryOS)** — Tiered memory implementation with segmented paging and heat-based eviction.
- **[A-MEM](https://github.com/WujiangXu/A-mem)** — Reference implementation of Zettelkasten-style linked notes and memory evolution.
- **[Memobase](https://github.com/memodb-io/memobase)** — User-profile memory service with structured profiles and event timelines.
- **[Memary](https://github.com/kingjulio8238/Memary)** — Open-source memory layer combining knowledge-graph and vector retrieval.
- **[ReMe](https://github.com/agentscope-ai/ReMe)** — Memory management kit for agents; procedural memory refinement and reuse.
- **[Memori](https://github.com/MemoriLabs/Memori)** — Agent-native memory infrastructure that turns execution and conversation into persistent structured state.
- **[Supermemory](https://github.com/supermemoryai/supermemory)** — Memory API and app for personal and agent knowledge.
- **[MemU](https://github.com/NevaMind-AI/memU)** — Memory framework for proactive, long-running agents.
- **[OpenMemory](https://github.com/mem0ai/openmemory)** — Self-hosted local memory service for MCP-compatible agents.
- **[MCP Memory Server](https://github.com/modelcontextprotocol/servers/tree/main/src/memory)** — Reference MCP server implementing knowledge-graph memory (entities, relations, observations).

### Graph & retrieval engines

- **[Graphiti (Zep)](https://github.com/getzep/graphiti)** — Bi-temporal knowledge graph engine for agent memory; the open-source core behind Zep.
- **[HippoRAG](https://github.com/OSU-NLP-Group/HippoRAG)** — Graph-indexed retrieval for multi-hop memory.
- **[GraphRAG](https://github.com/microsoft/graphrag)** — Graph-based RAG with community summaries and local/global search.
- **[LightRAG](https://github.com/HKUDS/LightRAG)** — Lightweight dual-level graph RAG with incremental updates.

### Storage backends

- **[pgvector](https://github.com/pgvector/pgvector)** — Vector similarity search in PostgreSQL.
- **[Qdrant](https://github.com/qdrant/qdrant)** — Vector database with payload filtering and hybrid search.
- **[Weaviate](https://github.com/weaviate/weaviate)** — Vector database with built-in hybrid and generative modules.
- **[Milvus](https://github.com/milvus-io/milvus)** — Distributed vector database for large-scale retrieval.
- **[Chroma](https://github.com/chroma-core/chroma)** — Embeddable open-source vector store.
- **[Neo4j](https://github.com/neo4j/neo4j)** — Graph database commonly used for temporal and knowledge-graph memory.
- **[FAISS](https://github.com/facebookresearch/faiss)** — Library for efficient similarity search and clustering.

## Articles, blogs & talks

Practitioner writing that explains the design choices.

### Overviews & context engineering

- **[LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)** (2023) — The post that popularised planning, memory and tool use as the three pillars of an agent.
- **[Effective context engineering for AI agents](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)** (2025) — Practical treatment of context as a finite resource: selection, compression, isolation and memory.
- **[Building effective AI agents](https://www.anthropic.com/research/building-effective-agents)** (2024) — Workflows vs agents, with memory and tool use as design choices.
- **[Context Engineering for Agents](https://www.langchain.com/blog/context-engineering-for-agents)** (2025) — Write, select, compress and isolate: a useful four-part taxonomy.
- **[How Long Contexts Fail](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html)** (2025) — Poisoning, distraction, confusion and clash; the failure modes memory design must avoid.
- **[How to Fix Your Context](https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html)** (2025) — Concrete techniques for selecting, compressing and isolating context.
- **[Context Inertia: When Agents Won't Let Go](https://www.dbreunig.com/2026/10/14/context-inertia.html)** (2026) — Why stale context persists and how to design for forgetting.

### Memory systems & practice

- **[LangMem SDK for agent long-term memory](https://www.langchain.com/blog/langmem-sdk-launch)** (2025) — Hot-path vs background memory formation, and the API design behind LangMem.
- **[Launching Long-Term Memory Support in LangGraph](https://www.langchain.com/blog/launching-long-term-memory-support-in-langgraph)** (2024) — Namespaced long-term memory store for graph-based agents.
- **[Memory Blocks: The Key to Agentic Context Management](https://www.letta.com/blog/memory-blocks)** (2025) — Editable, labelled blocks that keep core state in the context window.
- **[Agent Memory: How to Build Agents That Learn and Remember](https://www.letta.com/blog/agent-memory)** (2025) — Memory types and lifecycle in the Letta/MemGPT architecture.
- **[Dream: Background Memory Consolidation for AI Agents](https://mem0.ai/blog/dream-background-memory-consolidation-for-ai-agents)** (2026) — Background consolidation, staleness and forgetting in production memory.
- **[Benchmarked OpenAI Memory vs LangMem vs MemGPT vs Mem0](https://mem0.ai/blog/benchmarked-openai-memory-vs-langmem-vs-memgpt-vs-mem0-for-long-term-memory-here-s-how-they-stacked-up)** (2025) — A vendor comparison; read for harness choices as much as for scores.
- **[Announcing Zep Agent Skills](https://www.getzep.com/blog/introducing-zep-agent-skills/)** (2026) — Packaging verified traces into deployable skills.
- **[Context Graphs: Two Timelines for Every Fact](https://www.getzep.com/blog/context-graphs-two-timelines-every-fact/)** (2026) — Bi-temporal modelling explained for practitioners.

## Related lists & communities

Other curated collections worth following.

- **[Agent Memory Paper List](https://github.com/Shichun-Liu/Agent-Memory-Paper-List)** — Companion list to the Forms-Functions-Dynamics survey.
- **[Awesome Graph Memory](https://github.com/DEEP-PolyU/Awesome-GraphMemory)** — Graph-based agent memory papers, benchmarks and libraries.
- **[LLM Agent Memory Survey](https://github.com/nuster1128/LLM_Agent_Memory_Survey)** — Companion repository to the ACM TOIS memory survey.
- **[Awesome Agent Memory (TeleAI)](https://github.com/TeleAI-UAGI/Awesome-Agent-Memory)** — Broad, continuously updated agent-memory reading list.
- **[Awesome AI Memory](https://github.com/IAAR-Shanghai/Awesome-AI-Memory)** — Papers and resources on memory in LLMs and agents.

## How to use this list

- **New to the area:** read the first three surveys in *Start here*, then one system paper and one benchmark.
- **Building a product:** start with the frameworks section, then read the benchmark that matches your workload. Vendor blogs are useful for design vocabulary; treat their scores as directional.
- **Writing a paper:** the survey and benchmark sections give the current baselines and evaluation axes. The *Consolidation, forgetting & pruning* and *Control, triggering & self-evolution* sections are where the open problems are.
- **Looking for a gap:** [docs/taxonomy.md](docs/taxonomy.md) lists the lifecycle stages and the questions each stage still leaves open.

## Contributing

Corrections and additions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) first: entries live in [`data/entries.csv`](data/entries.csv), and `README.md` is generated by `make build`. A good pull request adds one entry, a working link and a one-sentence description that says why the work matters.

## License

The curation, descriptions and documentation in this repository are licensed under [CC BY 4.0](LICENSE). Linked papers, code and articles remain under their own licenses.

## Citation

If you use this list in teaching or research, cite it via [CITATION.cff](CITATION.cff). Corrections to individual entries are tracked in the git history.

## Acknowledgements

This list benefited from the surveys and companion repositories it indexes, especially the paper lists maintained by the agent-memory and graph-memory communities. Errors in selection or description are the maintainers' own.
