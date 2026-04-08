# Multi-Agent Validation Patterns — Reference

**Sources:**

- Generator/verifier separation pattern — widely used in multi-agent LLM orchestration. See Anthropic's engineering writing on multi-agent systems and on letting Claude check its own work with separate evaluator prompts.
- Adversarial validation in ML trading strategies — quality-diversity archives paired with critic agents is a common pattern in the trading-strategy literature for preventing overfitting.
- The [P vs NP intuition](https://en.wikipedia.org/wiki/P_versus_NP_problem) — the long-standing observation that verifying a solution is fundamentally easier than producing one.

## Core Principle: Separate Production from Evaluation

> "Don't ask Claude to be perfect in one shot. Separate production from evaluation. Cache intermediates so loops are cheap. Grade on concrete binary criteria. Iterate until the evaluator is happy."

Verification is fundamentally easier than generation. Checking if an answer is correct is easier than producing the correct answer — a verifier catches mistakes the generator cannot self-detect in a single pass. Autoresearch v2 applies this to autonomous optimization: the researcher agent generates, the critic agent verifies, and the verifier has the final say.

## The Three-Role Pattern

### Researcher (Generator)

- Proposes hypotheses and makes changes
- Runs the eval on training data
- Optimistic by nature — always thinks the next change will help
- Never sees holdout data

### Critic (Verifier)

- Validates results with binary pass/fail gates
- Runs eval on holdout data that the researcher never sees
- Pessimistic by nature — assumes overfitting until proven otherwise
- Has veto power — one failed gate = experiment rejected
- Gates are concrete and binary, not subjective ("Did holdout improve? yes/no" — not "Is this a good change?")

### Meta-Reviewer (Composer / Strategist)

- Reviews the full experiment log periodically
- Identifies patterns: "You've been stuck on blending weights for 15 experiments"
- Recommends strategic pivots: "Explore structural changes instead"
- Updates the research instructions with learned domain knowledge
- Tells the researcher what's missing at the strategy level

## Binary Gate Protocol (Critic)

Gates should be:

1. **Concrete** — "Did MAPE improve on holdout?" — not "Is this a good direction?"
2. **Binary** — Pass or fail, no "maybe"
3. **Independent** — Each gate checks a different failure mode
4. **Domain-configurable** — Different systems need different gates

Default gates:

| Gate | What it checks | Failure mode it prevents |
|---|---|---|
| Holdout validation | Metric on unseen data | Overfitting to training set |
| No-regression | No segment gets 2× worse | Robbing Peter to pay Paul |
| Stability | Improvement > noise floor | Chasing random variance |
| Directional sanity | Change makes domain sense | Nonsensical parameter values |

## Coverage-Driven Exploration (QD Archive)

Instead of pure hill-climbing (keep if better, discard if worse), maintain awareness of what's been explored:

- **Coverage map.** Track which parameter dimensions have been tried and how thoroughly.
- **Exploration pressure.** Unexplored dimensions get priority over micro-tuning explored ones.
- **Archive of diverse configs.** Keep the top N configs that are meaningfully different from each other, not just the top N by score.
- **Branch from diverse parents.** When stuck, restart from a different archive entry.

This prevents the failure mode where the agent spends 40 experiments incrementing one weight by 0.02 while ignoring an entire class of structural improvements. The underlying idea traces back to **MAP-Elites** (Mouret & Clune, 2015) and the broader quality-diversity literature, which argues that the path to good solutions usually runs through diverse stepping stones rather than pure hill-climbing.

## Practical Implementation for Agents

The three roles are implemented as separate prompts / sub-agent calls:

1. **Researcher agent** — Launched for batches of experiments (e.g., 10 at a time). Has full context about the system being optimized.
2. **Critic agent** — Launched after each successful researcher experiment to validate. Short prompt — only needs the experiment result, the gate definitions from `research.md`, and holdout-eval access.
3. **Meta-reviewer agent** — Launched every N experiments (or on convergence trigger). Reads the full experiment log, identifies patterns, and appends strategic guidance to `research.md`.

The critic and meta-reviewer are **short prompts** — they don't need the full optimization context, just the artifacts and the rules. Keeping them small makes them cheaper to run and keeps them honest (a critic that shares the researcher's full context is more likely to share its blind spots).
