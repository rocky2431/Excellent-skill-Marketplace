# Marketplace and related Skill maintenance

## Repository map

This repository is the coordination and distribution entry point for five
independent Skill source repositories. Local checkouts are siblings, not submodules
or vendored source. Resolve these paths relative to this repository; verify the Git
root and remote before editing. If a checkout is missing, locate it before proceeding.

| Plugin | Local source repository | Responsibility |
|---|---|---|
| `deep-thinking` | `../deepthink-skill` | Clarify questions, research evidence, and deliver supported judgments and actionable results. |
| `task-state-with-files` | `../plan-with-flie-skill` | Preserve task understanding, decisions, evidence, and current execution state for recovery. |
| `agent-delegation` | `../agent-delegate-skill` | Connect available agents, dispatch missions, continue sessions, and collect receipts and results. |
| `ultra-goal` | `../ultra-goal-skill` | Prepare complete goal contracts, coordinate execution, preserve continuity, and evaluate completion evidence. |
| `agent-harness-design` | `../Agent-harness-design-skill` | Maintain evolving methods and evidence for designing and evaluating Agent systems and their execution layers. |

Each source repository owns its implementation, tests, version, and releases.
[sources.json](sources.json) owns the marketplace's selected repositories, plugin
paths, versions, and full commit pins. Do not duplicate changing version numbers here.
Read the target repository's applicable instructions before making changes there.
When working directly in a sibling repository, read its own guidance; do not assume
this file was loaded automatically.

## Independent capabilities and optional composition

Deep Thinking, Task State, Agent Delegation, and UltraGoal are the four workflow
Skills. Agent Harness Design is independently maintained alongside them and is used
when the Agent system itself is the design or evaluation target.

- Preserve complete standalone use of each Skill; other Skills are optional reuse.
- UltraGoal retains its own clarification, necessary research, continuity,
  coordination, and verification without the other three installed. Its review roles
  are specialized roles, not copies of the companion Skills.
- Compose through existing artifacts and explicit handoffs, not mandatory dependency
  chains or a shared runtime. Preserve accepted requirements, corrections, authority,
  acceptance IDs, and evidence conditions across handoffs.
- Keep one current execution record and writer per task. Research history, goal
  contracts, and worker evidence may remain separate and reference that record.
- Hooks must remain silent for unselected or unrelated tasks. File existence alone
  must not activate recovery or claim ownership of another session's task.
- A successful dispatch or model turn is not business acceptance. Retain the original
  delegation ID and actual receipt; inspect unknown outcomes before retrying.

Use [docs/skill-composition.md](docs/skill-composition.md) for detailed handoff,
recovery, document ownership, and behavior-validation conventions. Keep detailed
rules there rather than maintaining a second copy here.

## Agent Harness Design is a living design and evaluation discipline

Continuously incorporate current primary documentation, architecture research,
implementation experience, incident reports, and observed failures into the upstream
Skill. Its purpose is to improve actual Agent architecture and Agent System design
judgments, not merely collect links or preserve one fixed architecture.

During Harness research, review, or maintenance, check current sources for claims
that may have changed. Revisit guidance when model or provider capabilities, host
behavior, or new failure evidence changes its assumptions.

- Record source links, publication or observation dates, model/version, host/runtime,
  task conditions, and evidence limits where available. Mark unknown details explicitly.
- Distinguish reported experience, locally reproduced findings, inference, and
  recommendations. A recent anecdote is useful evidence to investigate, not a universal
  architectural rule.
- Preserve architectures from different periods and for different models with their
  applicability, trade-offs, failure modes, and reasons for replacement. Evaluate the
  model-harness configuration; do not assume a design transfers unchanged to another
  model, host, or task distribution.
- Keep durable principles distinct from defaults, conditional patterns, and examples.
  Reassess model-compensating controls after upgrades and retire obsolete guidance from
  active recommendations while retaining useful historical evidence.
- Put concise, supported decision rules in the upstream `SKILL.md`; keep detailed
  model-specific patterns, historical comparisons, and source evidence in its existing
  `references/` structure. Reuse repository reports and evaluation artifacts for raw
  findings. Link supporting material from the Skill so installed users can find it.
- When evidence changes a recommendation, update the relevant Skill guidance and
  references together and run proportionate checks of the affected behavior. State
  which configurations were actually tested and which remain unverified.

The Marketplace distributes those upstream updates. Keep the maintained Harness
knowledge in its source package rather than creating a competing corpus here.

## Cross-repository update and validation

1. Identify affected source repositories and inspect their working trees. Preserve
   unrelated changes and research artifacts; modify only the requested scope.
2. Make behavior and Skill-content changes upstream, then run the smallest relevant
   package and behavior checks. Verify standalone use and affected handoffs when those
   behaviors change; package checks alone do not prove native-host task completion.
3. For an authorized release, commit and publish the affected upstream changes with
   appropriate versions before advancing Marketplace pins. Keep commits scoped to
   each repository; a coordinated workspace is not one Git repository.
4. Generate catalogs and packages with `scripts/catalog.py`; never edit generated
   catalogs or ZIPs directly. `refresh` advances upstream pins; `build` rebuilds
   existing pins. Prefer `refresh --plugin <id>` for a scoped update.
5. For distribution changes, run `python3 scripts/catalog.py check` and
   `python3 -m unittest discover -s tests -v`, and verify reproducible artifacts as
   described in [README.md](README.md). Preserve older ZIPs and their usable URLs.

The configured [sync workflow](.github/workflows/sync.yml) can also publish validated
upstream updates. Distinguish source changes, published upstream commits, Marketplace
pins/packages, installed copies, and newly loaded sessions when reporting status.
Updating the Marketplace does not automatically update every installed plugin.
