# Local invoice summary — approach decision and implementation specification

Prepared 2026-09-08 from `sources/brief.md` and the local sample files. Self-contained:
a receiving agent needs this document and the paths it names, not the originating dialogue.

**Status: proposal delivered for review. The owner has not accepted it, and this document
does not authorize implementation.** Requirements A1–A4 below are already-accepted owner
requirements carried over unchanged from `sources/brief.md`; items P1–P6 are assistant
proposals on points the brief leaves to the implementation.

## Answer and status

**Recommended approach: a single-file Python 3 standard-library script,
`invoice_summary.py`, structured as three strictly sequential phases — validate every row,
then aggregate, then write once.**

1. **Read and validate.** Parse the whole input with `csv.DictReader` and validate *every*
   data row, with no reference to `status`. Hold the parsed rows in memory (the operational
   inputs described in the brief are small local files). Any invalid row → write a message
   to stderr and exit nonzero **without having opened the output path for writing**.
2. **Aggregate.** Only after all rows pass: walk the rows in input order, keep those with
   `status == "finalized"`, and accumulate per currency into a `dict` — a running
   `total_cents` sum of the signed integers and a list of the original `invoice_id`
   strings appended in input order.
3. **Write once.** Serialize the currencies sorted by code into a JSON list and write it,
   via a temporary file in the output's directory followed by `os.replace` (proposal P1).

This is the simplest structure that carries A3's guarantee by construction rather than by
luck: the output file cannot be replaced by a partial or wrong report, because nothing is
written until the entire input has been proven valid. "Simplest" is applied as a
tie-breaker among approaches that already satisfy A1–A4 — not as grounds to drop one.

Nothing in this document has been executed. It is a design derived by reading the brief
and the sample files.

## Reasons and evidence

**Validation must run before the finalized/cancelled filter — this is the decisive point.**
`sources/malformed.csv` line 8 is `100,cancelled,EUR,not-an-integer` (assistant inspection,
2026-09-08). The only invalid row in the supplied failure fixture is *cancelled*, which is
exactly what A3's clause "even if the invalid row is cancelled" targets. A program that
filtered by status before validating would skip that row, exit 0, and overwrite a
previously good report — passing casual testing while violating A3 on the supplied
evidence. Phase 1 therefore validates every row, including cancelled ones.

**Amount validation must be stricter than a bare `int()` call.** Probe on this machine's
Python 3.12.10 (assistant-run, 2026-09-08): `int("1_0")` returns `10`, `int("١٢")` and
`int("１２")` return `12`, and `int(" 5")` returns `5`. A naive `try: int(value)` is
therefore a weaker validator than it appears — it silently coerces values that are not
plain signed integers. Specify `re.fullmatch(r"[+-]?[0-9]+", value)` first, then `int()`
(proposal P2). The supplied `not-an-integer` sample would be rejected either way; the
probe, not the sample, is the reason for the stricter rule.

**Invoice IDs must remain strings and must not be de-duplicated.** `sources/invoices.csv`
contains `001`, `002`, `099`, with three separate rows carrying `001`. Numeric conversion
would render `001` as `1`, and set-based collection would drop two USD rows — both
violating A2. Use a list of strings appended in input order.

**`invoice_count` counts finalized rows, not distinct IDs** (assistant interpretation of
A1 read against A2). A2 states repeated IDs are distinct rows, so `invoice_count` always
equals `len(invoice_ids)`. Flagged here because the alternative reading changes the
expected USD count from 3 to 2.

**Derived expected output for `sources/invoices.csv`.** The finalized rows are
`001/USD/120`, `001/EUR/100`, `002/USD/-20`, `001/USD/5`; `099/USD/700` is cancelled and
excluded:

```json
[
  {"currency": "EUR", "invoice_count": 1, "total_cents": 100, "invoice_ids": ["001"]},
  {"currency": "USD", "invoice_count": 3, "total_cents": 105, "invoice_ids": ["001", "002", "001"]}
]
```

This was computed by hand from the file's contents, **not** by running a program. It is the
fixture the implementation must reproduce, and confirming it is part of execution.

**Input-unchanged baseline (A4).** `sources/input.sha256` contains
`fed9dd1d20771e2fd2cb26000c82369148ae435c282428957caa21b35b16b830`, which the assistant
confirmed on 2026-09-08 matches `shasum -a 256 sources/invoices.csv` exactly. No hash was
published for `sources/malformed.csv`; the assistant computed
`690b34f4c8c5a7da5cbb535fa5dc7a5a7442be84d0ee8b8f97cfa5659a5efeb5` as a working baseline.
Inputs are opened read-only and never written.

