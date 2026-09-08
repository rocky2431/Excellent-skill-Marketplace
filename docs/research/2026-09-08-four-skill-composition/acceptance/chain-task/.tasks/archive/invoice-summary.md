# Invoice summary execution

## Current understanding

Execute A1-A4 from sources/brief.md. The prior research handoff is docs/invoice-summary/RESULT.md, with the reasoning trail in THOUGHTS.md. Read them completely. The current receiving workspace is this record's parent's parent; the absolute path in RESULT refers to the originating workspace and must not redirect writes. The research itself did not authorize implementation; this disposable acceptance mission now explicitly authorizes local implementation and verification of A1-A4. P1-P6 are proposals, not extra owner requirements. Routine implementation choices are delegated to the worker. No publication, external writes, installation or global config changes.

Status: delivered and verified 2026-09-08. `invoice_summary.py` exists in this workspace and A1-A4 each pass on observed runs (evidence below). Nothing is left in progress.

## Steps

1. done — Original research produced the handoff.
2. done — Implemented `invoice_summary.py` (validate every row -> aggregate finalized rows -> write once) and independently checked A1-A4 against the supplied fixtures. All four pass on observed output.
3. done — Actual evidence recorded below; this note is archived to `.tasks/archive/invoice-summary.md`.

## Judgments and corrections

An earlier suggestion to deduplicate IDs was rejected: repeated IDs are distinct rows. Leading zeros must survive. Refunds reduce totals. A malformed cancelled row still fails validation before output replacement. Preserve A1-A4 ID and requirement meanings; test cases are evidence, not new requirements.

Correction to the upstream handoff (do not rewrite RESULT.md/THOUGHTS.md): both documents place the bad row of `sources/malformed.csv` at "line 8". The file has 7 lines; `grep -n 'not-an-integer' sources/malformed.csv` -> `7:100,cancelled,EUR,not-an-integer`. The substantive point is unaffected — the only invalid row is `cancelled`, so validation must precede the status filter — and the program reports "row 7".

P1-P6 stay implementation proposals; no owner acceptance is recorded. `sources/brief.md` states "The later implementation may choose its internal design", so the following were taken as internal design choices, not as accepted requirements, and each can be changed without touching the A1-A4 evidence: temp file + `os.replace` (P1 shape, closes A3's "no partial result may replace a previous successful report" for an interrupted write), `re.fullmatch(r"[+-]?[0-9]+", ...)` before `int()` (P2 shape; `int()` accepts `1_0`, ` 5` and non-ASCII digits), header/missing-field/extra-column rejection in phase 1 (P3 shape), exit 2 + one-line stderr message naming path, 1-based row and offending value (P4 shape), `indent=2` UTF-8 with trailing newline and A1 key order (P5 shape), non-finalized statuses excluded but not an error (P6 shape). A missing output directory also exits 2 with a message instead of a traceback; that is beyond P1-P6 and equally revisable.

## Evidence and artifacts

Sources (unmodified, read-only): `sources/brief.md`, `sources/invoices.csv`, `sources/malformed.csv`, `sources/input.sha256`. Upstream handoff kept byte-identical: `docs/invoice-summary/RESULT.md`, `docs/invoice-summary/THOUGHTS.md`. Delivered code: `invoice_summary.py` (stdlib only: csv, json, os, re, sys, tempfile). Test output: `out/summary.json`. Workspace root: `/private/var/folders/cm/zpwxmr512rq1qz4_0_ryz8t80000gn/T/four-skill-acceptance-g3wlbf6c/chain-task` (not a git repository; the absolute root in RESULT.md points at the originating workspace and was not used). Python 3.12.10; no install, no global config change, no publication or external write.

Checks actually run, in this order, working directory = workspace root:

- A1/A2 — `python3 invoice_summary.py sources/invoices.csv out/summary.json` -> exit 0. Output parses to exactly `[{"currency":"EUR","invoice_count":1,"total_cents":100,"invoice_ids":["001"]},{"currency":"USD","invoice_count":3,"total_cents":105,"invoice_ids":["001","002","001"]}]`, matching the fixture derived by hand in RESULT.md. EUR before USD; USD 105 shows the `-20` refund subtracted and the cancelled `099/USD/700` absent from both total and id list; ids are JSON strings with leading zeros, repeats and input order preserved; key order is `currency, invoice_count, total_cents, invoice_ids`. Asserted structurally by an inline `python3 -` check (equality with the fixture, sorted currencies, all ids `str`, `invoice_count == len(invoice_ids)`), which printed "parsed structure equals derived fixture; ids are strings; currencies sorted" and exited 0.
- Good-output baseline — `shasum -a 256 out/summary.json` -> `e457fb5cae39f41ff8d926eafbdde288563268e0aad56688c11d48053fad479c`.
- A3 — `python3 invoice_summary.py sources/malformed.csv out/summary.json` (same output path) -> exit 2, stderr `sources/malformed.csv row 7: amount_cents is not an integer: 'not-an-integer'`, and `shasum -a 256 out/summary.json` still `e457fb5c…479c`, byte-for-byte unchanged. `ls -a out/` shows only `summary.json`: no temp file left behind. Extra check: the same malformed run against a not-yet-existing path `out/never.json` exits 2 and creates no file, so the output path is never opened before validation succeeds.
- A4 — after all runs, `shasum -a 256 sources/invoices.csv sources/malformed.csv` -> `fed9dd1d20771e2fd2cb26000c82369148ae435c282428957caa21b35b16b830` (equals `sources/input.sha256`) and `690b34f4c8c5a7da5cbb535fa5dc7a5a7442be84d0ee8b8f97cfa5659a5efeb5` (equals the assistant-computed baseline in RESULT.md). `grep -n '^import\|^from' invoice_summary.py` shows stdlib imports only; `python3 -c "import csv,json,os,re,sys,tempfile"` succeeds with no install step.

Limits, unchanged from the handoff: whole-file in-memory processing (fine for these local files; the parked two-pass variant is for inputs that outgrow memory); quoted fields, embedded commas, CRLF, BOM and blank lines are still unexercised by any local fixture — the header/column checks are the only coverage there; string sort of currency codes coincides with alphabetical order for uppercase ASCII only; A1-A4 remain owner premises, not independently verified against any operational process.

## Next action

None. A1-A4 are implemented and verified on the supplied fixtures. If work resumes: P1-P6 still await the owner's decision, and the CSV shapes listed under Limits have no local fixture.
