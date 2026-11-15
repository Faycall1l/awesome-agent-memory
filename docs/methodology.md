# Methodology and provenance

This repository is a **curated reading list**, not a systematic review. It is informed by one. This page records where the entries came from, how they were selected, and what the list does not cover.

## 1. Where the list comes from

The initial set was assembled from three sources:

1. **A systematic review workspace** on abstraction, consolidation and forgetting in LLM agents. The workspace pooled roughly 2,000 unique records from the arXiv API, Semantic Scholar, OpenReview, ACL Anthology and backward/forward snowballing; title-and-abstract screening produced a **93-paper core reading set** organised by five research questions: store/retrieve, skill extraction, abstraction trigger, forgetting/consolidation and evaluation.
2. **A PhD reference set** on cognitive distillation and schema formation: ten papers read in full (six systems, four surveys), with the further-reading list they generated.
3. **Snowballing and verification** for landmark papers, benchmarks and open-source tools that the review set did not contain (for example MemGPT, Voyager, LoCoMo, LongMemEval, GraphRAG and the frameworks section).

The public list is a curated subset of that material plus later additions. It is not the full review corpus: the raw candidate pool contains many records that failed the review's inclusion criteria, and publishing them unfiltered would add noise rather than value.

## 2. What gets in

An entry is included when it satisfies the scope and at least one of the contribution criteria.

**Scope**

- The subject is an LLM or foundation-model agent acting over multiple steps, tasks or sessions.
- A persistent artifact is kept outside the model weights: facts, notes, episodes, graphs, workflows, skills, code or profiles.
- The artifact is written from the agent's own experience, or is a curated procedure that the agent updates.

**Contribution (at least one)**

- A memory mechanism, architecture or representation.
- A consolidation, forgetting, verification or governance mechanism.
- A benchmark, metric or empirical study of memory over time.
- A tool or framework that implements one of the above.
- A survey, systematization or position paper that defines the design space.

**Exclusions**

- Context-window tricks with no persistent artifact.
- RAG over a fixed corpus with no agent-written state (kept only when it informs memory design).
- Weight-only fine-tuning with no external artifact.
- Generic tool-use benchmarks with no memory or skill component.
- Papers with no accessible link or identifiable venue/identifier.

These criteria are adapted from the review protocol. They are deliberately permissive about **preprints**: the field's review cycle lags by a year or more, so restricting the list to published papers would hide the current frontier.

## 3. How entries are chosen

Within the eligible set, selection favours:

- **Coverage** of every lifecycle stage and every memory form, not only the most cited systems.
- **Influence** on later work, measured by citation, reuse of the idea, or adoption in frameworks.
- **Clarity** of the mechanism: a paper that states its write trigger, conflict rule and retrieval budget is more useful than one that reports only a score.
- **Availability** of code, data or a reproducible harness.
- **Contrast**: papers that disagree with each other are kept together, because the disagreement is the useful part.

The list is **not** a quality ranking. Ordering within a section is thematic, not by score. Vendor blogs are included in the articles section and are labelled as practitioner writing; their benchmark numbers are treated as directional.

## 4. Verification

- Paper titles, years and arXiv identifiers were checked against the arXiv API at curation time.
- Every link is present in the repository and can be checked with `make links`.
- Descriptions are written by the maintainers from the paper's abstract, introduction or artifact; they are not auto-generated paraphrases.
- The list does not claim that every reported result replicates. Where a paper's own claims are contested, the description says what the paper reports rather than asserting the result.

## 5. Known biases

- **Recent and arXiv-heavy.** The corpus is skewed toward 2023–2026 preprints. Older cognitive-science and database work appears only when it directly informs agent design.
- **English-language.** Non-English work is underrepresented.
- **Systems with code and benchmarks** are easier to verify and therefore overrepresented relative to theoretical work.
- **Survivorship.** Well-marketed systems receive more attention than equally good systems with less visibility. Corrections are welcome.
- **Cutoff.** The list reflects sources available up to **2026-11-15**. Newer work must be added by pull request.

## 6. Data dictionary

The source of truth is [`data/entries.csv`](../data/entries.csv). `README.md` is generated from it.

| Column | Meaning |
|---|---|
| `section` | Top-level section in the README |
| `subsection` | Optional subgroup (used for tools and articles) |
| `title` | Display title, usually the paper or project title |
| `year` | Publication or first-release year |
| `link` | Canonical paper, project or article URL |
| `extra_label` | Label for a secondary link (`Code`, or empty) |
| `extra_url` | Secondary link URL |
| `description` | One-sentence statement of what the entry contributes |
| `kind` | `paper`, `tool`, `article` or `list` |

The CSV is generated by [`scripts/gen_entries.py`](../scripts/gen_entries.py), which holds the curation tables: every paper, the section it belongs to and the one-line reason it is listed. arXiv titles and years are pinned in [`data/arxiv_meta.json`](../data/arxiv_meta.json) so the regeneration is offline and deterministic; `make refresh` re-queries the arXiv API and rewrites that cache.

## 7. Maintenance

- `make build` regenerates `README.md`.
- `make validate` checks required fields, duplicate titles, section names and URL shape.
- `make links` checks every link with a polite delay; 403 and 429 responses are reported but not treated as hard failures.
- `make check` runs the validator and fails if the committed `README.md` differs from the generated one; this is what CI runs.
- CI validates data and README freshness on every pull request.
- A scheduled link check runs weekly and opens an issue when a link stops responding.

Corrections to a description, a broken link or a misattributed paper are as valuable as new entries. Please open an issue or a pull request using the format in [CONTRIBUTING.md](../CONTRIBUTING.md).