**Environment.** Python 3.12.10 is present on this machine and `csv`, `json`, `os`,
`tempfile` and `re` import successfully (assistant check, 2026-09-08). No installation or
global configuration change is required, satisfying A4. The specification needs nothing
newer than CPython 3.8.

## Alternatives and objections

| Approach | Verdict |
| --- | --- |
| Stream rows and write output incrementally | **Rejected.** Violates A3: a bad row late in the file leaves a partial output or a replaced good report. |
| Two passes over the file (validate, then re-read and aggregate) | **Equivalent guarantee, more code**, plus a second read that can disagree with itself if the file changes between passes. Parked: reopen only if inputs outgrow memory. |
| Third-party CSV or dataframe library | **Rejected.** Violates the brief's stdlib-only constraint and A4's no-install rule. |
| Validate first, then write directly to the output path (no temp file) | **The strongest objection to the recommendation.** It already passes the supplied failure case, and the temp file is extra machinery. Kept anyway — see below. |

On that last point: A3's second sentence — "No partial result may replace a previous
successful report" — constrains the *state of the output*, and a direct write that dies
mid-stream (full disk, interrupt, crash) leaves precisely that partial result. Writing to a
temporary file in the same directory and calling `os.replace` is a few standard-library
lines and closes the gap. It is an implementation choice made under A3, not an additional
requirement — hence P1, subject to review. If the owner prefers the smaller version, the
supplied acceptance evidence still passes; the guarantee simply becomes narrower.

## Conditions, limits, and next action

- **Not executed.** No program was written and nothing was run. The expected JSON above and
  every claim about the program's behaviour are derived, not observed.
- **In-memory whole-file processing** suits the local operational files the brief
  describes (the sample is 148 bytes). A very large input would require the parked
  two-pass variant.
- **"Currencies sorted alphabetically"** is specified as Python's default string sort
  (code-point order). This coincides with alphabetical order for uppercase ASCII currency
  codes, which is all the samples contain; the intended order for non-ASCII codes is
  undefined by the brief and no such case exists locally.
- **Untested CSV shapes.** The samples contain no quoted fields, embedded commas, CRLF
  line endings, BOM, blank lines, or ragged rows (assistant inspection: `file` reports
  "CSV text", first bytes carry no BOM, `cat -ve` shows LF endings). P3 proposes failing
  before write on structurally bad rows, but no local evidence exercises those shapes.
- **Requirement provenance.** A1–A4 are taken as owner premises from `sources/brief.md`
  and the live request. They were not independently verified against any operational
  process, and no external research was performed — the request states all domain facts
  are supplied.
- **Next action:** the owner reviews this decision and P1–P6. On acceptance, hand this file
  to an implementing agent; the first useful execution step is to build the script and run
  the three checks in the table below.

## Execution handoff

### Accepted owner requirements

IDs and meanings preserved verbatim from `sources/brief.md`. Test cases appear in the
evidence column only — they are not additional requirements.

| ID | Required outcome and pass condition | Evidence or independent check |
|---|---|---|
| A1 | Only finalized rows contribute to totals. Signed integer `amount_cents` is summed per currency, so negative refunds reduce that currency's total. Output is a JSON list, currencies sorted alphabetically; each object has `currency`, `invoice_count`, `total_cents`, `invoice_ids`. | `python3 invoice_summary.py sources/invoices.csv <out>.json` exits 0; parsed output equals the derived fixture above — EUR `{count 1, total 100}` and USD `{count 3, total 105}`, EUR before USD. The cancelled `099/USD/700` row must be absent from both the total and the ID list; USD's 105 confirms the `-20` refund was subtracted. |
| A2 | Original `invoice_id` strings are retained — leading zeros intact, repeated IDs kept as separate entries — in input order within each currency. | In the same output, USD `invoice_ids` is exactly `["001","002","001"]` (order, repetition and leading zeros all preserved) and EUR is `["001"]`. Values are JSON strings, not numbers. |
| A3 | Every input row is validated before the output is replaced. A noninteger `amount_cents` causes a nonzero exit and leaves an existing output byte-for-byte unchanged, even when the invalid row is cancelled. No partial result replaces a previous successful report. | Run the A1 command to produce a good output; record its SHA-256. Re-run against `sources/malformed.csv` writing to the **same** output path. Expect a nonzero exit, a message on stderr, and an output file whose SHA-256 is unchanged. Note the fixture's bad row is `cancelled`, so a program that filters by status before validating will fail this check. |
| A4 | Input bytes remain unchanged; no dependencies installed and no global configuration changed. Local code, tests and output in this workspace are authorized; publication and external writes are out of scope. | After all runs, `shasum -a 256 sources/invoices.csv` still yields `fed9dd1d…b830` (matching `sources/input.sha256`) and `sources/malformed.csv` still yields `690b34f4…feb5`. The script imports only standard-library modules; no install command is run. |

