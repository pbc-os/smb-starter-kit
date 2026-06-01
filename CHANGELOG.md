# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0] — 2026-06-01

### Added

- **`data-lake-starter` skill (tier-1-foundation) — v1.0.0.** The new "start here" foundation skill: stands up a secure, empty BigQuery data lake in the owner's own GCP project. Builds four layered datasets (raw → clean → marts → archive), three least-privilege service accounts (ingest / transform / agent, where the agent identity reads `marts` only and never raw), Workload Identity Federation for keyless CI (no downloadable service-account keys), BigQuery data-access audit logging, a billing budget + alert, and enables Secret Manager. Ships two paths from one folder — an agent-guided `gcloud`/`bq` walkthrough and a full Terraform scaffold (`templates/terraform/`) — plus three references: the **SMB Data Lake Hardening Standard** (`references/hardening.md`), the manual-boundary guide for connecting your own sources (`references/connecting.md`), and an honest cost breakdown (`references/cost.md`). Connectors are deliberately **not** shipped — connecting sources is a manual trust decision by design.

### Changed

- **README reframed from "skills catalog" to "starter kit with a path."** Retitled to **SMB Starter Kit**. The repo now leads with: stand up a secure data lake, then climb the tiers (each reads/writes the same lake you own). Added the foundation arc (`data-lake-starter → secrets-manager → connect sources → semantic-layer-audit`), listed `data-lake-starter` as the first Tier-1 skill, and refreshed the dependency map to root on it. The Story now centers the data lake the rest is built on.
- **Skill catalog count corrected to 24** and the previously-unlisted `long-running-agent` skill added to the Tier-5 table to match `index.json`.
- **`skills/index.json`** — added `data-lake-starter` as the first foundation entry; regenerated date.

### Hardened (pre-publish multi-agent review)

- **`data-lake-starter` now opens with a "How to use this skill" callout** telling owners to clone the kit into an AI agent (Claude Code / Claude Desktop) and let the agent drive setup — the secure on-ramp the skill depends on.
- **`data-lake-starter` gained a "Working With the User — Transparency & Consent" section** directing the agent to announce consequential actions (enabling billable APIs, creating identities, granting IAM), surface cost/access/reversibility, and pause for explicit approval before each create/enable/grant. Path A and Path B both reference it (`terraform plan` → show user → approve → `apply`).
- **Consent gates added to consequential skills** — `slack` (posting/DMs/channels), `google-ads` (live-spend mutations), `gmail` (sending + filters), and `secrets-manager` (confirm before create/delete; never echo a secret value).
- **Terraform hardening** — Workload Identity now pins trust to a branch/ref (`github_ref`), not just the repo; the authorized-view note no longer suggests papering over the conflict with `ignore_changes = [access]`; an empty `billing_account` (no budget alert) is now a loud warning; added ADC auth + `TF_VAR_project_id` guidance and a first-apply API-propagation retry note.
- **Proprietary scrub** — genericized example identifiers: removed a real internal BigQuery table name from the semantic-layer template, the owner's first name from `morning-briefing` examples, and exact ad-budget / forecast-accuracy / experiment-count figures from `README` and `revenue-forecaster`.

## [1.3.0] — 2026-04-08

### Changed

- **README onboarding flow rewritten.** Default install path is now Claude Desktop (5-minute, no-terminal experience), with CLI agents (Claude Code, Codex, Gemini CLI, Goose) as a power-user fallback. Cut the "paste this URL into ChatGPT first" intro and the npm-based 15-minute install ceremony. Collapsed the three duplicated install sections into one tight Setup section. Reduced the "agents vs skills vs tools" explanation from three metaphors (chef + employee + GitHub Actions) to one (employee). README went from 437 lines / 15 sections to 281 lines / 12 sections.
- **README emoji-stripped.** All section header emojis removed (8 instances) for a cleaner, more professional render. Skill catalog tables and the rest of the page were already emoji-free.
- **README copy fixes.** Setup section now references the bundled "Claude chat, Claude Cowork, and Claude Code" framing from claude.com/download (verified live). Fixed brittle in-page anchor link in the developer-skip line — now points to the `./skills/` directory directly.

### Added

