# Contributing

Thanks for helping. This list is small on purpose: an entry earns its place by being useful to someone building or researching agent memory, not by existing.

## The one-entry rule

One pull request adds, fixes or removes **one entry**. Small pull requests are easy to check, easy to revert and easy to discuss. If you have five entries, send five pull requests — or open an issue first if they belong to a theme.

## How entries work

`data/entries.csv` is the source of truth. `README.md` is generated from it and must never be edited by hand.

| Column | Rule |
|---|---|
| `section` | Must be one of the sections listed in `scripts/build_readme.py`. Pick the one where a reader would look for it. |
| `subsection` | Optional grouping inside a section (used by the tools and articles sections). Empty is fine. |
| `title` | The work's own title, not a marketing rewrite. Do not add venue names. |
| `year` | Four-digit year of first public release. |
| `link` | Canonical, stable URL: arXiv abstract page, publisher page, official repository or the author's own post. No PDF-only links when an abstract page exists, no URL shorteners, no tracking parameters. |
| `extra_label` / `extra_url` | Optional second link, always as a pair. Use `Code` for the official implementation, `Project` for a project page, `Docs` for documentation. |
| `description` | One sentence, 30–260 characters, that says **what the work contributes and why it matters**. |
| `kind` | `paper`, `tool`, `article` or `list`. |

### Writing the description

Good descriptions answer "should I read this, and what will I get?" They say what is new, what it measures, or what decision it helps you make.

- Good: *"OS-inspired virtual context: pages information between main context, recall storage and archival storage."*
- Weak: *"A paper about memory for agents."*
- Weak: *"Proposes a novel framework for long-term memory."* (Says nothing; every paper proposes something.)

Avoid hype ("revolutionary", "state-of-the-art" without a number), avoid copying the abstract verbatim, and avoid claims you cannot support from the paper itself. If the work is a vendor's own benchmark, say so — that is useful information.

Do not open the description with the work's own name ("FadeMem: …") when the title already says it; the generator strips that automatically when the name appears in the title, but it reads better if you just start with the contribution.

## Workflow

```bash
# 1. branch
git checkout -b add/<short-slug>

# 2. add the row to data/entries.csv, then rebuild the README
make build

# 3. check structure, then optionally check links
make validate
make links

# 4. commit both files
git add data/entries.csv README.md
git commit -m "add: <title>"
```

`make check` is what CI runs: it validates the CSV and fails if `README.md` does not match what the generator would produce.

The tooling uses only the Python standard library (Python 3.10 or newer), so there is nothing to install.

### A note on the generated README

`README.md` is deterministic: the counts are derived from `data/entries.csv` and there is no build timestamp, so rebuilding without changing data must produce a byte-identical file. Include the regenerated file in your pull request.

## What belongs here

**In scope.** Work about persistent state outside the model weights that an LLM or foundation-model agent writes, manages and reads across tasks or sessions: facts, episodes, notes, graphs, workflows, skills, profiles.

**Out of scope.**

- Work with no persistent artifact (a single-session prompt trick).
- Static-corpus RAG with no agent write path, unless it directly informs agent-memory design.
- Fine-tuning that only changes weights with no memory mechanism around it.
- Generic vector or graph databases, except as infrastructure the list explicitly indexes.
- Generic tool-use, planning or multi-agent benchmarks with no memory component.
- Product announcements without technical content, listicles, SEO posts.
- Papers with no stable public link.

If you are unsure, open an issue with the link and one sentence about why it matters.

## Corrections

Broken link, wrong year, wrong title, misleading description, better canonical URL — these are the most valuable contributions. Send them as a one-line pull request. If a work was published at a venue after appearing as a preprint, update `year` only if the year of the linked page changed; do not add the venue to the title.

## Style

- Markdown: sentence case for headings, em dashes (`—`) not double hyphens, Oxford comma.
- Dates and years: ISO (`2026-11-15`).
- Link text should name the work, not say "here" or "this paper".
- British or American spelling is fine; be consistent within an entry.

## Code of conduct

Be civil, assume good faith, and argue about the work rather than the person. Harassment, personal attacks and spam are removed and reported.

## License

By contributing you agree that your contribution is licensed under [CC BY 4.0](LICENSE), the same license as the rest of the curation. Linked works keep their own licenses.
