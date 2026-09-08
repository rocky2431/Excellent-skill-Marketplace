# Invoice summary request

Operations needs a local command that reads a CSV and writes a JSON summary grouped by currency.
Use Python standard library only. It runs on local files; no databases, cloud services or currency conversion.
The command line is: python3 invoice_summary.py INPUT.csv OUTPUT.json.

## Accepted requirements

- A1: Include only finalized rows in totals. Sum signed integer amount_cents separately per currency; refunds are negative and reduce the total. Output is a JSON list, currencies sorted alphabetically; each object has currency, invoice_count, total_cents, invoice_ids.
- A2: Retain the original invoice_id strings, including leading zeros and repeated IDs, in input order within each currency. Repeated IDs are distinct rows, not duplicates to discard.
- A3: Validate every input row before replacing the output. A noninteger amount_cents fails with nonzero exit and leaves an existing output byte-for-byte unchanged, even if the invalid row is cancelled. No partial result may replace a previous successful report.
- A4: Input bytes remain unchanged. Do not install dependencies or change global configuration. Local code, tests and output in this workspace are authorized; publication and external writes are outside this example task.

All four criteria are owner requirements. There is no unresolved business decision. The later implementation may choose its internal design. Evidence must include the concrete output, a malformed input case, and an input-unchanged check.
