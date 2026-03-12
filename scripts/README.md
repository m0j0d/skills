# Scripts

## Behavioral Evals

Use the official skill-creator eval pipeline, not a custom runner.

```bash
# From Claude Code, invoke the skill-creator's eval workflow:
# 1. Spawn with-skill and baseline subagents in parallel
# 2. Grade outputs with grader agent
# 3. Aggregate and launch viewer

# See: skill-creator SKILL.md "Running and evaluating test cases"
```

The eval pipeline spawns real Claude Code subagents that attempt tasks with and without the skill, producing actual output files. An independent grader agent scores assertions against those outputs. Results are aggregated with statistics (mean, stddev, delta) and displayed in an HTML viewer for human review.

### Quick reference

- **Eval prompts**: `docs/test-results/<skill>/eval.json`
- **Grader agent**: `~/.claude/plugins/.../skill-creator/agents/grader.md`
- **Aggregation**: `python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>`
- **Viewer**: `python <skill-creator-path>/eval-viewer/generate_review.py <workspace> --skill-name <name>`