- **`docs/advanced-onboarding.md`** — New page documenting the chatbot-bridge pattern (LLM.txt → handoff packet → CONTINUE.md) as an *advanced* alternative for users who can't or won't install Claude Desktop. The pattern still works and the supporting files (LLM.txt, CONTINUE.md) are preserved unchanged in functionality, but they're now clearly framed as the advanced path rather than the default. Headers added to both LLM.txt and CONTINUE.md pointing readers at Claude Desktop first.

## [1.2.3] — 2026-04-08

### Changed

- **`morning-briefing` skill → v1.3.1** — Added two more patterns to the "false urgency" failure-mode list, both surfaced by a real-world re-run: (1) "thread between two other people that doesn't address or @-mention the user" — drop entirely rather than including as informational, and (2) "CI / build / deploy failure where the actual deploy step succeeded" — modern pipelines run non-blocking audit and security-scan jobs alongside the main build, and a failure in one of those with `Deploy: succeeded` in the same run is a code-quality follow-up, not a production incident. The agent must read the per-job status from the body before classifying.

## [1.2.2] — 2026-04-08

### Changed

- **`morning-briefing` skill → v1.3.0** — Email urgency classification now requires reading the message body with `gws gmail +read`, not just inspecting sender + timing metadata. Promotion to "Urgent" requires at least one explicit escalation signal in the body: direct address, explicit ask, deadline language, decision request, escalation phrasing, or money/risk on the line. Sender being a "key contact" is no longer sufficient on its own. New "False urgency failure mode" section catalogs the patterns that *look* urgent but usually aren't (vendor status replies, two-reply threads, monthly statements, automated "Important" subjects). Calendar and metric urgency rules are unchanged (mechanical, no body to read). Discovered when a real-world test flagged a vendor reply as urgent purely because of sender + timing pattern, with no actual escalation in the body.

## [1.2.1] — 2026-04-08

### Changed

- **`morning-briefing` skill → v1.2.0** — Added a real Setup Verification section that checks `gws` install, auth, and required scopes (gmail, calendar) before running, and routes the user to the `google-workspace` skill on failure rather than silently producing a partial briefing. Tasks and Drive scopes are now treated as recommended-but-not-blocking. Restructured the briefing format spec to require sub-bullets and clickable source links on every urgent item — a bare one-line urgent item is now non-conformant. New "How to build the source links" reference table covers Gmail / Calendar / Drive / Tasks URL patterns. Example briefing rewritten to demonstrate the new format. Discovered while running the skill end-to-end on a real inbox (NYC butcher shop) and finding that bare urgent lines forced the user to go hunting for the email.

## [1.2.0] — 2026-04-07

### Added

- **`revenue-forecaster` skill** (Tier 5 — Automation) — Weekly, 13-week, daily, and stress-test revenue forecasting for multi-entity SMBs. Blends recent trend + seasonal + YoY with per-entity holiday multipliers and week-of-month adjustments. Ships with a fixed eval script (`scripts/eval.py`) that the `autoresearch` skill can drive to self-tune the parameters on your own historical data. Pure-Python stdlib implementation, no numpy/pandas dependencies.
- **`patent-figure` skill** registered in README and `index.json` — previously present on disk but unregistered. Frontmatter brought into spec compliance (added `version`, `tier`, `requires`).

### Changed

- **`autoresearch` skill → v2.0.0** — Upgraded from a single-agent loop to a three-agent pipeline (researcher, critic, meta-reviewer) with holdout validation, coverage-driven exploration, a stepping-stones archive, and metacognitive self-modification. New reference docs: `hyperagents.md` (citing Zhang et al. 2026), `multi-agent-patterns.md` (generator/verifier separation), and the existing Karpathy reference. The v1 file-based loop is preserved — the new agents layer on top of it.
- **Clawdbot branding scrubbed** from `secrets-manager` skill, reference files, test scripts, and top-level docs. Section 4 of the secrets-manager skill rewritten as a generic "Integration with Your Agent Runtime" pattern that works with any CLI agent.
- **`smb-pbc/agent-skills-public` install-command URLs** replaced with the correct `pbc-os/agent-skills-public` across README, CONTINUE.md, LLM.txt, and semantic-layer-audit README.
- **README** rewritten for clarity — consolidated three duplicated install sections into one, removed noisy per-skill install command columns from the skill tables, updated the dependency map, reframed Tier X as "Experimental" instead of "Agent Performance", added Goose to the CLI agent alternatives table.

