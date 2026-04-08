---
name: autoresearch
version: 2.0.0
tier: automation
description: "Autonomous iterative improvement for any measurable system. A three-agent loop (researcher, critic, meta-reviewer) with holdout validation, coverage-driven exploration, and metacognitive self-modification. Extends Karpathy's autoresearch with generator/verifier separation and ideas from the HyperAgents paper."
requires:
  bins: []
  skills: []
---

# Autoresearch

**Autonomous iterative improvement for any measurable system.**

Built on [Karpathy's autoresearch](https://github.com/karpathy/autoresearch) pattern, extended with:

- **Critic agent with binary pass/fail gates** and holdout validation — generator/verifier separation so the agent can't grade its own homework
- **Coverage-driven exploration** instead of pure hill-climbing — don't spend 40 experiments tuning one knob when another knob has never been touched
- **Metacognitive self-modification** — a meta-reviewer agent that can improve the researcher's own optimization strategy between runs
- **Archive of stepping stones** — maintain a diverse population of good configurations, not just the single best, so you can branch out when stuck in a local optimum

See the `references/` folder for the academic and practitioner sources behind each of these extensions.

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

Three agents work in a pipeline, coordinated by a small set of files on disk:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌──────────────────┐     │
│  │  RESEARCHER │───▶│   CRITIC    │───▶│  META-REVIEWER   │     │
│  │  (proposes) │    │ (validates) │    │ (every N exps)   │     │
│  └─────────────┘    └─────────────┘    └──────────────────┘     │
│        │                   │                    │              │
│        ▼                   ▼                    ▼              │
│  1. Analyze weakness  4. Holdout gate      7. Review full log  │
│  2. Form hypothesis   5. Overfitting check 8. Update strategy  │
│  3. Change 1 param    6. Binary pass/fail  9. Suggest new      │
│     + run eval           → KEEP/DISCARD       dimensions       │
│        │                   │                    │              │
│        └───────────────────┴────────────────────┘              │
│                            │                                   │
│                    ┌───────▼────────┐                          │
│                    │ COVERAGE MAP   │                          │
│                    │ What's been    │                          │
│                    │ explored?      │                          │
│                    │ What's missing?│                          │
│                    └────────────────┘                          │
│                            │                                   │
│                    ┌───────▼────────┐                          │
│                    │    ARCHIVE     │                          │
│                    │ Top N configs  │                          │
│                    │ Branch from    │                          │
│                    │ diverse parents│                          │
│                    └────────────────┘                          │
└─────────────────────────────────────────────────────────────────┘
```

### File Roles

| File | Role | Who Edits |
|------|------|-----------|
| `research.md` | Agent instructions — what to optimize, how to think, domain knowledge | Human initially; **meta-reviewer can append** |
| `eval script` | Fixed measurement — runs the metric calculation | **Nobody (frozen)** |
| `parameters file` | Tunable knobs — the ONLY thing the researcher changes | Researcher agent |
| `experiments/` | Accountability trail — every experiment logged | All agents (append-only) |
| `archive.json` | Top N parameter configs with scores | Researcher agent |
| `coverage.json` | Which parameter dimensions have been explored | Auto-tracked |

**The eval script is sacred.** No agent ever modifies it. This prevents "improving" the score by weakening the test — the single most common failure mode in autonomous optimization systems.

## Prerequisites

- A **measurable objective** — a number you want to go up or down
- An **evaluation method** — a script, API call, or command that produces that number
- **Tunable parameters** — things you can change that affect the metric
- Sufficient **historical data or test cases** to evaluate against (enough to split into train + holdout)

## Workflow

### Phase 1: Define the Objective

Ask the user (or infer from context):

1. **What are we optimizing?** (e.g., forecast accuracy, prompt quality, page load time, ad ROAS)
2. **What's the metric?** (e.g., MAE, F1, p95 latency, Lighthouse score, cost-per-conversion)
3. **Direction?** Lower is better, or higher is better?
4. **How do we measure it?** (e.g., backtest against actuals, run eval suite, run benchmark)
5. **What can we change?** (e.g., model parameters, prompt sections, config values, weights)
6. **What data do we evaluate against?** (e.g., last 30 days of actuals, test dataset, production logs)
7. **Can we split the data?** The eval should support a `--holdout` flag so the critic can validate on data the researcher never saw.

### Phase 2: Scaffold the Files

Create 6 files in the project. Adapt file names and formats to the domain.

#### 1. `research.md` — Agent Instructions (mutable)

The "program.md" equivalent from Karpathy's original. It tells the researcher agent:

- What system we're optimizing
- What the metric means
- Domain knowledge and constraints
- What parameters are available to tune
- Rules of engagement

**v2 change:** The meta-reviewer agent can append to `research.md` in a clearly marked `## Learned Insights` section. This is the metacognitive self-modification idea — the agent improves not just the parameters, but its own optimization strategy.

Use the template: [`templates/research-template.md`](templates/research-template.md).

#### 2. Eval Script — Fixed Measurement

A script that:

- Takes the current parameters as input (or reads them from the parameters file)
- Runs the evaluation against the test data
- Outputs a single primary metric (and optionally secondary metrics)
- Is deterministic — same parameters always produce the same score
- **Supports a `--holdout` flag** to evaluate on a held-out data split (the critic uses this)
- **Outputs a per-segment breakdown** so the critic can check for regressions, not just the aggregate metric

This can be a Python/Node/Shell script, CLI command, API call, database query, etc.

**Mark it read-only after creation:**

```bash
chmod 444 eval.py  # or eval.sh, eval.js, etc.
```

#### 3. Parameters File — The Tunable Knobs

A structured file (YAML, JSON, Markdown — whatever fits the domain) containing every parameter the agent can adjust. For each parameter:

- Current value
- Description of what it controls
- Acceptable range or constraints
- Last modified date and the experiment that changed it

Use the template: [`templates/parameters-template.md`](templates/parameters-template.md).

#### 4. `experiments/` Directory — The Log

Each experiment gets its own file: `experiments/NNN-hypothesis-slug.md`.

Use the template: [`templates/experiment-template.md`](templates/experiment-template.md).

#### 5. `archive.json` — Stepping Stones Archive

Maintain the **top N parameter configs** (default: 5) with their scores. Instead of always branching from the current best, the researcher can branch from any archived config — this is how you escape local optima.

```json
{
  "entries": [
    {
      "id": "exp-025",
      "metric": 3.50,
      "params_snapshot": { },
      "lineage": "baseline → exp-001 → exp-009 → exp-025",
      "notes": "Best blending weights, no structural features"
    }
  ],
  "max_entries": 5
}
```

Keep configs that are **diverse**, not just the top 5 by raw score. When two configs have similar scores, keep the one that's more different from existing entries — this is the quality-diversity principle from MAP-Elites and from the HyperAgents archive.

#### 6. `coverage.json` — Exploration Map

Auto-tracked file recording which parameter dimensions have been explored and how thoroughly:

```json
{
  "dimensions": {
    "blending.recent_weight": {"experiments": 12, "range_tested": [0.50, 0.90], "last_explored": "exp-036"},
    "momentum.trend_weight": {"experiments": 0, "range_tested": null, "last_explored": null},
    "mean_reversion.strength": {"experiments": 2, "range_tested": [0.2, 0.5], "last_explored": "exp-041"}
  }
}
```

The researcher agent reads this before each experiment to steer toward under-explored dimensions. **Don't spend 20 experiments micro-tuning one knob when another knob has never been touched.**

### Phase 3: Establish Baseline

1. Run the eval script with current parameters (full data **and** holdout)
2. Record the baseline metric on both splits
3. Log as experiment `#000` (the starting point)
4. Initialize `archive.json` with the baseline config
5. Initialize `coverage.json` with all parameter dimensions at 0
6. Analyze the eval output — identify the biggest sources of error

### Phase 4: Run the Loop (Three-Agent Pipeline)

#### The Researcher Agent

The researcher proposes and tests changes:

1. **Check coverage map.** Read `coverage.json`. If any dimension has 0 experiments, explore it before micro-tuning explored dimensions.
2. **Analyze current weaknesses.** Look at the eval output from the previous run. Identify the single biggest source of error. Quantify it — "Shop 1 week 3 is 7.5% under-forecast" is useful; "some weeks seem high" is not.
3. **Consider branching from archive.** If the current line of exploration has stalled (last 3 experiments failed), load a different config from `archive.json` and explore from there.
4. **Form a hypothesis.** Be specific. Target the biggest error or the least-explored dimension. One variable at a time.
5. **Make the change.** Modify ONLY the parameters file.
6. **Evaluate.** Run the eval script on the **training data**. Record the metric.
7. **Pass to critic.** If the training metric improved, hand off to the critic. If it worsened, revert immediately and log.

#### The Critic Agent

The critic validates with **binary pass/fail gates**. Verification is fundamentally easier than generation (the P vs NP intuition — checking an answer is easier than producing one). The critic doesn't propose changes — it only validates or rejects.

- **Gate 1 — Holdout validation.** Run the eval with `--holdout`. Did the metric improve on data the researcher never saw? If the training metric improved but holdout worsened → **FAIL** (overfitting).
- **Gate 2 — No-regression check.** Did any individual segment (shop, time period, category, traffic source) regress by more than 2× the overall improvement? Example: overall MAPE dropped 0.3%, but one segment got 1.5% worse → **FAIL** (robbing Peter to pay Paul).
- **Gate 3 — Stability check.** Is the improvement larger than the noise floor? If the metric only improved by 0.01% and the eval has 0.05% natural variance → **FAIL** (noise, not signal).
- **Gate 4 — Directional sanity.** Does the parameter change make domain sense? A critic with domain knowledge (from `research.md`) can flag: "You increased the holiday threshold to 3.0× — that means you're barely trimming holidays at all. This is likely overfitting to the few holiday weeks in the test set."

**Decision:** ALL gates must pass → **✅ KEEP**. Any gate fails → **❌ DISCARD** with the specific gate failure noted.

The critic's gates are defined in `research.md` and are configurable per domain. Some domains need stricter or different gates. **The critic never modifies the eval script.**

#### The Meta-Reviewer Agent (every N experiments)

Every 10 experiments (configurable), a fresh meta-reviewer agent reads the entire experiment log and does four things:

1. **Pattern analysis.** "The last 8 experiments all tried blending weight variations and 6 failed. The parameter space for blending is exhausted."
2. **Coverage gaps.** "Momentum, mean reversion, and week-of-month have never been explored. These represent structural changes that could break through the current ceiling."
3. **Strategy update.** Append to `research.md` under `## Learned Insights`:

    ```markdown
    ## Learned Insights (auto-generated by meta-reviewer)

    ### Insight from review at experiment #030 (2026-04-03)
    - Blending weights are saturated (0.78–0.82 range all within noise)
    - The remaining error is structural: week 3 consistently under-forecasts by 7%
    - RECOMMENDATION: Explore week-of-month adjustments before any more blending experiments
    - RECOMMENDATION: Try per-segment parameter overrides — segments have different error profiles
    ```

4. **Archive pruning.** Suggest removing archive entries that are clearly dominated or too similar to other entries.

This is **metacognitive self-modification** from the HyperAgents paper — the system improves not just the parameters but its own improvement strategy. A meta-reviewer is the mechanism that stops the researcher from spending 50 experiments on blending weights when the real breakthrough is a structural change the researcher couldn't see from inside the loop.

### Phase 5: Report Results

Present a summary table at the end of the session:

```markdown
## Autoresearch Session: [System Name]
Date: YYYY-MM-DD
Duration: [time]

### Results
| Metric | Before | After | Change | Holdout |
|--------|--------|-------|--------|---------|
| [Primary] | X.XX | X.XX | -X.X% | X.XX |
| [Secondary] | X.XX | X.XX | -X.X% | X.XX |

### Experiments Run: N (kept: K, critic-rejected: C, researcher-reverted: R)
| # | Hypothesis | Change | Train | Holdout | Critic | Decision |
|---|------------|--------|-------|---------|--------|----------|
| 1 | [description] | [param: old → new] | -X.X% | -X.X% | ✅ PASS | ✅ KEEP |
| 2 | [description] | [param: old → new] | -X.X% | +X.X% | ❌ Gate 1 | ❌ DISCARD |

### Critic Gate Statistics
| Gate | Passed | Failed | Rejection Rate |
|------|--------|--------|----------------|
| Holdout validation | 15 | 3 | 17% |
| No-regression | 16 | 2 | 11% |
| Stability | 14 | 4 | 22% |
| Directional sanity | 18 | 0 | 0% |

### Coverage Map
| Dimension | Experiments | Range Tested | Status |
|-----------|-------------|--------------|--------|
| blending weights | 15 | 0.50–0.90 | Saturated |
| momentum | 0 | — | Unexplored |

### Meta-Reviewer Insights
[Key strategy changes recommended during the session]

### Archive (Top 5 Configs)
[Diverse set of high-performing parameter configs]

### Remaining Weaknesses
[Biggest remaining errors — seeds for the next session]
```

### Phase 6: Optionally Set Up Recurring Runs

If the user wants continuous improvement:

- Schedule a recurring run (cron, launchd, or any scheduler your agent supports)
- Each session picks up from the current parameters and archive
- The meta-reviewer's learned insights carry forward across sessions
- Results are posted or logged for human review

## Rules of Engagement

### Core Rules (from Karpathy's original)

1. **One variable at a time.** Never change two parameters in one experiment. If you're tempted to change multiple things, run them as separate experiments.
2. **The eval script is sacred.** No agent ever modifies the eval script. If the eval is wrong, tell the human. Modifying the eval is like a student grading their own test.
3. **Always revert failures.** If a change doesn't improve the metric (or fails critic validation), restore the parameters file before the next experiment.
4. **Log everything.** Even failed experiments are valuable. "Tuesday multiplier 0.75 overcorrected" prevents trying 0.70 next. Critic rejections are especially valuable — they reveal overfitting patterns.
5. **Target the biggest error.** Don't fine-tune a 2% error when there's a 25% error somewhere else.
6. **Be honest about sample size.** If a parameter only has 2 data points, note it. Don't over-tune on small samples.

### v2 Rules (new)

7. **Coverage before depth.** Check the coverage map before each experiment. If any parameter dimension has 0 experiments, explore it before micro-tuning explored dimensions. Breadth-first, then depth.
8. **Critic has veto power.** If the critic rejects an experiment that the researcher thought improved the metric, the critic wins. No appeals. This is the generator/verifier separation principle.
9. **Branch from the archive, not just the current best.** When the current line of exploration stalls (3+ consecutive failures), load a different config from the archive and explore a different direction. Don't keep bashing your head against a local optimum.
10. **Meta-reviewer doesn't touch parameters.** The meta-reviewer can only append to `research.md` (under `## Learned Insights`) and update the archive. Its job is strategy, not tactics.
11. **Holdout is sacred too.** The researcher never sees holdout results. Only the critic runs holdout evaluation. If the researcher starts using holdout patterns to inform hypotheses, the holdout loses its value. Treat it like a sealed envelope.
12. **Diminishing returns trigger meta-review.** If the last 5 experiments all failed or were critic-rejected, trigger a meta-review immediately (don't wait for the scheduled interval). The parameter space may be exhausted and the system needs a strategic pivot.
13. **Structural changes > parametric tweaks.** When the meta-reviewer identifies that the remaining error is structural (e.g., "week-of-month patterns"), recommend adding **new parameter dimensions** rather than continuing to tune existing ones. This may require a new eval script version — flag it for the human.

## Example Applications

### Revenue Forecasting

- **Metric:** Mean Absolute Percentage Error (MAPE) — lower is better
- **Eval:** Backtest the last N weeks of forecasts against actuals
- **Parameters:** Blending weights (recent / seasonal / YoY), day-of-week multipliers, holiday multipliers, outlier thresholds, decay factors
- **Data:** Historical revenue or deposit data
- **Pairs with:** `revenue-forecaster` skill — which ships with an eval script and parameters file pre-wired for autoresearch

### Prompt Engineering

- **Metric:** Eval score on test cases — higher is better
- **Eval:** Run prompt against 50 test inputs, score outputs with a rubric
- **Parameters:** System prompt sections, few-shot examples, temperature, formatting instructions
- **Data:** Test input/output pairs with expected answers

### API Performance

- **Metric:** p95 latency — lower is better
- **Eval:** Run a load test (k6, wrk, hey) against a staging endpoint
- **Parameters:** Connection pool size, cache TTL, batch sizes, timeouts, query limits
- **Data:** Load test results

### Ad Spend Optimization

- **Metric:** ROAS (Return on Ad Spend) — higher is better
- **Eval:** Pull last 14 days of ad spend vs revenue attribution
- **Parameters:** Daily budgets per campaign, bid adjustments, audience targeting weights
- **Data:** Ad platform data + revenue data
- **Pairs with:** `google-ads` skill

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
- **Eval:** Compute cost metrics from billing data over the last N days
- **Parameters:** Instance sizes, scaling thresholds, caching policies, batch sizes
- **Data:** Cloud billing and usage metrics

## Tips

- **Start simple.** You can always add more parameters later. Begin with the obvious knobs.
- **Warm up the eval.** Run it 2–3 times before starting to make sure it's stable and deterministic.
- **Watch for overfitting.** If you're tuning on a small dataset, you might optimize for noise. Use a holdout set.
- **Session length matters.** 10–20 experiments per session is usually the sweet spot. Beyond that you start making micro-adjustments with diminishing returns — let the meta-reviewer pivot you.
- **Let it run overnight.** The best use of autoresearch is setting it up, going to sleep, and waking up to a log of experiments and better parameters.

## Credits & Prior Art

This skill stands on the shoulders of several sources. The extensions in v2 are applications of ideas from the references below.

- **[Andrej Karpathy — `autoresearch`](https://github.com/karpathy/autoresearch)** ([announcement thread](https://x.com/karpathy/status/2030371219518931079)) — the original pattern: a human writes `program.md` files that instruct an agent to iterate on experiments overnight. The single-file simplicity, the sacred eval, the git-log-as-experiment-trail, and the "you're programming the program.md" framing all come from here. See [`references/karpathy-autoresearch.md`](references/karpathy-autoresearch.md).

- **Generator/verifier separation** (a.k.a. the critic pattern) — the principle that verification is easier than generation, and that you get better results by having one agent propose and a separate agent validate with concrete binary gates. Popularized in multi-agent LLM orchestration writing (see Anthropic's engineering posts on multi-agent systems) and in the trading-strategy literature around quality-diversity archives plus adversarial critics. See [`references/multi-agent-patterns.md`](references/multi-agent-patterns.md).

- **[HyperAgents — Zhang et al. (2026)](https://arxiv.org/abs/2603.19461)** ([code](https://github.com/facebookresearch/Hyperagents)) — introduces **metacognitive self-modification**: the improvement mechanism itself is editable, so the agent can improve both how it solves tasks and how it generates future improvements. The meta-reviewer agent, the archive of stepping stones, and coverage-driven exploration in this skill are direct applications of ideas from that paper. See [`references/hyperagents.md`](references/hyperagents.md).

- **MAP-Elites and quality-diversity algorithms** (Mouret & Clune, 2015) — the principle that you should maintain a diverse archive of good solutions rather than just the single best, because diverse parents lead to stepping-stone discoveries. This is why the archive here is scored on quality *and* diversity, not raw metric alone.

The original insight — that you should set this up, go to sleep, and wake up to better parameters — is still Karpathy's. Everything else is scaffolding around that core idea.

## Related Skills

- `playbook-discovery` — Find repeatable workflows to optimize; use autoresearch once you know *what* to improve
- `revenue-forecaster` — Ships with an autoresearch-ready eval script, parameters file, and research.md template, so you can tune it on your own historical data
- `semantic-layer-audit` — Document the data sources your eval script pulls from

---

*"You're not touching Python files like you normally would. Instead, you're programming the program.md files that provide context to the AI agents."* — Andrej Karpathy
