# Taxonomy: what agent memory is, and where the open questions are

This page gives the vocabulary used by the list. It follows the three surveys that anchor the field: the **Forms–Functions–Dynamics** taxonomy of Hu et al. (2025), the **write–manage–read** formalization of Du (2026), and the **extraction–storage–retrieval–evolution** lifecycle of Yang et al. (2026). Links to the papers are in [Surveys & SoKs](../README.md#surveys--soks).

## 1. What counts as agent memory

Agent memory is persistent state, outside the model weights, that an agent writes, manages and reads across steps, tasks or sessions. It is not the same as:

- **The context window.** The window is working memory at one moment; agent memory is the store that decides what enters it.
- **RAG over a static corpus.** RAG retrieves from documents that the agent did not produce. Agent memory is written from the agent's own observations, actions and outcomes, and changes as a result.
- **Fine-tuning.** Weight updates can encode experience, but they are slow, opaque and not auditable. Parametric memory counts only when the agent also maintains an external artifact or an explicit write policy.

The boundary is useful but not rigid: systems such as MemOS and AI Engram deliberately mix token-level, latent and parametric memory.

## 2. Forms: what carries the memory

| Form | Examples | Strengths | Costs |
|---|---|---|---|
| **Token-level, flat** | dialogue logs, fact lists, preference profiles | simple, inspectable, cheap to append | retrieval noise, unbounded growth |
| **Token-level, structured** | trees, knowledge graphs, hierarchies, hypergraphs | multi-hop recall, provenance, composability | construction and maintenance cost |
| **Parametric** | adapters, LoRA modules, edited weights | fast, no retrieval prompt | hard to audit, catastrophic forgetting |
| **Latent** | KV cache, recurrent state, activation memory | cheap at inference, preserves context | model-specific, hard to share or inspect |

The list's [Graph, temporal & structured memory](../README.md#graph-temporal--structured-memory) section covers the structured token-level pole; [Memory systems & architectures](../README.md#memory-systems--architectures) covers mixed designs.

## 3. Functions: why the agent keeps it

| Function | What is stored | Typical questions |
|---|---|---|
| **Factual — user** | preferences, profile, history | who is the user, what do they want, what changed? |
| **Factual — environment** | domain facts, tool behaviour, world state | what is true here, what does this tool do? |
| **Experiential — case** | trajectories, successes, failures | what happened last time? |
| **Experiential — strategy** | insights, workflows, plans | what generally works? |
| **Experiential — skill** | code, procedures, `SKILL.md`, tool macros | what can I execute? |
| **Working** | condensed context, plans, scratch state | what am I doing right now? |

Experiential memory is where memory meets skill learning. The [Procedural memory, skills & experience](../README.md#procedural-memory-skills--experience) section is the bridge.

## 4. Dynamics: how memory changes

1. **Formation.** Extract, summarise, distil or internalise. The key decision is the *unit*: turn, fact, episode, note, triplet, workflow, skill, or weight.
2. **Consolidation.** Merge duplicates, abstract across episodes, resolve contradictions, promote important items.
3. **Update.** Supersede, version, retract or edit. Bi-temporal stores keep *valid time* (when a fact was true) separate from *transaction time* (when the system learned it).
4. **Forgetting.** Decay, prune, compress or deactivate. Forgetting is the least implemented and least evaluated stage: Zhang et al. found only 5 of 28 surveyed systems implemented it.
5. **Retrieval.** Select by similarity, graph expansion, recency, importance, or a learned policy; then fit the result into a bounded context.

A useful design rule: **the write path should be cheap and the consolidation path should be allowed to be slow.** Several systems in the list (Engram, Mem0 Dream, sleep-time compute) make this split explicit.

## 5. The lifecycle and its control points

```
observation ──► write ──► store ──► consolidate ──► retrieve ──► act
                  │          │            │             │
               admit?     structure?    merge/forget?  budget?
```

Each arrow hides a decision that most papers fix by hand:

- **Admission:** is this observation worth storing? (novelty, surprise, value of information)
- **Structure:** flat, graph, tree, typed schema, or weights?
- **Consolidation trigger:** every step, fixed batch, threshold, prediction error, or learned policy?
- **Verification:** is a distilled fact or skill correct, and on what evidence?
- **Retrieval policy:** what to fetch, how much, and when to stop?
- **Governance:** who may write, who may read, when must it be deleted?

The [Control, triggering & self-evolution](../README.md#control-triggering--self-evolution) and [Trust, governance & security](../README.md#trust-governance--security) sections collect work on these decisions.

## 6. Five tensions

Du (2026) frames the design space as five competing objectives:

| Tension | The trade-off |
|---|---|
| **Utility** | more memory can help, but irrelevant memory distracts |
| **Efficiency** | writes, consolidation and retrieval all cost tokens and latency |
| **Adaptivity** | memory must change, but change can erase correct knowledge |
| **Faithfulness** | summaries and abstractions drift from their sources |
| **Governance** | persistence creates privacy, poisoning and authority risks |

Most evaluation papers measure utility and efficiency. Faithfulness and governance are younger, and the list marks them separately because they change what "good memory" means.

## 7. Evaluation stack

A complete evaluation has four levels:

1. **Task outcome.** Does memory improve success, answer quality or transfer?
2. **Memory quality.** Precision, recall, contradiction rate, staleness, provenance coverage.
3. **Efficiency.** Write tokens, read tokens, latency, store size, cost per successful task.
4. **Governance and safety.** Unauthorized use, poisoning, privacy leakage, deletion compliance.

Report success **together with** tokens and store size. A system that wins by storing everything has not shown that its memory policy is better; it has shown that a larger context helps. The [benchmark sections](../README.md#benchmarks-memory--long-horizon-evaluation) list the datasets that test these levels.

## 8. Open problems this list is organized around

- **Cost-aware distillation triggers.** Most systems distil every step or at a fixed threshold. A learned trigger that weighs surprise, expected gain and cost is still rare.
- **Verification before promotion.** Few systems execute or replay a distilled skill before trusting it. Sandboxed promotion is an open design.
- **Forgetting with guarantees.** Decay curves are common; boundedness, rollback and non-revival guarantees are not.
- **An expertise metric.** Success alone does not distinguish a brittle lookup table from a compact, transferable schema.
- **Stability and convergence.** Memory update loops can oscillate or drift; formal treatments are rare.
- **Multi-agent memory coherence.** Shared memory raises cache-sharing, consistency and access-control problems borrowed from computer architecture.
- **Authority and provenance.** Consolidated memory must not silently become an instruction; source-bound, fail-closed release is an emerging answer.

## 9. Reading map

| If you care about... | Go to |
|---|---|
| the overall field | [Surveys & SoKs](../README.md#surveys--soks) |
| classic designs | [Foundations & position papers](../README.md#foundations--position-papers) |
| end-to-end systems | [Memory systems & architectures](../README.md#memory-systems--architectures) |
| graphs and time | [Graph, temporal & structured memory](../README.md#graph-temporal--structured-memory) |
| forgetting | [Consolidation, forgetting & pruning](../README.md#consolidation-forgetting--pruning) |
| skills | [Procedural memory, skills & experience](../README.md#procedural-memory-skills--experience) |
| adaptive control | [Control, triggering & self-evolution](../README.md#control-triggering--self-evolution) |
| safety | [Trust, governance & security](../README.md#trust-governance--security) |
| evaluation | [Benchmarks: memory & long-horizon evaluation](../README.md#benchmarks-memory--long-horizon-evaluation) |
| building something | [Frameworks, libraries & tools](../README.md#frameworks-libraries--tools) |
