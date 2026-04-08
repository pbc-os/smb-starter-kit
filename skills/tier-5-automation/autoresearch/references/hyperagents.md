# HyperAgents — Reference

**Source:** Zhang et al. (2026). *HyperAgents: Self-Referential Agents that Improve Their Own Improvement Process.* arXiv:2603.19461. Meta / UBC / Vector Institute / Edinburgh.
**Code:** https://github.com/facebookresearch/Hyperagents

## Core Concept

Hyperagents are **self-referential agents** that integrate a task agent (which solves the task) and a meta agent (which modifies both itself and the task agent) into a **single editable program**. Crucially, the meta-level modification procedure is itself editable — enabling **metacognitive self-modification**.

## Key Insight

Prior self-improving systems (like the Darwin Gödel Machine) use a **fixed, handcrafted** mechanism to generate improvements. The DGM relies on a fixed prompt that analyzes past results and generates improvement instructions. That mechanism cannot itself be improved — it bottlenecks the system.

Hyperagents solve this by making the improvement mechanism itself part of the editable program. The agent can improve:

1. How it solves tasks (the task agent)
2. How it generates future improvements (the meta agent)

This is **metacognitive self-modification** — improving the process of improvement.

## Architecture: DGM-H (Darwin Gödel Machine with Hyperagents)

```
Archive of Hyperagents
    │
    ├── Select parent (probabilistic, biased toward high performers)
    │
    ├── Metacognitive Self-Modify
    │   ├── Meta agent sees: past performances + its own repo
    │   ├── Meta agent generates: code diff (new hyperagent)
    │   └── The diff can modify BOTH the task agent AND the meta agent
    │
    ├── Evaluate on computable tasks
    │   ├── Task inputs → Task agent of new hyperagent → Solve task
    │   └── Score the result
    │
    └── Add new hyperagent to archive (stepping stones for future)
```

## Key Mechanisms

1. **Open-ended exploration (archive).** Maintains a growing population of hyperagent variants. Successful variants serve as stepping stones. Parent selection is probabilistic and inversely proportional to number of children (this encourages diversity rather than exploiting a single lineage).

2. **Metacognitive self-modification.** The agent improves its own improvement process. Examples discovered by DGM-H in the paper:
   - Persistent memory (tracking what's been tried)
   - Performance tracking (monitoring which changes helped)
   - Structured evaluation pipelines (multi-stage with checklists)
   - Domain knowledge accumulation (building internal knowledge bases)

3. **Transfer across domains.** Meta-level improvements (better self-improvement strategies) transfer to new domains. Hyperagents optimized on paper review + robotics tasks generated significantly better task agents on Olympiad-level math grading — a domain they never trained on.

## Results (from the paper)

- **Coding (Polyglot):** 0.084 → 0.267 on full benchmark (comparable to handcrafted DGM)
- **Paper review:** 0.0 → 0.710 on test set (exceeds static baseline of 0.630)
- **Robotics reward design:** 0.060 → 0.372 on test set
- **Cross-domain transfer:** imp@50 = 0.639 on math grading, starting from paper review / robotics hyperagents

## Ablation Results (what matters)

Both components are necessary for sustained improvement:

- **Without self-improvement:** DGM-H w/o self-improve achieves 0.0 on paper review, 0.213 on robotics. Metacognitive self-modification is essential.
- **Without open-ended exploration:** DGM-H w/o archive shows 0.0 on paper review, 0.116 on robotics. The archive of stepping stones is essential — you can't just keep the latest version.

## Relevance to the Autoresearch Skill

| HyperAgents Concept | Autoresearch v2 Application |
|---|---|
| Metacognitive self-modification | Meta-reviewer can update `research.md` with learned insights |
| Archive of stepping stones | `archive.json` maintains top N diverse configs |
| Open-ended exploration | Coverage map steers toward unexplored parameter dimensions |
| Task agent + meta agent separation | Researcher (task) + Meta-reviewer (meta) |
| Parent selection with diversity bias | Branch from archive entries that are different from current |

## Scope Note

The autoresearch skill in this repo is not a reimplementation of HyperAgents — it's a much simpler, file-based adaptation of a few of its ideas to the Karpathy-style experiment loop. In particular, autoresearch doesn't edit its own agent code at runtime. It only lets the meta-reviewer append domain insights and exploration strategy to `research.md`. For a full metacognitive agent architecture, go to the paper and the reference implementation.
