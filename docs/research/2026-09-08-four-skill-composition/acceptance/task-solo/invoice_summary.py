#!/usr/bin/env python3
"""Summarize finalized invoice rows by currency.

Usage: python3 invoice_summary.py INPUT.csv OUTPUT.json

Reads a CSV of invoice rows and writes a JSON list of per-currency summaries,
sorted alphabetically by currency. Only finalized rows contribute to totals,
but every input row is validated before any output is written, so a malformed
file never replaces a previously written report.
"""

import csv
import json
import os
import re
import sys
import tempfile

REQUIRED_COLUMNS = ("invoice_id", "status", "currency", "amount_cents")
FINALIZED = "finalized"

# Strict signed integer: no decimals, no underscores, no surrounding whitespace.
INTEGER_RE = re.compile(r"^[+-]?[0-9]+$")


class ValidationError(Exception):
    """An input row or header that cannot be accepted."""


def parse_rows(path):
    """Return the validated rows of `path` as a list of dicts.

    Raises ValidationError on a bad header or any bad row, including rows that
    would not contribute to the summary (for example cancelled ones).
    """
    with open(path, "r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValidationError("input has no header row")
        missing = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
        if missing:
            raise ValidationError("header is missing column(s): %s" % ", ".join(missing))

        rows = []
        for row in reader:
            # csv line numbers count the header, matching what a user sees in an editor.
            line = reader.line_num
            values = {}
            for column in REQUIRED_COLUMNS:
                value = row.get(column)
                if value is None:
                    raise ValidationError("line %d: missing value for %s" % (line, column))
                values[column] = value

            extra = row.get(None)
            if extra:
                raise ValidationError("line %d: more fields than the header declares" % line)

            for column in ("invoice_id", "status", "currency"):
                if values[column] == "":
                    raise ValidationError("line %d: %s is empty" % (line, column))

            amount = values["amount_cents"]
            if not INTEGER_RE.match(amount):
                raise ValidationError(
                    "line %d: amount_cents is not an integer: %r" % (line, amount)
                )
            values["amount_cents"] = int(amount)
            rows.append(values)
    return rows


def summarize(rows):
    """Group finalized rows by currency, preserving invoice_id strings and input order."""
    by_currency = {}
    for row in rows:
        if row["status"] != FINALIZED:
            continue
        entry = by_currency.setdefault(
            row["currency"],
            {
                "currency": row["currency"],
                "invoice_count": 0,
                "total_cents": 0,
                "invoice_ids": [],
            },
        )
        # Repeated invoice_ids are distinct rows; each one counts and is kept.
        entry["invoice_count"] += 1
        entry["total_cents"] += row["amount_cents"]
        entry["invoice_ids"].append(row["invoice_id"])
    return [by_currency[currency] for currency in sorted(by_currency)]


def write_json(summary, path):
    """Write `summary` to `path` atomically, so a partial file never lands there."""
    directory = os.path.dirname(os.path.abspath(path))
    handle = tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", suffix=".tmp", dir=directory, delete=False
    )
    try:
        with handle:
            json.dump(summary, handle, indent=2)
            handle.write("\n")
        os.replace(handle.name, path)
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
        rows = parse_rows(input_path)
    except ValidationError as error:
        sys.stderr.write("error: %s: %s\n" % (input_path, error))
        return 1
    except OSError as error:
        sys.stderr.write("error: cannot read %s: %s\n" % (input_path, error))
        return 1

    # Only reached once the whole input validated, so the previous output stands
    # untouched on any failure above.
    try:
        write_json(summarize(rows), output_path)
    except OSError as error:
        sys.stderr.write("error: cannot write %s: %s\n" % (output_path, error))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
