# Grok native integration acceptance — 2026-10-14

The native integration and installation checks passed in the current macOS user
environment. Intermittent network transport errors remain unresolved: the final
installed-package goal run recovered through Grok's own retries and completed,
but this is not evidence that their underlying cause was removed.

## Published and installed

| Plugin | Version | Upstream commit |
| --- | --- | --- |
| Agent Delegation | 0.9.2 | `36bbc23ac090f35464dada4fe536c2506eb2264a` |
| Task State | 0.6.0 | `be03cf4cd5a88802241da723dbfa42f660d8d9af` |
| UltraGoal | 2.20.0 | `62f75e07dd9a9cb74ed40adade462934fc72baf4` |
| Building Rules | 0.2.0 | `642ab25d1149307e1dc70a91165d4cd21126aac1` |

Marketplace distribution commit: `8dc2d0a0f0f9b167f324b6dab43e8a14faf69467`.
Deep Thinking 0.3.1, Agent Harness Design 0.5.2 and Awesome HTML 0.1.0 retain
their existing pins. All seven plugins were read back from Codex, Claude Code,
zCode and Grok native plugin managers. The 28 installations' 568 component files
matched the pinned ZIP contents. Existing Codex Hook trust entries were preserved.
Already-running conversations must reload or start a new session to load changes.

## Observed native behavior

Tests used Grok 1.0.52, the real HOME, account, default model configuration and
configured MCP/Hindsight integration. No clean HOME or disabled-MCP acceptance
environment was substituted. Source-candidate probes selected native plugin
directories; final installed probes omitted that override entirely.

- Agent Delegation completed file read/write, named-session recall, explicit
  model selection and one-time result collection. A Grok-origin Claude mission
  woke its idle parent through native background completion without another
  user prompt or model polling.
- Task State and Building Rules injected their actual context through native
  PostToolUse hooks. A fresh installed-plugin session recovered the expected
  task marker and engineering core without manually reading either file.
- UltraGoal's Stop hook continued unfinished work. A native background producer
  completed, woke the idle session and delivered its result once. The final
  installed run doubled 21 to 42, passed the protected verification command and
  reached `completed` after 377.387 seconds, from one initial client prompt.
- A separate native FIFO handoff ended one turn and resumed work in a new turn.
  Cancellation paused the goal, cancelled its wait and released the process lock.
  Reload and actual native compaction recovered the current task context while
  preserving the paused goal. The cancellation fixture waits for the asynchronous
  StopCancelled hook before asserting state.
- The final installed goal and context probes had no RPC errors or unexpected
  hook failures. Intentional Stop blocks are host control decisions, not failed
  integration execution.

## Network findings and remaining limit

Two earlier failed delegations crossed macOS sleep intervals of 950 and 197
seconds. Agent Delegation now holds a process-scoped `caffeinate -i` assertion
during queued/executing work and releases it afterward. An actual managed Grok
run verified both the assertion and its release and completed without retries.
This prevents idle sleep; it does not override explicit system sleep.

Separately, Marketplace refresh exposed a missing Python default CA bundle.
Restoring the standard certificate link to the installed certifi bundle made
default urllib requests to GitHub succeed with certificate verification enabled.
This was a Python installation issue, not proof about Grok's TLS implementation.

The final installed goal run recorded an HTTP/2 keep-alive timeout at 342.195
seconds and a TLS handshake EOF at 345.385 seconds. Grok recovered and completed
the protected verification. There was no system sleep in that interval. Current
connections used the machine's existing Clash TUN/proxy route; direct-to-TUN and
explicit-loopback-proxy HTTP/1.1 and HTTP/2 handshake probes all succeeded.
Those probes do not identify which network hop caused the intermittent failure.
Grok's stable updater reported 1.0.52 as current, with no update available.

The native sampler already [rebuilds with HTTP/1.1 after transport failure](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-sampler/src/actor/request_task.rs).
No speculative proxy rerouting, credential changes, certificate bypass or
duplicate outer retry loop was applied. Transport recovery is observed; removal
of the remaining network fault is not established.

## Validation and evidence

Agent Delegation: 103 tests, 21 skipped. Task State: 56 passed. Building Rules:
6 passed. UltraGoal's final upstream CI passed on macOS, Linux and Windows;
the five new Grok tests and 138 package-surface tests also passed locally.
Marketplace check and six tests passed, and rebuilding preserved all 55 catalog
and archive artifacts byte for byte. The generic Skill validator rejects
UltraGoal's pre-existing `when_to_use` field; its repository contract and native
plugin validation accept that field, which was not removed to satisfy the generic
validator.

Local evidence directory: `/tmp/grok-delegation-research/`. Key receipts are
`installed-goal-result.json`, `installed-goal-acp.ndjson`,
`installed-context-result.json`, `handoff-result.json`, `cancel-r2-result.json`,
`recovery-result.json`, `power-managed-result.json`, `python-ca-repair.json`,
`network-route-probe.json` and `installed-hooks-integrity.json`. These are local
probe artifacts, not distributed plugin files or a permanent evidence archive.
