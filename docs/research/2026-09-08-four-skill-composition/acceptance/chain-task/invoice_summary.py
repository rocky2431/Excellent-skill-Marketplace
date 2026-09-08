#!/usr/bin/env python3
"""Summarize finalized invoice rows per currency.

Usage: python3 invoice_summary.py INPUT.csv OUTPUT.json

Three strictly sequential phases: validate every row, then aggregate, then
write once. The output path is not opened for writing until the whole input
has been proven valid (A3).
"""

import csv
import json
import os
import re
import sys
import tempfile

FIELDS = ("invoice_id", "status", "currency", "amount_cents")
# int() alone accepts "1_0", " 5" and non-ASCII digits, so match the syntax first.
AMOUNT_RE = re.compile(r"[+-]?[0-9]+")


class ValidationError(Exception):
    pass


def read_and_validate(input_path):
    """Return every data row as (invoice_id, status, currency, amount) tuples."""
    rows = []
    with open(input_path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or [f.strip() for f in reader.fieldnames] != list(FIELDS):
            raise ValidationError(
                "%s: header must be %s, got %s"
                % (input_path, ",".join(FIELDS), reader.fieldnames)
            )
        for line_no, row in enumerate(reader, start=2):
            if row.get(None) is not None:
                raise ValidationError("%s row %d: too many columns" % (input_path, line_no))
            values = []
            for field in FIELDS:
                value = row.get(field)
                if value is None or value == "":
                    raise ValidationError(
                        "%s row %d: missing %s" % (input_path, line_no, field)
                    )
                values.append(value)
            invoice_id, status, currency, amount_cents = values
            if not AMOUNT_RE.fullmatch(amount_cents):
                raise ValidationError(
                    "%s row %d: amount_cents is not an integer: %r"
                    % (input_path, line_no, amount_cents)
                )
            rows.append((invoice_id, status, currency, int(amount_cents)))
    return rows


def aggregate(rows):
    """Group finalized rows per currency, preserving input order of the ids."""
    by_currency = {}
    for invoice_id, status, currency, amount in rows:
        if status != "finalized":
            continue
        entry = by_currency.setdefault(
            currency,
            {"currency": currency, "invoice_count": 0, "total_cents": 0, "invoice_ids": []},
        )
        entry["invoice_count"] += 1
        entry["total_cents"] += amount
        entry["invoice_ids"].append(invoice_id)
    return [by_currency[code] for code in sorted(by_currency)]


def write_once(summary, output_path):
    """Write the summary atomically so no partial file can replace a good one."""
    directory = os.path.dirname(os.path.abspath(output_path))
    handle = tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=directory, prefix=".invoice_summary-", delete=False
    )
    try:
        with handle:
            json.dump(summary, handle, indent=2)
            handle.write("\n")
        os.replace(handle.name, output_path)
    except BaseException:
        if os.path.exists(handle.name):
            os.unlink(handle.name)
        raise


def main(argv):
    if len(argv) != 3:
        sys.stderr.write("usage: python3 invoice_summary.py INPUT.csv OUTPUT.json\n")
        return 2
    input_path, output_path = argv[1], argv[2]
    try:
        rows = read_and_validate(input_path)
    except (ValidationError, OSError, UnicodeDecodeError, csv.Error) as exc:
        sys.stderr.write("%s\n" % exc)
        return 2
    try:
        write_once(aggregate(rows), output_path)
    except OSError as exc:
        sys.stderr.write("%s: cannot write output: %s\n" % (output_path, exc))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
