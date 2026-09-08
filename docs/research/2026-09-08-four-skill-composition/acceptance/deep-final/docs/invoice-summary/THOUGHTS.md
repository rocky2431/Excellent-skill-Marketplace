# Inquiry working draft — local invoice summary approach

## Current position

- **Question and purpose:** What is the simplest dependable approach for the local
  invoice-summary command described in `sources/brief.md`, and what specification does
  another agent need to build it? Purpose: give the owner a decision they can review and
  an execution-ready spec, without implementing the program in this turn.
- **Scope, intended deliverable, and sufficient outcome:** Scope is design and
  specification only, derived from `sources/brief.md` and the two local CSV examples.
  Deliverable is `docs/invoice-summary/RESULT.md` (decision + execution handoff) plus this
  draft. Sufficient when a receiving agent can build and check the program against A1–A4
  without re-interviewing the owner, and every implementation choice beyond A1–A4 is
  visibly labelled as a proposal awaiting review.
- **Stage:** Deliver (Frame → Clarify → local-source Research → Synthesize → Check done).
- **Status:** `delivered` — result written and presented; owner review pending. No
  acceptance recorded, no execution started.
- **Settled so far and the basis for each:**
  - A1–A4 are owner requirements and there is no open business decision — stated in
    `sources/brief.md`, "Accepted requirements" and its closing paragraph (user premise,
    reaffirmed in the live request; not independently verified against any ops process).
  - Validation of *all* rows must precede any output write, and must run *before* the
    finalized/cancelled filter — `sources/malformed.csv` line 8 is `100,cancelled,EUR,not-an-integer`,
    and A3 says such a file must fail "even if the invalid row is cancelled" (assistant
    inspection of the file, 2026-09-08).
  - `invoice_id` must stay a string and repeated IDs are separate rows — A2 plus observed
    values `001`, `099` and three `001` rows in `sources/invoices.csv`.
  - Bare `int()` is not a dependable integer test — probe on this machine's
    Python 3.12.10 (2026-09-08): `int("1_0")==10`, `int("١٢")==12`,
    `int(" 5")==5`. Assistant-run language probe, not the program.
  - Python 3.12.10 with `csv`, `json`, `os`, `tempfile`, `re` is present; no install needed (A4).
- **Latest material change and its basis:** Moved the amount check from "call `int()` and
  catch `ValueError`" to an explicit `^[+-]?[0-9]+$` regex before `int()`, because the
  probe above showed `int()` silently accepts underscore separators and non-ASCII digits.
  Assistant-initiated revision; not yet reviewed by the owner.
- **Still open (pivotal gaps and pending owner choices):**
  - P1–P6 in `RESULT.md` are assistant proposals on points the brief leaves to the
    implementation. Owner review settles them; none changes A1–A4's meaning.
  - Nothing here has been executed. The expected JSON for `sources/invoices.csv` was
    derived by reading the file, not by running a program. Execution must confirm it.
  - The samples contain no quoted fields, embedded commas, CRLF line endings, BOM, blank
    lines, or extra/missing columns, so no local evidence shows how those behave. Handled
    by proposal P3 (fail before write), unverified.
- **Next action and why it serves the whole inquiry:** Owner reviews the decision and
  P1–P6. On acceptance, hand `docs/invoice-summary/RESULT.md` to an implementing agent;
  that record then owns execution state. Nothing further is useful before that review.
- **Result path:** `docs/invoice-summary/RESULT.md` — written and presented 2026-09-08.

## Problem structure and current judgment

The owner's real goal (user statement in the live request) is a *dependable* small local
tool, not a minimal one: "simplest" is a tie-breaker among approaches that already satisfy
A1–A4, not a licence to drop a guarantee. A3 is the constraint that actually selects the
design, because it forbids any state in which a previous good report has been replaced by
a partial or wrong one. Every other requirement is satisfiable by several designs.

Reading the brief that way, the shape of the program is forced:

