# Research Instructions — [System Name]

## Objective

**What we're optimizing:** [describe the system]
**Primary metric:** [metric name] — [lower/higher] is better
**Current baseline:** [value] (established [date])

## How to Evaluate

Run the eval script. Do NOT modify the eval script under any circumstances.

```bash
# Example:
python eval.py
# or
./eval.sh
# or
node eval.js
```

The eval script outputs the primary metric and a breakdown of errors by segment.

## Domain Knowledge

[Add context the agent needs to make good hypotheses. Examples:]
- [What drives the metric up/down]
- [Known constraints or business rules]
- [Seasonal patterns or external factors]
- [What has been tried before and failed]

## Available Parameters

See `parameters.md` for the full list. Key parameters to explore:

1. **[Parameter group 1]** — [what it controls, why it matters]
2. **[Parameter group 2]** — [what it controls, why it matters]
3. **[Parameter group 3]** — [what it controls, why it matters]

## Data Sources

- **[Source 1]:** [what it provides, how to access it]
- **[Source 2]:** [what it provides, how to access it]

## Rules

1. Change ONE parameter per experiment
2. NEVER modify the eval script
3. Always revert failed experiments before trying the next one
4. Target the biggest error first
5. Log every experiment in `experiments/`
6. Stop after [N] experiments or when the last 3 all fail

## Session Settings

- **Max experiments per session:** 10
- **Max time per session:** 30 minutes
- **Convergence threshold:** Stop if last 3 experiments all fail
- **Branch strategy:** Create a git branch per session (e.g., `autoresearch/YYYY-MM-DD`)
