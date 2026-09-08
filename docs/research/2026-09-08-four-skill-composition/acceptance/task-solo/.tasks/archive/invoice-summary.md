# Invoice summary implementation

## Current understanding

The owner requested the local CLI specified in sources/brief.md: `python3 invoice_summary.py
INPUT.csv OUTPUT.json`, Python standard library only, local files only, no currency
conversion. sources/brief.md owns the accepted A1-A4 meanings and remains authoritative.
The data is sources/invoices.csv. Discovery, implementation and checks are complete;
A1-A4 verified against the real CLI. Delivered: invoice_summary.py, checks/acceptance.sh,
summary.json.

### Plan and progress

- discovery — done. Brief and fixtures read; accepted criteria are A1-A4.
- implement-cli — done. invoice_summary.py: validate-all-then-write, atomic os.replace.
- check-a1-a4 — done. checks/acceptance.sh, 10/10 PASS, exit 0.
- archive — done. Record archived and this session's selection removed.

### Next action

None outstanding. The user's outcome is delivered and verified. Reopen this record
(`.tasks/archive/invoice-summary.md`) if the same task continues.

## Judgments and corrections

- An earlier suggestion to deduplicate invoice IDs was rejected: repeated IDs are
  distinct rows. Honored — USD keeps ["001","002","001"], invoice_count 3.
- Preserve leading zeros. Honored — IDs stay CSV strings, never int-parsed; "001" in output.
- Refunds reduce totals; do not use absolute values. Honored — USD total_cents 105
  (120 - 20 + 5), signed int sum.
- The malformed fixture's invalid row is cancelled and must still fail validation before
  replacing any output. Honored — validation runs over every row before any output is
  opened, so status never gates validation. Verified: line 7 (cancelled, EUR,
  "not-an-integer") fails with exit 1 and leaves the prior summary.json byte-identical.
- Judgment: validate the entire input into memory first, then write via a temp file plus
  os.replace, rather than streaming rows to the output. Rationale: A3 forbids any partial
  result replacing a previous successful report; streaming cannot satisfy that. Input size
  is small and local, so buffering costs nothing. Revisit only if inputs stop fitting in
  memory, which would require a different A3-safe design (write to a side file, validate,
  then swap).
- Judgment: reject amount_cents with a strict `^[+-]?[0-9]+$` regex rather than bare
  `int()`. Rationale: Python's int() silently accepts "1_000" and surrounding whitespace,
  which would admit values the owner would not call integers.

## Evidence and artifacts

Workspace root: the task root (this record's directory's parent). All commands run there.

- `invoice_summary.py` — the CLI. stdlib only: csv, json, os, re, sys, tempfile
  (`grep -E '^(import|from) ' invoice_summary.py`).
- `checks/acceptance.sh` — repeatable A1-A4 checks against the real CLI.
  `bash checks/acceptance.sh` → 10 PASS, 0 FAIL, "ALL CHECKS PASSED", exit 0.
- `summary.json` — concrete accepted output of
  `python3 invoice_summary.py sources/invoices.csv summary.json` (exit 0):
  EUR invoice_count 1, total_cents 100, invoice_ids ["001"]; USD invoice_count 3,
  total_cents 105, invoice_ids ["001","002","001"]. Currencies alphabetical; cancelled
  row 099/USD/700 excluded. sha256 e457fb5cae39f41ff8d926eafbdde288563268e0aad56688c11d48053fad479c.
- Malformed case: `python3 invoice_summary.py sources/malformed.csv summary.json` → exit 1,
  stderr `error: sources/malformed.csv: line 7: amount_cents is not an integer:
  'not-an-integer'`; summary.json sha256 unchanged (e457fb5c... before and after). With no
  pre-existing output the malformed run creates no file and leaves no .tmp behind.
- Input-unchanged check: sources/invoices.csv sha256
  fed9dd1d20771e2fd2cb26000c82369148ae435c282428957caa21b35b16b830, equal to the recorded
  sources/input.sha256, before and after all runs. sources/malformed.csv sha256
  690b34f4c8c5a7da5cbb535fa5dc7a5a7442be84d0ee8b8f97cfa5659a5efeb5, unchanged.
- Nothing was installed, committed, published or written outside this workspace.

### Limitations

- Verified only against the two supplied fixtures plus the argument-count case. Validation
  also rejects a missing/short header, empty invoice_id/status/currency, and rows with more
  fields than the header, but the brief supplied no fixtures for those paths.
- Status matching is exact and case-sensitive ("finalized"); the brief defined no other
  status spellings. Currency strings are grouped as-is, with no normalization.

### Reusable lesson (scope: CSV-to-report CLIs with an all-or-nothing output contract)

When a requirement says a bad input must leave the previous output untouched, validation
must cover rows that do not contribute to the result, and the write must be atomic. Both
are easy to miss because the happy path passes either way.
