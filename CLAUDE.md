# skills

**Status**: no status label is recorded for this repo anywhere the portfolio can see — treat it as *published but between factory runs*. Last commit 2026-08-28 (`5eb363d`); the last full-repo factory cycle was Run 3 on 2026-03-10 and Run 4 is deferred (`../skill-gen/PLAN.md`).
**Tier**: none. Root [`../PLAN.md`](../PLAN.md) lists this repo under **Not tiered** — "external mirror library — not a portfolio project". That is a deliberate recorded exclusion, not a missing row.

Public MIT-licensed collection of lightweight Python skills for Claude Code, each calling its
service's REST/GraphQL API directly instead of through an MCP server process. Remote:
`https://github.com/m0j0d/skills`. The trade-off this repo takes a position on is argued in
[`WHY-SKILLS.md`](WHY-SKILLS.md) — skills and MCP complement each other; neither is universally better.

## Intent (SSOT)

**One sentence:** Thirteen small, readable, directly-editable Claude Code skills, published so an
outside developer can install one in a minute and change it in five.

**For whom:** Claude Code users — the operator first, but the repo is public, licensed, and has a
[`SECURITY.md`](SECURITY.md), so an unknown reader landing on it cold is a first-class audience.
Not for other AI clients: skills are Claude Code only.

**Picture this:** You want Claude to file Jira tickets. You copy `jira/` into `~/.claude/skills/`,
export one token, and it works. A month later the API changes; you open `jira/scripts/` and fix the
call yourself, because it is a hundred lines of Python and not a server you have to rebuild.

**Purpose:** Be the graduation destination for skills the [`../skill-gen`](../skill-gen/CLAUDE.md)
factory produces, and the public shop window for what a skill can be.

