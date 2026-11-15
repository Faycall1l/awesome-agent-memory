# Reading paths

Five ways through the list, depending on what you need. Each path is short on purpose; follow the section links when you want the full set.

## Building an agent

For engineers who need a memory layer this quarter.

1. **[MemGPT](https://arxiv.org/abs/2310.08560)** — the tiered, OS-style mental model: main context, recall, archival.
2. **[Mem0](https://arxiv.org/abs/2504.19413)** — what a production extraction-and-consolidation pipeline looks like.
3. **[Zep](https://arxiv.org/abs/2501.13956)** — when time matters: temporal graphs and bi-temporal invalidation.
4. **[LangMem SDK launch](https://blog.langchain.com/langmem-sdk-launch/)** — hot-path vs background memory formation in practice.
5. **[Letta memory blocks](https://www.letta.com/blog/memory-blocks)** — keeping core state editable and in-context.
6. **[LoCoMo](https://arxiv.org/abs/2402.17753)** and **[LongMemEval](https://arxiv.org/abs/2410.10813)** — the two benchmarks to run before trusting a vendor claim.
7. **[Frameworks, libraries & tools](../README.md#frameworks-libraries--tools)** — runnable options, from Mem0 and Letta to Graphiti and pgvector.

**Design checklist:** decide the write unit, the consolidation trigger, the retrieval budget and the deletion policy before choosing a database. Most production failures are policy failures, not index failures.

## Researching architectures

For a literature review or a thesis chapter.

1. **[Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564)** — the Forms–Functions–Dynamics map.
2. **[Memory for Autonomous LLM Agents](https://arxiv.org/abs/2603.07670)** — the write–manage–read formalism and evaluation levels.
3. **[Graph-based Agent Memory](https://arxiv.org/abs/2602.05665)** — the structured-memory lifecycle.
4. **[A Survey on the Memory Mechanism of LLM-based Agents](https://arxiv.org/abs/2404.13501)** — the earlier taxonomy and the forgetting gap.
5. **[A-MEM](https://arxiv.org/abs/2502.12110)**, **[PISA](https://arxiv.org/abs/2510.15966)**, **[Memanto](https://arxiv.org/abs/2604.22085)** — three contrasting answers: link-and-evolve, schema construction, typed semantic store.
6. **[AriGraph](https://arxiv.org/abs/2407.04363)** and **[HippoRAG 2](https://arxiv.org/abs/2502.14802)** — graph memory for planning and multi-hop retrieval.
7. **[Memory systems & architectures](../README.md#memory-systems--architectures)** — the full set.

**Reading tip:** for each system, write down the unit stored, the write trigger, the conflict rule, the forgetting rule and the retrieval budget. The differences that matter appear in that five-line table, not in the headline benchmark.

## Forgetting and consolidation

For anyone whose store only grows.

1. **[A Survey on the Memory Mechanism of LLM-based Agents](https://arxiv.org/abs/2404.13501)** — the 5-of-28 forgetting audit.
2. **[FadeMem](https://arxiv.org/abs/2601.18642)** — differential decay, hysteresis promotion and fusion; the most reusable recipe.
3. **[MemoryBank](https://arxiv.org/abs/2305.10250)** — Ebbinghaus-style decay in a dialogue assistant.
4. **[FSFM](https://arxiv.org/abs/2604.20300)** — selective forgetting from hippocampal indexing.
5. **[Useful Memories Become Faulty When Continuously Updated by LLMs](https://arxiv.org/abs/2605.12978)** — why repeated LLM rewriting can degrade consolidated abstractions.
6. **[What to Keep, What to Forget](https://arxiv.org/abs/2607.08032)** — a rate–distortion view that unifies context compaction and store pruning.
7. **[Consolidation, forgetting & pruning](../README.md#consolidation-forgetting--pruning)** — the full set.

**Open question:** almost every paper reports retention at a smaller store size. Very few report a bound, a rollback path, or a guarantee that a deleted fact cannot reappear through an old index.

## Procedural memory and skills

For agents that need to learn *how*, not just *what*.

1. **[Voyager](https://arxiv.org/abs/2305.16291)** — the canonical executable skill library.
2. **[ExpeL](https://arxiv.org/abs/2308.10144)** — success/failure contrast into reusable insights.
3. **[Agent Workflow Memory](https://arxiv.org/abs/2409.07429)** — trajectories into reusable workflows.
4. **[Memp](https://arxiv.org/abs/2508.06433)** and **[ReMe](https://arxiv.org/abs/2512.10696)** — learnable and dynamic procedural memory.
5. **[Trace2Skill](https://arxiv.org/abs/2603.25158)** and **[SkillX](https://arxiv.org/abs/2604.04804)** — consolidating many trajectories into a skill library.
6. **[Dynamic Agent Skills](https://arxiv.org/abs/2607.10113)** and **[SoK: Agentic Skills](https://arxiv.org/abs/2602.20867)** — the taxonomies.
7. **[SkillEvolBench](https://arxiv.org/abs/2605.24117)** and **[SkillFlow](https://arxiv.org/abs/2604.17308)** — evaluation of skill formation and lifelong maintenance.
8. **[Procedural memory, skills & experience](../README.md#procedural-memory-skills--experience)** — the full set.

**Design question:** is the skill a document, a program, a workflow graph, or a set of weights? Each choice buys a different verification strategy. Only code and executable workflows can be replayed in a sandbox before promotion.

## Evaluation

For choosing a benchmark or designing an ablation.

1. **[LoCoMo](https://arxiv.org/abs/2402.17753)** — long multi-session conversation; single-hop, multi-hop, temporal and adversarial questions.
2. **[LongMemEval](https://arxiv.org/abs/2410.10813)** — extraction, multi-session reasoning, temporal reasoning, knowledge updates and abstention.
3. **[MemoryAgentBench](https://arxiv.org/abs/2507.05257)** — incremental multi-turn interactions; retrieval, test-time learning, long-range understanding and conflict resolution.
4. **[HaluMem](https://arxiv.org/abs/2511.03506)** — operation-level hallucination measurement, not just final-answer accuracy.
5. **[MemoryArena](https://arxiv.org/abs/2602.16313)** — interdependent multi-session tasks where memory must support action.
6. **[StreamBench](https://arxiv.org/abs/2406.08747)** and **[LifelongAgentBench](https://arxiv.org/abs/2505.11942)** — improvement and retention over task streams.
7. **[Benchmarks: memory & long-horizon evaluation](../README.md#benchmarks-memory--long-horizon-evaluation)** — the full set.

**Reporting checklist:** always report task success, input/output tokens, store size, number of sessions and the retrieval budget. Without all five, a memory result is not comparable to another system.

## Trust and governance

For systems that persist user data or act on what they remember.

1. **[Governed Persistent Memory](https://arxiv.org/abs/2608.12476)** — source-bound admission, conflict isolation and fail-closed release.
2. **[TOKI](https://arxiv.org/abs/2606.06240)** — contradiction resolution as a bi-temporal operator algebra.
3. **[When Memory Becomes Authority](https://arxiv.org/abs/2608.01679)** — authority collapse at the consolidation boundary.
4. **[SSGM](https://arxiv.org/abs/2603.11768)** — stability, safety and semantic-drift governance.
5. **[TRUSTMEM](https://arxiv.org/abs/2606.25161)** — trustworthy write, revise and delete operations.
6. **[MemSecBench](https://arxiv.org/abs/2607.27080)** — memory poisoning from persistence to repair.
7. **[Trust, governance & security](../README.md#trust-governance--security)** — the full set.