### Implementation proposals — awaiting the owner's decision

These are the assistant's choices on points the brief leaves open. They are **not**
requirements, and none narrows or widens A1–A4's meaning.

- **P1 — Atomic output replacement.** Write to a temporary file in the output's directory,
  then `os.replace` onto the target, so an interrupted write cannot leave a partial file.
  Rationale and the counterargument are in "Alternatives and objections".
- **P2 — Strict amount syntax.** Validate `amount_cents` with `re.fullmatch(r"[+-]?[0-9]+",
  value)` before `int()`, rather than relying on `int()` alone, which accepts underscore
  separators and non-ASCII digits. This is a stricter input policy than the brief's wording
  literally requires and needs the owner's assent.
- **P3 — Structural row validation.** Treat a row with a missing/empty `currency` or
  `status`, a missing `amount_cents` field, or a column count that disagrees with the
  header as a validation failure in phase 1 — same nonzero exit, same untouched output.
  Alternative if rejected: such rows raise an uncaught exception, which still exits nonzero
  before any write but gives a worse message.
- **P4 — Failure reporting.** Exit code `2` on validation failure, with a one-line stderr
  message naming the input path, the 1-based row number and the offending value. Exit `0`
  on success with no stdout output.
- **P5 — Output formatting.** UTF-8, `json.dump(..., indent=2)` plus a trailing newline,
  no key sorting (keys emitted in the A1 order: `currency`, `invoice_count`, `total_cents`,
  `invoice_ids`). Affects only byte-level formatting, not the parsed structure A1 requires.
- **P6 — Non-finalized statuses.** A status other than `finalized` — including values
  neither sample contains — excludes the row from totals but is not an error. A1 says
  include only finalized rows; A3 names only a noninteger amount as a failure. Rejecting
  unknown statuses would add a rule the owner did not state.

### Exclusions, constraints and authority

- **Excluded by the brief:** databases, cloud services, currency conversion, non-stdlib
  dependencies, and any command line other than
  `python3 invoice_summary.py INPUT.csv OUTPUT.json`.
- **Excluded by this turn's instruction:** the implementation itself, any execution
  workflow, and modification of the supplied source files or any other package.
- **Constraints:** work stays inside this workspace; publication and external writes are
  outside the task; no global configuration changes.
- **Open decisions and their owner:** P1–P6 are the owner's to accept, amend or reject.
  There is no unresolved *business* decision — A1–A4 are settled.
- **Authority:** delivering this document is not acceptance and grants no implementation
  authority. An implementing agent needs the owner's go-ahead.

### Workspace and paths

- Workspace root: `/private/var/folders/cm/zpwxmr512rq1qz4_0_ryz8t80000gn/T/four-skill-acceptance-g3wlbf6c/deep-final`
- Requirements source: `sources/brief.md`
- Fixtures: `sources/invoices.csv` (valid), `sources/malformed.csv` (invalid row, cancelled),
  `sources/input.sha256` (baseline hash for `invoices.csv`)
- Working draft with the evidence trail: `docs/invoice-summary/THOUGHTS.md`
- This specification: `docs/invoice-summary/RESULT.md`
- Planned but not yet created: `invoice_summary.py` and its test output
- Not a git repository; no revision identifiers exist. The only artifacts created for this
  inquiry are the two documents above; no source file was modified.
- **Next useful action on acceptance:** implement the three phases as specified, then run
  the A1, A3 and A4 checks in that order — the A3 check depends on a good output produced
  by the A1 run. No receiving skill or additional state file is required; this document
  and `THOUGHTS.md` carry the full context.
