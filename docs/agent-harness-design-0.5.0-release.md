# Agent Harness Design 0.5.0 release verification

Date: 2026-09-09. The seven-step implementation is complete upstream; this
receipt records the final distribution candidate and its verification. Remote
publication is verified after the commit containing this receipt is pushed.

## Delivered scope

1. Calibrated the existing entry and seven references, separating general
   responsibilities, conditional choices, interface contracts and historical advice.
2. Added a basic model/tool loop and twelve-component architecture guide.
3. Added model-selection guidance and seven dated provider profiles: OpenAI,
   Anthropic, Google, DeepSeek, Moonshot, Z.ai and Qwen.
4. Shortened the entry to 146 lines with focused routes for design, review,
   diagnosis and migration; all seventeen references are reachable.
5. Added historical cases and evidence-driven maintenance guidance.
6. Extended the existing evaluation corpus and corrected observed failures.
7. Published upstream 0.5.0, refreshed its Marketplace pin and generated
   catalogs/package, and verified the extracted package in fresh sessions.

The [upstream evaluation and A1–A9 results](https://github.com/rocky2431/agent-harness-design-skill/blob/e744f4b0acd06290171f8c8888bced9fddb9d446/reports/v0.5.0-evaluation.md)
retain the approved plan, source snapshots, initial/intermediate failures,
corrections and final evidence. Marketplace [AGENTS.md](../AGENTS.md) records the
source-repository map, independent Skill boundaries and upstream-first maintenance.

## Exact distribution identity

| Item | Value |
|---|---|
| Plugin version | `0.5.0` |
| Upstream repository | `rocky2431/agent-harness-design-skill` |
| Source commit | `e744f4b0acd06290171f8c8888bced9fddb9d446` |
| ZIP | `packages/kimi/agent-harness-design-0.5.0-e744f4b0acd0.zip` |
| ZIP SHA-256 | `194b8492b4c87d24d4b556658e5b9a7b4a506b229d0c0790ac7ee29c75cc6d46` |
| Skill tree SHA-256 | `25a335fdade59170bac56994ffa7318bc9447c59de1e2e99d14f7020a38b9e91` |

`sources.json` selects the exact upstream commit. Codex and Claude catalogs point
to that source; Kimi and zCode catalogs point to the ZIP above, with zCode also
carrying its SHA-256. Catalogs that expose a version report 0.5.0; Codex identifies
the source by commit and reads the upstream manifest. Older published ZIPs remain.
The extracted Skill tree matches the final behavior/discovery evidence digest.

The immutable upstream `v0.5.0` tag points to the initial release commit. The final
Marketplace pin includes Windows test/telemetry portability corrections and a
report correction; the Skill tree and plugin payload are unchanged. Final source
CI passed on Linux, macOS and Windows:
[run 34304184154](https://github.com/rocky2431/agent-harness-design-skill/actions/runs/34304184154).

## Checks and fresh-session observations

| Check | Observed result |
|---|---|
| Upstream deterministic checks | 35 unit tests passed; compilation and Skill validation passed; missing-reference counterexample rejected |
| Final focused Skill behavior | 16 answers and 8 blind grades completed; candidate 8/8 graded passes, baseline 6/8 |
| Final discovery probes | 12/12 accepted selections across positive, negative, ambiguous and coexistence cases |
| Marketplace consistency | `python3 scripts/catalog.py check` passed |
| Marketplace unit tests | All 4 tests passed |
| Rebuild reproducibility | All 26 source/catalog/package files compared byte-identically before and after `catalog.py build` |
| Extracted-package sessions | Both fresh Codex sessions completed; requested reads reached the relevant packaged references |

Local network generation used `SSL_CERT_FILE=/etc/ssl/cert.pem` to select the
system CA bundle; TLS verification remained enabled.

[Raw package-session evidence](agent-harness-design-0.5.0-package-eval.json)
records Codex CLI 0.153.4, gpt-5.6-sol, low reasoning, one trial per case, fresh
temporary homes/workspaces, and explicit loading from the extracted ZIP. No model
grading was used for these two distribution checks; their concrete answers were
read and reviewed:

- Case 29 read the packaged state and failure references, preserved corrections,
  authority and pending-operation identity, and required reconciliation before a
  retry. It allowed independent work while the dependent outcome remained unknown.
- Case 31 read the adaptation, OpenAI, Google and architecture references and
  distinguished the documented target protocols/settings with source links and a
  checked date. It did not apply the consulting model's settings to both targets.

These observations complete A9 for portable package loading and useful guidance
in the tested Codex configuration. Command records show requested reads, not proof
of attention. Provider/API statements added by an answer beyond the profiles are
not independently certified by this package test.

## Evidence limits

The seven model profiles are supported by dated primary documentation. This
release does not establish measured optimization gains on all seven target
systems. The behavioral samples are targeted, small and partly model-graded;
they do not establish a universal quality, speed or cost improvement.

Installer layouts were checked for six hosts. Actual Skill behavior and fresh
package loading were tested on Codex. The ZCode/GLM-5.3 probe failed before a final
answer, with cause unresolved; native Kimi/zCode/Claude runtime acceptance and
all target-model API round trips remain unverified. No existing global plugin
installation was changed by publication.
