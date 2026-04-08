---
name: autoresearch
version: 1.0.0
tier: automation
description: "Autonomous iterative improvement loop for any measurable system. Inspired by Karpathy's autoresearch pattern. Agent forms hypotheses, makes single changes, evaluates, keeps improvements, discards regressions."
requires:
  bins: []
  skills: []
---

# Autoresearch

**Autonomous iterative improvement for any measurable system.**

Inspired by [Karpathy's autoresearch](https://github.com/karpathy/autoresearch) — "you're not touching code like you normally would. Instead, you're programming the program.md files that provide context to the AI agents."

## Triggers

- "autoresearch"
- "run autoresearch on..."
- "iteratively improve..."
- "optimize [X] autonomously"
- "run experiments on..."
- "self-improve [system]"
- "find better parameters for..."
- "tune [X]"
- User wants to autonomously improve any measurable system

## The Pattern

The agent works in an autonomous loop:

```
┌─────────────────────────────────────────────┐
│  1. MEASURE    → Establish baseline metric  │
│  2. ANALYZE    → Find biggest weakness      │
│  3. HYPOTHESIZE → Form a specific theory    │
│  4. CHANGE ONE THING → Modify parameters    │
│  5. EVALUATE   → Run the fixed eval         │
│  6. KEEP/DISCARD → Did metric improve?      │
│  7. LOG        → Record the experiment      │
│  8. REPEAT     → Go to step 2              │
└─────────────────────────────────────────────┘
```

The separation of concerns is critical:

| File | Role | Who Edits |
|------|------|-----------|
| `research.md` | Agent instructions — what to optimize, how to think, domain knowledge | Human |
| `eval script` | Fixed measurement — runs the metric calculation | Nobody (frozen) |
| `parameters file` | Tunable knobs — the ONLY thing the agent changes | Agent |
| `experiments/` | Accountability trail — every experiment logged | Agent (append-only) |

**The eval script is sacred.** The agent NEVER modifies it. This prevents the agent from "improving" its score by weakening the test.

## Prerequisites

- A **measurable objective** — a number you want to go up or down
- An **evaluation method** — a script, API call, or command that produces that number
- **Tunable parameters** — things you can change that affect the metric
- Sufficient **historical data or test cases** to evaluate against

## Workflow

### Phase 1: Define the Objective

Ask the user (or infer from context):

1. **What are we optimizing?** (e.g., forecast accuracy, prompt quality, page load time)
2. **What's the metric?** (e.g., MAE, F1 score, p95 latency, Lighthouse score)
3. **Direction?** Lower is better or higher is better?
4. **How do we measure it?** (e.g., run backtest against actuals, run eval suite, run benchmark)
5. **What can we change?** (e.g., model parameters, prompt text, config values, weights)
6. **What data do we evaluate against?** (e.g., last 30 days of actuals, test dataset, production logs)

### Phase 2: Scaffold the Files

Create 4 files in the project. Adapt file names and formats to the domain:

#### 1. `research.md` — Agent Instructions

This is the "program.md" equivalent. It tells the agent:
- What system we're optimizing
- What the metric means
- Domain knowledge and constraints
- What parameters are available to tune
- Rules of engagement (one change at a time, always backtest, etc.)

Use the template: [templates/research-template.md](templates/research-template.md)

#### 2. Eval Script — Fixed Measurement

A script that:
- Takes the current parameters as input (or reads them from the parameters file)
- Runs the evaluation against the test data
- Outputs a single primary metric (and optionally secondary metrics)
- Is deterministic — same parameters always produce the same score

This can be:
- A Python/Node/Shell script
- A CLI command
- An API call
- A database query
- A `curl` command that hits a test endpoint
- Anything that returns a number

**Mark it read-only after creation:**
```bash
chmod 444 eval.py  # or eval.sh, eval.js, etc.
```

#### 3. Parameters File — The Tunable Knobs

A structured file (YAML, JSON, Markdown, or whatever fits) containing every parameter the agent can adjust. Each parameter should have:
- Current value
- Description of what it controls
- Acceptable range or constraints (if any)
- Last modified date and experiment that changed it

Use the template: [templates/parameters-template.md](templates/parameters-template.md)

#### 4. `experiments/` Directory — The Log

Each experiment gets its own file: `experiments/NNN-hypothesis-slug.md`

Use the template: [templates/experiment-template.md](templates/experiment-template.md)

### Phase 3: Establish Baseline

1. Run the eval script with current parameters
2. Record the baseline metric
3. Log as experiment #000 (the starting point)
4. Analyze the eval output — identify the biggest sources of error

### Phase 4: Run the Loop

For each iteration (default: 10 experiments per session, configurable):

#### Step 1: Analyze Current Weaknesses
- Look at the eval output from the previous run
- Identify the single biggest source of error or underperformance
- Quantify it — "Shop 1 Tuesday is 25% over-forecast" not "Tuesdays seem high"

#### Step 2: Form a Hypothesis
- Be specific: "Reducing the Shop 1 Tuesday multiplier from 1.0 to 0.80 will reduce MAE because we're consistently over-forecasting by 25% on that day"
- Target the biggest error first (highest expected impact)
- **One variable at a time** — never change two things simultaneously

#### Step 3: Make the Change
- Modify ONLY the parameters file
- Change exactly one parameter (or one tightly-coupled group)
- Record what was changed and why

#### Step 4: Evaluate
- Run the eval script
- Compare the new metric to the previous baseline
- Check for regressions in secondary metrics (e.g., overall MAE improved but one segment got worse)

#### Step 5: Decision

**If metric IMPROVED:**
- KEEP the change
- Update the parameters file (it stays modified)
- Update the baseline metric
- Log the experiment as ✅ SUCCESS

**If metric WORSENED or stayed the same:**
- REVERT the change (restore previous parameter value)
- Log the experiment as ❌ FAILED
- Note WHY it failed (overcorrected? wrong direction? no effect?)

**If metric improved overall but regressed on a segment:**
- Use judgment — is the tradeoff acceptable?
- Consider a smaller change
- Log the nuance

#### Step 6: Log the Experiment
Write the experiment file with:
- Hypothesis (what you expected)
- Change made (exact before/after values)
- Results (metric before and after)
- Decision (KEEP/DISCARD)
- Reasoning (what you learned)

#### Step 7: Repeat
- Go back to Step 1 with the new baseline
- Stop when: max iterations reached, metric converges (last 3 experiments all failed), or time limit reached

### Phase 5: Report Results

Present a summary table:

```markdown
## Autoresearch Session: [System Name]
Date: YYYY-MM-DD
Duration: [time]

### Results
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| [Primary] | X.XX | X.XX | -X.X% |
| [Secondary] | X.XX | X.XX | -X.X% |

### Experiments Run: N
| # | Hypothesis | Change | Result |
|---|-----------|--------|--------|
| 1 | [description] | [param: old → new] | ✅ -X.X% |
| 2 | [description] | [param: old → new] | ❌ Made worse |
| ... | ... | ... | ... |

### Parameters Changed (kept)
[List of all parameters that were modified and kept]

### Remaining Weaknesses
[What the biggest remaining errors are — seeds for next session]
```

### Phase 6: Optionally Set Up Recurring Runs

If the user wants continuous improvement:
- Set up a cron job (nightly, weekly, etc.)
- The cron runs the loop autonomously
- Each session picks up from the current parameters and continues improving
- Results are posted/logged for human review

## Rules of Engagement

1. **One variable at a time.** Never change two parameters in one experiment. If you're tempted to change multiple things, run them as separate experiments.

2. **The eval script is sacred.** Never modify the eval script. If the eval is wrong, tell the human — don't "fix" it yourself. Modifying the eval is like a student grading their own test.

3. **Always revert failures.** If a change doesn't improve the metric, the parameters file must be restored to its previous state before the next experiment.

4. **Log everything.** Even failed experiments are valuable data. "Tuesday multiplier 0.75 overcorrected" prevents trying 0.70 next.

5. **Target the biggest error.** Don't fine-tune a 2% error when there's a 25% error somewhere else. Fix the big things first.

6. **Diminishing returns are real.** If the last 3-5 experiments all failed, you may be near the optimum for this parameter space. Report that and suggest what NEW parameters or data sources might unlock further improvement.

7. **Git branch per session.** If working in a git repo, create a feature branch for the session. Commit each kept change. This makes it easy to review or revert.

8. **Be honest about sample size.** If a parameter only has 2 data points, note it. Don't over-tune on small samples.

## Example Applications

### Revenue Forecasting
- **Metric:** Mean Absolute Error (MAE) — lower is better
- **Eval:** Backtest last 30 days of forecasts against actuals from BigQuery
- **Parameters:** Day-of-week multipliers, weather effects, seasonal adjustments, baseline revenue
- **Data:** Historical revenue, weather data, events calendar

### Prompt Engineering
- **Metric:** Eval score on test cases — higher is better
- **Eval:** Run prompt against 50 test inputs, score outputs with rubric
- **Parameters:** System prompt sections, few-shot examples, temperature, formatting instructions
- **Data:** Test input/output pairs with expected answers

### API Performance
- **Metric:** p95 latency — lower is better
- **Eval:** Run load test (k6, wrk, etc.) against staging endpoint
- **Parameters:** Connection pool size, cache TTL, batch sizes, timeout values, query limits
- **Data:** Load test results

### Ad Spend Optimization
- **Metric:** ROAS (Return on Ad Spend) — higher is better
- **Eval:** Pull last 14 days of ad spend vs revenue attribution
- **Parameters:** Daily budgets per campaign, bid adjustments, audience targeting weights
- **Data:** Google Ads + revenue data

### Lighthouse / Web Performance
- **Metric:** Lighthouse Performance score — higher is better
- **Eval:** `lighthouse --output=json URL | jq '.categories.performance.score'`
- **Parameters:** Image compression levels, lazy loading thresholds, bundle split points, cache headers
- **Data:** Lighthouse audit results

### LLM Fine-tuning Config
- **Metric:** Validation loss — lower is better
- **Eval:** Train for N steps, report val loss
- **Parameters:** Learning rate, batch size, warmup steps, weight decay, dropout
- **Data:** Training/validation datasets

### Cost Optimization
- **Metric:** Cost per unit ($/order, $/API call, $/user) — lower is better
- **Eval:** Calculate cost metrics from billing data over last 30 days
- **Parameters:** Instance sizes, scaling thresholds, caching policies, batch sizes
- **Data:** Cloud billing, usage metrics

## Tips

- **Start simple.** You can always add more parameters later. Begin with the obvious knobs.
- **Warm up the eval.** Run it 2-3 times before starting to make sure it's stable and deterministic.
- **Watch for overfitting.** If you're tuning on a small dataset, you might optimize for noise. Use a holdout set if possible.
- **Session length matters.** 10-20 experiments per session is usually the sweet spot. More than that and you start making micro-adjustments with diminishing returns.
- **Let it run overnight.** The best use of autoresearch is setting it up, going to sleep, and waking up to a log of experiments and better parameters.

## Related Skills

- `playbook-discovery` — Find repeatable workflows to optimize
- `semantic-layer-audit` — Document the data sources your eval script pulls from

---

*"The human iterates on the program.md files that provide context to the AI agents... You're programming the program.md."* — Andrej Karpathy
