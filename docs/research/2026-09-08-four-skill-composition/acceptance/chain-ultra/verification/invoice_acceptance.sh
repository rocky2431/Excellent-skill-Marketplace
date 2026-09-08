#!/usr/bin/env bash
# Observational acceptance check for the goal `invoice-summary-cli`.
#
# Drives the command line `sources/brief.md` specifies and checks outcomes only:
# it never inspects the program's internal design, never asserts a byte-level
# output format, and never demands a particular exit code beyond "nonzero" on the
# malformed fixture. An implementation that declines P1-P6 of
# docs/invoice-summary/RESULT.md can still pass.
#
# Reads sources/ without writing to it; writes only inside .work/.
# DRAFT: awaiting owner inspection. Never executed as of 2026-09-08.

set -u

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)" || exit 3
cd "$root" || exit 3

fail() { echo "FAIL: $*" >&2; exit 1; }
sha() { shasum -a 256 "$1" | awk '{print $1}'; }

# The baseline for malformed.csv has no owner-published hash; it is the working
# baseline recorded in docs/invoice-summary/RESULT.md.
VALID_SHA="$(tr -d '[:space:]' < sources/input.sha256)"
MALFORMED_SHA="690b34f4c8c5a7da5cbb535fa5dc7a5a7442be84d0ee8b8f97cfa5659a5efeb5"

[ -f invoice_summary.py ] || fail "invoice_summary.py does not exist: the outcome is unknown, not passing"

mkdir -p .work || exit 3
work="$(mktemp -d "$root/.work/invoice-acceptance.XXXXXX")" || exit 3
trap 'rm -rf "$work"' EXIT
out="$work/summary.json"

# A1/A2: the valid fixture produces the accepted result.
python3 invoice_summary.py sources/invoices.csv "$out" \
  || fail "A1: nonzero exit on sources/invoices.csv"
[ -f "$out" ] || fail "A1: no output file was written"

python3 - "$out" <<'PY' || fail "A1/A2: parsed output does not equal the accepted result"
import json, sys
expected = [
    {"currency": "EUR", "invoice_count": 1, "total_cents": 100, "invoice_ids": ["001"]},
    {"currency": "USD", "invoice_count": 3, "total_cents": 105, "invoice_ids": ["001", "002", "001"]},
]
try:
    got = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception as exc:
    print(f"output is not readable JSON: {exc}", file=sys.stderr)
    sys.exit(1)
if got != expected:
    print(f"expected {expected!r}\n     got {got!r}", file=sys.stderr)
    sys.exit(1)
PY

# A3: the malformed fixture, whose only invalid row is cancelled, must fail
# without replacing the good report that already sits at the output path.
before="$(sha "$out")"
if python3 invoice_summary.py sources/malformed.csv "$out"; then
  fail "A3: exit 0 on sources/malformed.csv, whose only invalid row is cancelled"
fi
[ "$(sha "$out")" = "$before" ] || fail "A3: the previous successful report was replaced"

# A4 (mechanical part): the inputs are byte-for-byte what they were.
[ "$(sha sources/invoices.csv)" = "$VALID_SHA" ] || fail "A4: sources/invoices.csv changed"
[ "$(sha sources/malformed.csv)" = "$MALFORMED_SHA" ] || fail "A4: sources/malformed.csv changed"

echo "PASS: A1, A2, A3 and the input-unchanged part of A4 observed on both fixtures"
echo "A4's no-install / no-global-config claim is assigned to the independent review, not to this check"
