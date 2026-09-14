# Three-Skill composition release validation

Observed 2026-09-14 UTC on macOS. This release implements the document ownership and
scope relationships in [skill-composition.md](../skill-composition.md). Skills remain
independently installable; composition uses existing documents and explicit selection.

| Package | Release | Source commit |
|---|---|---|
| Deep Thinking | 0.3.0 | `f60c6012312c40c04112ca0be5eaeb4a772ebb38` |
| Task State with Files | 0.5.0 | `5bfe9129faac20bbe42a90ddf9c0954e84561a9f` |
| UltraGoal | 2.19.0 | `5d860223b625d1de94847f4e6e31b979ebfa0bfb` |

## Observable behavior

Fresh Claude Code 2.1.270 CLI sessions read only the selected Skills' source entrypoints
and relevant references in isolated local fixtures. The task was to investigate or
repair a first-page-only inventory exporter against an owner-supplied two-page fixture.
Implementation cases used the original acceptance program; goal cases used a confirmed
fixture contract and the real arming and verification scripts in explicit no-Git mode.
No native Goal mode or cross-provider worker was required by the fixture tasks.

| Selected Skills | Observed result |
|---|---|
| Deep Thinking | Delivered a supported inquiry result and working record; exporter and source fixture unchanged. Final scope recheck preserved the existing acceptance and labeled the additional count policy as a proposal. |
| Task State | Repaired the exporter, passed acceptance, completed and archived its own task record. |
| UltraGoal | Repaired and verified the exporter through the goal gate; preserved frozen terms and kept state in Carry-over. |
| Deep Thinking + Task State | Reused the existing large `THOUGHTS.md`, delivered the inquiry result and created no parallel task ledger. |
| Deep Thinking + UltraGoal | Completed bounded analysis and repair with state in the existing goal; no extra inquiry or task ledger. |
| Task State + UltraGoal | Used the existing Task record, verified the goal, and updated the Carry-over locator when the completed Task record was archived. |
| All three | Repaired and verified the exporter, retained the original Task record and goal terms, and created no parallel inquiry/state ledger. |

For all five implementation cases, a separate post-session check reran the repaired
exporter and the unchanged acceptance program. Every output contained A01, A02, A03,
A04 exactly once in source order. All four goal cases retained their original frozen
digests. Mutable completion checkboxes and current state were allowed to change.

An initial Deep Thinking case promoted a proposed implementation property to a new
requirement. A first clarification still left new inferred criteria in the handoff.
The final entrypoint and template distinguish a research recommendation from a requested
contract; a fresh rerun retained the existing acceptance without inventing requirement
IDs and labeled the additional count check as optional. This observed correction does
not establish a general model compliance guarantee.

A fresh Codex CLI 0.153.4 session used the installed Task State package and an explicitly
selected large inquiry record. It read the full record, compared the actual fixture,
identified missing `beta` and `gamma`, and updated the original inquiry's current position
and result. The fixture hash was unchanged and no second state document was created.
This proves this selected-record continuation, not every host's compaction lifecycle.

## Consumer and package checks

- Task State: 55 tests passed. The new regression fails on the previous preview selector
  and passes when Current position and Carry-over take priority over large background
  sections. Partial previews remain bounded and explicitly require a full read.
- UltraGoal: 453 tests, 451 passed and two platform skips. The suite ran on a copy of
  tracked source files, preserving unrelated local research artifacts outside the package.
- All three new Carry-over examples passed the real arming fence when substituted into
  a confirmed fixture goal, without changing its frozen digest. Both UltraGoal examples
  are covered by a package consumer regression.
- The compact recovery packet for the shipped goal template retains Cadence after
  shortening the external-state guidance; the existing budget was not increased.
- Deep Thinking's package check passed four matching native manifests, one Skill, catalogs
  and 65 local links. The three packages passed native Claude manifest validation.

An independent Claude Code review found missing read/update wiring in the new Carry-over
examples, instructional text inside frozen Intent, and remaining hardcoded research file
references. These were corrected before publication. Recovery guidance was shortened;
Task State explicitly states that a borrowed goal's partial preview is not its full contract.

## Installation and evidence limits

The existing three packages were updated through Codex, Claude Code, Kimi and zCode
native managers, plus the existing Hermes Task State installation: 13 installation
entries in total. Their tracked product files were compared with final source. No new
companion dependency or global task registry was installed.

Codex native discovery found the six packaged Skills and five enabled, trusted hooks
belonging to Task State and UltraGoal. zCode required refreshing its local marketplace
before plugin update; a successful update response alone had retained old cached content.
Installed copies and freshly loaded sessions are distinct; already-running sessions may
still carry earlier instructions.

Local receipts retain prompts, native event streams, fixture paths, before/after files,
verification events, installation manifests and file hashes. They are excluded from
public distribution because they contain machine-specific execution data. This report
records the inspected observations, not a publicly reproducible unattended benchmark.

The seven-case matrix was exercised on Claude Code; it is not seven cases on every
supported host. Codex received the additional selected-record continuation check.
This release does not re-establish all autonomous wait/wake/cancellation behavior from
UltraGoal 2.18.0: the driver was unchanged, and the earlier native evidence remains
separate from these document-composition checks. Package tests and normal model endings
alone are not business acceptance.