### Removed

- **`remedy` skill** moved out of the public repo (archived locally) — the Wendy Rhoades / Billions framing was a distraction from its actual substance, and the skill depended on sub-agent infrastructure that wasn't portable across runtimes.
- **`x402-customer-agent` skill** moved out of the public repo — it was a vertical-specific client for a private commerce API, not a reusable skill. Will live in a separate repo.

### Fixed

- `nano-banana/scripts/make_transparent.py` — removed dead code in the feathering block that was running the same Gaussian blur twice.
- `google-ads/SKILL.md` — added missing `from google.api_core import protobuf_helpers` import in the `pause_campaigns` and `pause_keywords` code snippets (copy-pasted code would raise NameError without it).
- `secrets-manager/scripts/verify_access.sh` — fixed six dead error branches where `if [ "$?" -eq 0 ]` after command substitution was always truthy. Rewrote with `if VAR=$(cmd)` pattern.
- `slack-directory/lookup.sh` — added `.ok` check on the Slack API response so silent auth failures no longer look like "no matches found." Fixed wrong line-number references in SKILL.md and lookup.sh.
- `google-sheets/SKILL.md` — wired in the previously-orphaned `references/smb-sheet-templates.md`.
- `gmail/SKILL.md` — linked to `references/email-templates.md` from within the skill body.
- `playbook-discovery/SKILL.md` — removed dead reference to non-existent `revenue-forecaster` skill (the reference is now live after this release).
- Stale `2025-01-XX` example dates in tier-2 and tier-3 skills bumped to `2026-01-XX` to match the current year.
- `slack` and `slack-directory` frontmatter — added missing `requires.secrets: ["slack-bot-token"]`.
- `brand-identity`, `creative-matrix`, `nano-banana` — genericized example brand names (removed references to real internal projects).

## [1.1.0] — 2026-03-23

### Added

- **Skill Spec** (`skills/SKILL_SPEC.md`) — Standard schema for skill frontmatter, directory structure, setup verification pattern, and agent-agnosticism guidelines.
- **Skills Index** (`skills/index.json`) — Machine-readable index of all skills with metadata, dependencies, and coming-soon listings. Agents can parse this to discover, validate, and plan installations.
- **Morning Briefing Config Template** (`templates/briefing-config.yaml`) — Starter configuration with toggleable sections, delivery methods, schedule, and key contacts.
- **Creative Matrix Example** (`examples/starter-set-example.md`) — Complete 6-concept starter set for a premium butcher shop showing expected output format and quality bar.
- **Remedy Trigger Criteria** — Concrete, actionable criteria for when to trigger a remedy session (consecutive failures, repeated mistakes, user frustration signals, cascading errors, avoidance behavior, system-level breakdowns).
- **Shared Communication Patterns** (`skills/shared/smb-team-messaging.md`) — Moved platform-agnostic messaging best practices to a shared location referenced by both Slack and Google Chat skills.
- **CHANGELOG.md** — This file.

### Changed

- **Google Ads** — Restructured as API-first. Browser automation demoted to "fallback, not recommended" with stability warnings. Removed browser mode from the main skill description.
- **Frontmatter Normalization** — All skills now use a consistent frontmatter schema with `name`, `version`, `tier`, `description`, and `requires` fields. Removed legacy runtime-specific metadata wrappers in favor of the standard schema.
- **Agent Agnosticism** — Updated language throughout to be agent-agnostic. Skills work with any AI agent (Claude Code, Codex, Gemini CLI, etc.), not just Claude Code.
- **README** — Added links to Skill Spec, Skills Index, and Changelog. Updated skill count and references.

### Removed

- **Browser-first approach in Google Ads** — Browser automation is no longer presented as an equal alternative to the API. It remains documented as a last-resort fallback.

## [1.0.0] — 2025-01-01

Initial public release with 19 skills across 5 tiers plus experimental.
