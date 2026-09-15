# Cadence & Case — admin

The admin page for this repository. Open `admin/index.html`.

## Why these five screens

Read the three agents in `.claude/agents/` together and they state one thesis
outright. The Instagram strategist's mandate is "(1) grow the account organically
and (2) produce a dated, public archive of original educational work that
functions as EB1A petition evidence for criterion #3 and criterion #6."

So the publishing pipeline and the petition are **the same pipeline seen twice**.
This page operates both faces at once — every artifact carries what it did for
reach and what it is worth as evidence, publishing a post files it against a
criterion, and the ledger totals what an adjudicator would actually find.

| Screen | The problem |
|---|---|
| Hit this week's cadence | Three LinkedIn, two Instagram — what shipped, what is drafted, what slot is still empty |
| Draft with a strategist | Pick one of the three agents, give a topic, get a draft |
| Build the EB1A case | The ten regulatory criteria, evidence counted, gaps named |
| Ask my own corpus | Query the markdown this repo already syncs to the knowledge layer |
| See what it cost | Model spend, reach, and what the gate refused |

## The gate

Anything that publishes, or spends a model call, is **proposed** rather than run
on click — scored against the weave platform's six-signal risk vector, then
committed separately.

It carries one rule that turns out to be the same rule the petition runs on: an
action cleared on **fewer than three signals is held for review however low it
scores**, because a low composite from one signal is not the evidence a low
composite from six is. A criterion "met" on one thin document does not survive an
adjudicator reading the file cold either. Same standard, twice — which is why the
thin-evidence banner on the case screen points at the gate.

## Data

- **`window.WEAVE_CONFIG` present** → live, fetched from the deployed stacks.
- **absent** → example data, labelled in the header, never passed off as real.

The config is the JSON that `mcp-observatory`'s `e2e/platform_env.py` emits:

```bash
python e2e/platform_env.py --format json    # paste as window.WEAVE_CONFIG
```

**A published Artifact is always the second mode.** The claude.ai CSP blocks
every fetch to an outside host, so the page cannot reach API Gateway from there.
Serve it from an origin that can — GitHub Pages, or S3 behind CloudFront — and
inject the config before the page's scripts.

### Corpus note

`.github/workflows/deploy.yaml` syncs `*.md` from this repo to the ContextWeave
artifacts bucket on every push to `main`, and **only** the markdown — the sync
filters on it. "Ask my own corpus" therefore answers from the articles, the
resume and the drafts, and from nothing else here. The workflow does not publish
`admin/`; adding that is a separate change, and it needs a hosting target this
repo does not currently name.

## Claude

Two jobs are genuinely generative and run through the `sample` capability:
drafting a post in the chosen agent's voice, and answering a corpus question.
Both are labelled. Neither is presented as a live service's output, and the EB1A
advisor's brief tells it to read the file cold and be candid about weakness
rather than flatter.