**Success:** A stranger can pick a skill, install it, and trust that it works — because every skill
carries published scores (safety gate, static pre-flight /20, behavioral eval /80) on the
[dashboard](https://m0j0d.github.io/skills/).

**NOT:** Not the factory — generation, validation and evaluation all live in `../skill-gen`; nothing
in this repo generates or scores anything. Not an MCP server, and not a Python package: there is no
`pyproject.toml`, no build, no release artifact. Distribution is `git clone` or `cp -r`.

## Structure

Thirteen skill directories, each with a `SKILL.md`, and `scripts/` where there is code to run:

```
fetch  github  github-actions  jira  linear  memory  notion  playwright
semgrep  sequential-thinking  slack  sqlite  twitter
```

That list is the truth on disk, and it agrees with [`README.md`](README.md) and with the explicit
list in [`.github/workflows/validate.yml`](.github/workflows/validate.yml). Two disagreements worth
knowing about:

- Twelve skills have `scripts/`; `sqlite/` does not (its `SKILL.md` is guidance only).
- `../skill-gen/PLAN.md` records the public repo as "13 skills" but then names fourteen, including
  `jira-workspace` — which is not a skill here. `jira-workspace/`, `playwright-eval/` and
  `semgrep-eval/` exist as untracked local scratch directories, matched by the `*-workspace/` and
  `*-eval/` rules in `.gitignore`. They are not part of the repo.

Supporting directories:

| Path | Role |
|---|---|
| `docs/` | The published dashboard — `docs/index.html`, `docs/data/skills.json` (scores), `docs/skills/detail.html`, plus `docs/test-results/`. Served at https://m0j0d.github.io/skills/ by GitHub's built-in `pages-build-deployment`; there is no Pages workflow file in this repo. |
| `scripts/` | Contains `scripts/README.md` only. |
| `.github/workflows/validate.yml` | Structure / syntax / JSON / secret checks. See below. |
| `.ci-config` | Pre-push gate overrides consumed by `../atlas/scripts/test-project.sh`. |

## Skill layout

Per [`CONTRIBUTING.md`](CONTRIBUTING.md), every skill follows:

```
skill-name/
  SKILL.md          # documentation, tools, examples
  scripts/
    skill_tools.py  # implementation
  requirements.txt  # dependencies, if any
```

Only `fetch/`, `github/` and `twitter/` carry a `requirements.txt`. Credentials always come from
environment variables (`GITHUB_TOKEN`, `SLACK_TOKEN`, ...) — never a config file in the repo, never a
literal in a script. `.gitignore` blocks `.env`, `*.key`, `*.pem`, `credentials.json` and friends as
defence in depth.

## Validation

Three layers are claimed by `README.md` and `CONTRIBUTING.md` — **safety gate** (pass/block),
**static pre-flight** (/20) and **behavioral eval** (/80, an A/B test asking whether Claude does
better with the skill than without). Layers two and three are *not implemented here*: the scoring
engine is `../skill-gen/validator/` and the eval pipeline is the factory's Phase 4. What this repo
holds is their published output in `docs/data/skills.json`, and those numbers are only as fresh as
the last factory run.

What actually runs on push and pull request is `.github/workflows/validate.yml`, and it is narrower
than the three layers:

1. every one of the thirteen skills has a `SKILL.md`;
2. eleven named skills have a `scripts/` directory — the list omits `notion`, which does have one,
   so `notion/scripts/` is unguarded;
3. `python -m py_compile` over every `*/scripts/*.py`;
4. `python -m json.tool` over every file under `docs/test-results/`;
5. a regex grep for hardcoded `api_key|token|secret|password` assignments in scripts.

**This workflow is currently disabled.** `gh workflow list --all` reports `Validate Skills` as
`disabled_manually`; the reason is not recorded in this repo. Re-enable before relying on any of the
five checks above.

Linting is also off, deliberately and on the record: `.ci-config` sets `SKIP_LINT=true` and explains
why — 356 ruff violations measured 2026-08-02 against the pinned ruff in
`../atlas/templates/ruff-pin.txt`, over half of them `UP006` style modernization. The named fix is a
`ruff.toml` that selects the rules this repo wants, not a grind through the raw count. Read that file
before touching lint here.

## Relationship to skill-gen

Documented, in [`../skill-gen/CLAUDE.md`](../skill-gen/CLAUDE.md): skill-gen "generates, validates,
evaluates, and graduates Claude Code skills to the public `skills/` repo", holds the **ratchet
principle** (an existing skill may stay or improve, never downgrade), and treats the behavioral A/B
eval — not the static score — as the graduation gate.

**Open, and stated as open rather than guessed:** the mechanism of graduation is not recorded on
this side. No script, workflow or documented procedure in this repo moves a skill in from the
factory, and nothing here reports back. The one staged graduation batch (the "Tier D ratchet",
13 skills' worth of `should_trigger` sections and eval files, staged 2026-04-20) was never merged
here and was retired unmerged on 2026-07-03. So in practice: changes arrive as ordinary commits, and
the factory's claim to own this repo's quality is a claim about intent, not an observed pipeline.

Two concrete gaps follow from that, both verified on disk today:

- **`should_trigger` is absent from all thirteen `SKILL.md` files.** The Skills 2.0 convention the
  factory planned to add (Run 4, Tier B) has not landed.
- **An eval file exists for exactly one skill** — [`jira/evals/evals.json`](jira/evals/evals.json), committed
  2026-03-11. `../skill-gen/PLAN.md`'s 2026-04-18 audit records "0/13", which is wrong by one; the
  substance of that finding — the factory's graduation gate has almost nothing to score against —
  still holds.

Also unrecorded: the operator direction of 2026-07-30 was to "resurrect the public `skills/` repo
with a new release and publish `skill-gen` alongside it — shape TBD". Shape is still TBD; do not
infer a release plan from this file.

## Conventions

- **Public repo, outside readers.** Write `SKILL.md` prose for someone who has never seen the
  portfolio. No internal run IDs, no portfolio-only paths in skill documentation.
- **Code, docs and scores move together.** Changing a skill's behaviour means updating its
  `SKILL.md` in the same change; if the change is meant to alter its published score, that number
  comes from a factory run, not from editing `docs/data/skills.json` by hand.
- **Substantive changes go through a pull request** (portfolio rule, root [`../CLAUDE.md`](../CLAUDE.md)).
  This repo has a remote and normal PR flow.
- **Never commit a credential.** Report vulnerabilities through GitHub Security Advisories, not a
  public issue — see [`SECURITY.md`](SECURITY.md).
- Skills are Claude Code only. If a request needs cross-platform support, persistent connections or
  team-scale distribution, the answer is an MCP server, not a skill here — the reasoning is already
  written down in `WHY-SKILLS.md`; don't re-derive it.

## Portfolio context

Portfolio-internal pointers; an outside reader can ignore this section.

- [`../skill-gen/CLAUDE.md`](../skill-gen/CLAUDE.md) — the factory, and the SSOT for how skills are
  meant to reach this repo.
- [`../atlas/patterns/skill-structure.md`](../atlas/patterns/skill-structure.md) — SKILL.md anatomy.
- [`../atlas/patterns/ratchet-constraint.md`](../atlas/patterns/ratchet-constraint.md) — the
  stay-or-improve rule the factory applies to these skills.
- Root [`../PLAN.md`](../PLAN.md) — where the "not tiered" classification is recorded.
