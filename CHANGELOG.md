# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
