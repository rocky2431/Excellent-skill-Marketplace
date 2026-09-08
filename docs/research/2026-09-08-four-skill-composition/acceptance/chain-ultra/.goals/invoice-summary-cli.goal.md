# Goal: invoice-summary-cli

**DRAFT — not confirmed, not armed.** Checkpoint C has not been shown to the owner and
`.goals/invoice-summary-cli.decisions.md` carries no `Confirm package checkpoint` row, so
this package is a proposal for review. Delivery of `docs/invoice-summary/RESULT.md` did not
authorize execution. See `## Open items awaiting the owner` for every term still unsettled.

## Intent

Owner request, quoted from `sources/brief.md` (the material wording; no other owner
dialogue is available to this draft):

> Operations needs a local command that reads a CSV and writes a JSON summary grouped by currency.
> Use Python standard library only. It runs on local files; no databases, cloud services or currency conversion.
> The command line is: python3 invoice_summary.py INPUT.csv OUTPUT.json.

> All four criteria are owner requirements. There is no unresolved business decision. The later implementation may choose its internal design. Evidence must include the concrete output, a malformed input case, and an input-unchanged check.

Agreed intent (operational interpretation, this draft's wording): produce a working
`invoice_summary.py` in this workspace that satisfies the already-accepted requirements
A1-A4 unchanged, and show the three kinds of evidence the brief demands - the concrete
output, the malformed-input case, and the input-unchanged check.

A1-A4 and their IDs are inherited, not reopened. `docs/invoice-summary/RESULT.md` is the
upstream specification; its items P1-P6 are assistant proposals and are **not** acceptance
requirements here.

## Boundary

**Scope.** Receiving root is this workspace,
`/private/var/folders/cm/zpwxmr512rq1qz4_0_ryz8t80000gn/T/four-skill-acceptance-g3wlbf6c/chain-ultra`.
Writable: `invoice_summary.py`, `verification/`, `.work/`, `.goals/`. Read-only and
preserved byte-for-byte: `sources/**` and `docs/**`, including `sources/invoices.csv`,
`sources/malformed.csv`, `sources/input.sha256`, `docs/invoice-summary/RESULT.md` and
`docs/invoice-summary/THOUGHTS.md`. No dependency installation, no global configuration
change, no network use, no publication and no write outside this workspace. The upstream
root named in RESULT.md (`.../deep-final`) is not this root and must not be touched.

Confirmed collaboration scope: **none yet.** No worker has been dispatched and none may be
until the owner answers whether this goal may use only current-host workers or also named
external agents. Availability is not authorization.

This workspace is not a Git repository, so arming would require `--allow-no-git` and loses
step-history coverage and committed writer-session exclusion.

**Confidence.** Never call the program correct, passing or done without this session's own
output from the anchor command. `docs/invoice-summary/RESULT.md` states its expected JSON
was computed by hand and that nothing in it was executed; it is a specification, not evidence.

**Inference.** Never conclude the program's behaviour from reading its source or from the
upstream document. Run it. A file that exists is not a file that is correct.

## Stop condition

Stop when `bash verification/invoice_acceptance.sh` exits 0 and the required independent
review for A4 has passed, or at the ceiling below.

success: verified
ceiling: 6

The ceiling counts completion attempts, not turns or tool calls, and is a proposal awaiting
the owner (see `## Open items awaiting the owner`). Exhausting it is an unverified exit.

## Anchor

```
bash verification/invoice_acceptance.sh
```

budget: 2 minutes

The script drives the real command line the brief specifies - `python3 invoice_summary.py
INPUT.csv OUTPUT.json` - on both supplied fixtures and compares the parsed output with the
accepted result. It checks outcomes only: it never inspects the program's internal design,
never asserts a byte-level output format, and never requires a particular exit code beyond
"nonzero" on the malformed fixture, so an implementation that rejects P1-P6 can still pass.
It writes only inside `.work/`, reads `sources/` without modifying it, and exits nonzero
today because `invoice_summary.py` does not exist yet. **It has never been executed**; only
`bash -n` syntax checking was run in this draft-only turn.

## Means

What this draft believes it takes to reach the intent. Every label below is agent-proposed
and needs the owner's assent before it binds a run.

- `[load-bearing]` keep the brief's command line exactly: `python3 invoice_summary.py INPUT.csv OUTPUT.json`
- `[load-bearing]` Python 3 standard library only - no installed dependency, no global configuration change
- `[load-bearing]` reach a green anchor on both supplied fixtures before any completion claim
- `[load-bearing]` leave `sources/**` and `docs/**` byte-for-byte unchanged
- `[droppable]` the three-phase structure recommended by RESULT.md (validate every row, then aggregate, then write once) - it is the upstream recommendation, not an accepted requirement; drop it only for a structure that still satisfies A3, and record why
- `[droppable]` a single-file script - drop it if a helper module makes the result clearer, since the brief constrains the command line, not the file count
- `[droppable]` P1 atomic replacement via a temporary file and `os.replace` - a proposal, droppable until the owner accepts it

## Roles

- **lead**: this session, with the owner. Interview, draft and read-back; owns this package.
  fallback: none; an interview cannot be delegated to something the owner is not talking to.
- **design critic**: an independent context that reads `sources/brief.md`, this draft and
  `docs/invoice-summary/RESULT.md` - never this session's argument for them - before
  checkpoint C. **Not yet run:** dispatch is blocked on the unconfirmed collaboration scope.
  fallback: any available independent context; if none is authorized, disclose the missing
  critique as a limit rather than recording a pass.
- **carry out**: the run's own session. Writes `invoice_summary.py` and any local test it wants.
  fallback: an authorized worker given this Carry-over, the failed attempts and the evidence.
- **anchor**: `bash verification/invoice_acceptance.sh`. No model in the path.
  fallback: none; if it cannot run, the outcome is unknown, which is the answer.
- **reviewer**: an independent session under the identity `independent-reviewer`, run at
  proposed completion on the bounded inputs in `## Verification`. It must not have written
  `invoice_summary.py`. It receives the criteria, the original brief and the fixtures, not
  the author's defence, and writes the receipt itself.
  fallback: another independent session using the same approved identity and criteria; never
  the generating session. If none is reachable, pause unverified and report the missing review.

## Verification

```json
{
  "source": "owner-approved",
  "basis": "DRAFT, not yet approved. The evaluator is verification/invoice_acceptance.sh, written in this turn from the already-accepted A1-A4 in sources/brief.md and pinned together with the two supplied fixtures and the published input hash. It has not been executed and the owner has not inspected or accepted it.",
  "protected": ["verification/invoice_acceptance.sh", "sources/invoices.csv", "sources/malformed.csv", "sources/input.sha256"],
  "covers": {"A1": "anchor", "A2": "anchor", "A3": "anchor", "A4": "review"},
  "review": {
    "path": ".goals/invoice-summary-cli.review.json",
    "verifiers": ["independent-reviewer"],
    "inputs": ["invoice_summary.py", "sources/brief.md", "sources/invoices.csv", "sources/malformed.csv", "sources/input.sha256"]
  }
}
```

A1-A3 are observable end to end from the command line the brief names, so the anchor decides
them. A4 is only partly mechanical: the anchor re-checks both input hashes after every run,
but "no dependency installed and no global configuration changed" is a claim about the whole
program and its execution, which an independent reader has to judge against the source. That
judgement is assigned to review, and the reviewer's receipt must cite the actual file text.

`invoice_summary.py` does not exist yet, so `review.inputs` cannot be snapshotted and
`protected` cannot be pinned until the run creates it; arming before then will refuse.

## Acceptance

Unordered; each line stands alone. IDs and requirement text are inherited verbatim from
`sources/brief.md` and must not be renamed, renumbered or reworded. `[x]` is a claim, and
only the anchor's output or the review receipt is its evidence.

- [ ] A1: Include only finalized rows in totals. Sum signed integer amount_cents separately per currency; refunds are negative and reduce the total. Output is a JSON list, currencies sorted alphabetically; each object has currency, invoice_count, total_cents, invoice_ids.
- [ ] A2: Retain the original invoice_id strings, including leading zeros and repeated IDs, in input order within each currency. Repeated IDs are distinct rows, not duplicates to discard.
- [ ] A3: Validate every input row before replacing the output. A noninteger amount_cents fails with nonzero exit and leaves an existing output byte-for-byte unchanged, even if the invalid row is cancelled. No partial result may replace a previous successful report.
- [ ] A4: Input bytes remain unchanged. Do not install dependencies or change global configuration. Local code, tests and output in this workspace are authorized; publication and external writes are outside this example task.

## Open items awaiting the owner

Concrete execution terms this noninteractive draft could not settle. Each is a proposal;
none is agreed, and the package cannot be armed while any of them is open.

- Collaboration scope: current-host workers only, or also named external agents? Proposed:
  current-host independent sessions only. Blocks the design critic and the reviewer.
- Reviewer identity `independent-reviewer` and the A4-to-review assignment.
- The evaluator `verification/invoice_acceptance.sh` itself: the owner inspects and accepts
  it, or amends it, before `source: owner-approved` is true.
- `ceiling: 6` completion attempts, and the native time/token budgets that sit beside it.
- P1-P6 from `docs/invoice-summary/RESULT.md`: still open proposals. They are deliberately
  absent from Acceptance and from the anchor's checks.
- Arming with `--allow-no-git`, or creating a repository baseline first.
- Whether the run may create `invoice_summary.py` at all - implementation authority has not
  been granted by this exercise.

## Carry-over

Read this before acting and rewrite it before finishing or at any known context transition.
Reconcile it against the named files before relying on it; this record, not any companion
plan, is the single execution-state writer for this goal.

### State

- Package status: draft only. Nothing armed, nothing implemented, no business command run.
- Upstream inputs read in full: `sources/brief.md`, `docs/invoice-summary/RESULT.md`.
- Fixtures verified present and unmodified this turn: `sources/invoices.csv`
  (`fed9dd1d...b830`, matching `sources/input.sha256`) and `sources/malformed.csv`
  (`690b34f4...feb5`, matching the working baseline recorded in RESULT.md).
- `verification/invoice_acceptance.sh` written this turn; `bash -n` clean; never executed.
- `invoice_summary.py` does not exist; the anchor is therefore red-by-absence, not failing.
- Owner confirmation outstanding: checkpoint A, B and C all unshown; no design critique run.

### Lessons

- Validation must precede the finalized/cancelled filter, because the only invalid row in
  `sources/malformed.csv` is `100,cancelled,EUR,not-an-integer` - a status filter applied
  first would skip it, exit 0 and overwrite a good report, passing casual testing while
  breaking A3. Any structure the run chooses has to survive that fixture.
- The upstream expected JSON was computed by hand and never executed, so the first anchor
  run is the first real observation of it; treat a mismatch as an open question about which
  side is wrong, not as an automatic implementation bug.

### Next

- Show checkpoint A/B/C to the owner and resolve `## Open items awaiting the owner`; do not
  implement, arm or dispatch until that reply exists.

## Handoff

**Do not paste this yet.** It is recorded so the owner can see exactly what starting would
run. It becomes valid only after checkpoint C is confirmed, the open items above are
settled, and the package is armed (which in this non-Git workspace needs `--allow-no-git`).

```
/ultra-goal:goal-run invoice-summary-cli
```

The run that eventually starts is the run, not the designer: A1-A4, the boundary, the
anchor, the stop condition, the verification contract and the labelled means are frozen for
it. If one of them turns out to be wrong, it stops and writes a row under
`## Challenges from the run` in `.goals/invoice-summary-cli.decisions.md` instead of editing
the term. Before any completion claim it finishes its edits, obtains the independent A4
review, and calls `goal_run.py verify invoice-summary-cli --root <project> --session-id
<current-native-session-id>`, reading that attempt's recorded result before reporting.
