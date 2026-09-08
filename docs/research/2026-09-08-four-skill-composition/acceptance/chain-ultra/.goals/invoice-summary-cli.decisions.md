# Decisions: invoice-summary-cli

| Decision | Rejected | Why | Who |
| --- | --- | --- | --- |
| A1-A4 inherited verbatim as the acceptance set, IDs and wording unchanged | Restating them in this draft's own words, or renumbering them | `sources/brief.md` states all four are owner requirements with no unresolved business decision; rewording an accepted requirement silently changes what was accepted | owner |
| Python standard library only, local files, no databases, cloud services or currency conversion | A third-party CSV or dataframe library | Stated as a constraint in `sources/brief.md` and repeated by A4's no-install rule | owner |
| The command line is exactly `python3 invoice_summary.py INPUT.csv OUTPUT.json` | Any other entry point, subcommand or flag set | Fixed by `sources/brief.md`; the brief constrains the interface, not the internal design | owner |
| Evidence must include the concrete output, a malformed input case and an input-unchanged check | Unit tests alone as the evidence | Named as the evidence condition in `sources/brief.md`; the anchor is built from exactly these three | owner |
| Loop, goal-based, single main session | A graph or a workflow attachment | Routing is trivial and known - write one script, run one checker; no workflow runtime consumer has been exercised here, so no `.workflow.js` is emitted | agent |
| `bash verification/invoice_acceptance.sh` as the anchor, driving the real command line on both supplied fixtures | Running a unit suite, or diffing the output file byte-for-byte | A unit suite tests the code, not the product the brief describes; a byte diff would freeze P5's formatting and falsely reject a valid implementation that declined it | agent |
| Anchor compares parsed JSON against EUR `{count 1, total 100, ids ["001"]}` and USD `{count 3, total 105, ids ["001","002","001"]}` | Accepting any structurally valid JSON | That is what A1 and A2 mean on `sources/invoices.csv`; `invoice_count` equals `len(invoice_ids)` because A2 makes repeated IDs distinct rows | agent |
| Anchor requires only a nonzero exit and an unchanged output hash on `sources/malformed.csv` | Requiring exit code 2 or a specific stderr message | A3 says "nonzero exit"; exit `2` and the stderr wording are P4, an unaccepted proposal, and demanding them would reject a conforming program | agent |
| A1-A3 covered by the anchor, A4 by required independent review | Covering A4 by the anchor alone | The anchor can re-hash the inputs but cannot judge "no dependency installed and no global configuration changed" across the whole program; that needs an independent reader | agent |
| Reviewer is an independent session under the identity `independent-reviewer`, and must not have written `invoice_summary.py` | The implementing session reviewing its own result | The generator never signs its own receipt; for a coding goal the final review belongs to a role that did not implement it | agent |
| `success: verified` with `ceiling: 6` completion attempts | `ceiling: none` | Six attempts is ample for a single stdlib script, and an unbounded run should be the owner's explicit choice | agent |
| P1-P6 from `docs/invoice-summary/RESULT.md` stay out of Acceptance and out of the anchor | Promoting them to requirements because the upstream document recommends them | RESULT.md labels them proposals awaiting the owner; adopting one here would add an acceptance term the owner never agreed | agent |
| Carry-over in `.goals/invoice-summary-cli.goal.md` is the single execution-state writer | A companion task/plan file, or `docs/invoice-summary/THOUGHTS.md` | One state record and one writer; THOUGHTS.md is upstream research history and is read-only in this workspace | agent |
| No worker dispatched, no design critique run, nothing armed in this turn | Running the critique against the draft anyway with a local subagent | Collaboration scope is unconfirmed and availability is not authorization; this exercise is explicitly preparation-only | agent |

## Open proposals awaiting the owner

Not decisions. Nothing here has been agreed, and the package cannot be armed while any row
is open. Once the owner answers, the answer moves into the table above with `Who` = `owner`.

| Open item | This draft's recommendation | What it blocks |
| --- | --- | --- |
| Collaboration scope: current-host workers only, or also named external agents? | Current-host independent sessions only | The design critic and the required A4 reviewer; any dispatch at all |
| Inspect and accept `verification/invoice_acceptance.sh` as the evaluator | Accept as written, or amend the fixture expectations | `source: owner-approved` in `## Verification`, and arming |
| Attempt ceiling and the native time/token budgets beside it | `ceiling: 6` | Arming |
| P1 atomic replace, P2 strict amount syntax, P3 structural row validation, P4 exit code and stderr text, P5 output formatting, P6 unknown statuses | Accept P1-P3 and P6, treat P4-P5 as free implementation choices | Nothing in the anchor; they would only widen or narrow what the run must do |
| Implementation authority: may a run create `invoice_summary.py`? | Not granted by delivery of RESULT.md; needs an explicit go-ahead | The entire run |
| Arming with `--allow-no-git`, or creating a Git baseline first | Arm with `--allow-no-git` and accept the loss of step-history coverage | Arming |
| Checkpoints A, B and C, and the `Confirm package checkpoint` row with its `frozen:` digest | Show all three, in that order, before anything starts | Everything downstream; the validator reports the missing row as `OWNER_CONFIRMATION_MISSING` until then |