1. Read the whole input and validate **every** row, with no reference to `status`.
2. Only if all rows pass, aggregate finalized rows per currency, preserving row order.
3. Only then write the output.

The three phases must be sequential and the output file must not be opened for writing
before phase 3 succeeds. The remaining freedom — file layout, error text, exit code,
whether the final write is atomic — is internal design, which the brief explicitly leaves
to the implementation.

Assistant interpretation (flagged, not owner-stated): A1's `invoice_count` counts
*finalized rows*, not distinct IDs, so `invoice_count == len(invoice_ids)` always. This
follows from A2 ("repeated IDs are distinct rows, not duplicates to discard"); the
alternative reading would make the USD count 2 with three IDs listed, which contradicts A2.

Assistant interpretation: a row whose `status` is neither `finalized` nor `cancelled` is
excluded from totals, not an error. A1 says "include only finalized rows"; A3 names only a
noninteger `amount_cents` as a failure. Inventing a status whitelist would add a rejection
rule the owner did not state.

## Factors and evidence

| Question or claim | Why it matters | Direct source, date, and locator | Observation and applicability | Support, counterevidence, and gap | Effect on judgment |
| --- | --- | --- | --- | --- | --- |
| What must the program output for the good input? | Gives A1/A2 a concrete pass condition | `sources/invoices.csv`, inspected 2026-09-08 (6 lines incl. header) | Finalized: `001/USD/120`, `001/EUR/100`, `002/USD/-20`, `001/USD/5`; `099/USD/700` is `cancelled`. Derived: EUR → 1 row, 100; USD → 3 rows, 105, ids `["001","002","001"]` | Arithmetic derived by hand from the file, not executed. Applies only to this sample | Becomes the A1/A2 acceptance fixture in `RESULT.md` |
| Is the malformed row also non-finalized? | Decides the order of validation vs. filtering | `sources/malformed.csv` line 8, inspected 2026-09-08 | `100,cancelled,EUR,not-an-integer` — the only bad row is `cancelled` | Matches A3's clause "even if the invalid row is cancelled". No counterevidence | Decisive: a filter-first design would skip the row, exit 0 and overwrite a good report. Validate-first is required, not stylistic |
| Does `int()` reliably reject non-integers? | The amount check is the only named failure rule (A3) | Assistant probe, python3 3.12.10 on this machine, 2026-09-08 | `int("1_0")→10`, `int("١٢")→12`, `int("１２")→12`, `int(" 5")→5`; `int("5.0")`, `int("")`, `int("not-an-integer")` raise | `int()` over-accepts; it would silently coerce values that are not plain signed integers. Applies to any CPython 3.x | Revised the spec to `^[+-]?[0-9]+$` then `int()` (proposal P2). The supplied malformed sample would be caught either way — the probe, not the sample, is the reason |
| Must invoice IDs stay strings? | A2 correctness | `sources/invoices.csv`, IDs `001`, `002`, `099`; three rows share `001` | Numeric conversion would yield `1`, and de-duplication would drop two USD rows | Directly stated in A2; sample confirms both leading zeros and repeats occur | Aggregate with a `dict` keyed by currency holding an ordered list of ID strings; never a `set`, never `int` |
| Is the input hash baseline usable for A4? | A4 requires an input-unchanged check | `sources/input.sha256`; `shasum -a 256` run 2026-09-08 | `invoices.csv` → `fed9dd1d…b830`, matches the published file exactly. No published hash for `malformed.csv`; computed `690b34f4c8c5a7da5cbb535fa5dc7a5a7442be84d0ee8b8f97cfa5659a5efeb5` | Verified by the assistant on this machine. Gap: the `malformed.csv` baseline is assistant-computed, not owner-published | A4 check = re-run both hashes after execution and compare; program opens inputs read-only |
| Does the sample exercise CSV edge cases? | Decides whether `csv` module handling is enough | Both sample files, 2026-09-08: `file` reports "CSV text"; first bytes are `invoice_id,statu…` (no BOM); `cat -ve` shows `$` line ends (LF), no quoting | Plain ASCII, LF, no embedded commas or quotes, uniform 4 columns | Gap: nothing local demonstrates quoted fields, CRLF, blank lines, or ragged rows | `csv.DictReader` with `newline=""`, `encoding="utf-8"` is sufficient and standard; ragged/missing-field rows covered by proposal P3, unverified |
| Are the tools A4 permits actually present? | "stdlib only, no installs" | `python3 -c "import csv,json,sys"` on this machine, 2026-09-08 | Python 3.12.10; imports succeed | Verified locally; other machines unverified (any CPython 3.8+ suffices for this spec) | No dependency step in the handoff |

