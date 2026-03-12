# Karpathy's Autoresearch — Reference

Source: https://github.com/karpathy/autoresearch
Post: https://x.com/karpathy/status/2030371219518931079

## Core Concept

A minimal framework where AI agents autonomously iterate on experiments to find better models/parameters. The human writes "program.md" files that instruct the agent; the agent modifies code/config, trains, evaluates, and keeps improvements.

## Key Insight

> "You're not touching Python files like you normally would. Instead, you're programming the program.md files that provide context to the AI agents."

The human's job shifts from writing code to writing instructions. The agent's job is to execute the experimental loop.

## Architecture

```
program.md      → Agent instructions (human writes)
prepare.py      → Data preparation (fixed)
train.py        → Training script (agent modifies)
eval results    → Automatic evaluation after each run
git log         → Experiment history via commits
```

## The Loop

1. Agent reads program.md for context and objectives
2. Agent modifies train.py (one change at a time)
3. Training runs for ~5 minutes
4. Results evaluated automatically
5. If improved → commit to git, update baseline
6. If worse → revert, try different approach
7. Repeat overnight
8. Human wakes up to a git log of experiments and better model

## Design Principles

1. **Single-file simplicity** — ~630 lines of training code, not a framework
2. **Fixed eval** — The measurement never changes; only the thing being measured changes
3. **One change at a time** — Isolate variables to understand what works
4. **Git as experiment log** — Every kept change is a commit with a message explaining why
5. **Overnight autonomy** — Set it running, come back to results
6. **Human-in-the-loop at the instruction level** — Human programs the program.md, not the code

## Generalization

The pattern isn't specific to ML training. It works for any system where:
- There's a measurable objective
- There are tunable parameters
- Changes can be evaluated automatically
- The evaluation is deterministic (or close to it)

This skill generalizes the pattern beyond ML to any measurable system.