## Alternatives, Alpha, and objections

- **Chosen — validate-all in memory, then aggregate, then write once.** Satisfies A3 by
  construction: the output path is not opened until every row has passed. Simplest design
  that carries the guarantee rather than relying on input luck.
- **Streaming: parse and write as rows arrive.** Rejected. Fails A3 — a bad row late in
  the file leaves a partial or replaced output. Simpler-looking, not dependable.
- **Two passes over the file (validate, then re-read and aggregate).** Same guarantee as
  the chosen design, more code and a second read, and it can disagree with itself if the
  file changes between passes. **Parked**, worth reopening only if inputs ever outgrow
  memory — the brief describes local operational files, and the sample is 148 bytes.
- **Third-party CSV/dataframe libraries.** Rejected: violates the brief's stdlib-only
  constraint and A4's no-install rule.
- **Validate-first but write directly to the output path (no temp file).** This is the
  genuinely strongest objection to the recommendation: it already passes the demonstrated
  failure case, and `tempfile` + `os.replace` is extra machinery. Assistant judgment: keep
  the atomic replace (P1). A3's second sentence — "No partial result may replace a previous
  successful report" — is about the output's state, and a direct write that dies mid-stream
  (full disk, interrupt) leaves exactly that partial result. `os.replace` is a few stdlib
  lines and closes the gap. It is an implementation choice under A3, not a new requirement,
  and it is listed as a proposal because it is not literally compelled by the sample case.
- **Alpha/Beta:** the design is ordinary practice (external Beta) — validate before write,
  atomic replace, `csv.DictReader`. The one non-obvious contribution is that Python's
  `int()` over-accepts underscores and non-ASCII digits, so a naive `try: int(...)` is a
  weaker validator than it appears. That is documented CPython behaviour, so also external
  Beta; whether it is new to the owner is unknown and not claimed.

## Meaningful changes and parked branches

- **Revised (assistant):** amount validation from `try: int(x)` to regex-then-`int()`,
  prompted by the local probe showing `int("1_0")==10`. Not yet owner-reviewed.
- **Sharpened (assistant):** validation must precede status filtering. Prompted by noticing
  that the only bad row in `sources/malformed.csv` is `cancelled`, which is what A3's
  "even if the invalid row is cancelled" clause exists to catch. Without this the sample
  would pass a filter-first program and silently replace a good report.
- **Parked:** two-pass streaming for very large inputs — reopen if an input stops fitting
  comfortably in memory.
- **Method note:** no roundtable or adversarial-review agent was used. The requirements are
  settled by the owner, the scope is one small local script, and the only consequential
  premise (validation order) was decided by direct file inspection rather than opinion.
  Reopen if the owner disputes P1 or the A3 reading. No external research was performed —
  the live request states all domain facts are supplied.

## Delivery or pause

`docs/invoice-summary/RESULT.md` exists and has been presented. Checked before delivery:
every A1–A4 clause maps to a stated observable outcome; the expected JSON was re-derived
from the raw file; `sources/input.sha256` was confirmed against `invoices.csv`.

Not done, by instruction: no program written, no execution workflow started, no source
file modified, nothing outside this workspace touched. The implementation is a **proposal
under review** — the owner has expressed no acceptance and no implementation authority has
been granted by this delivery.
