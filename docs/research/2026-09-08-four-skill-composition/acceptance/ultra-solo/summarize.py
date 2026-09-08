"""Summarize a JSON array of {"id", "value"} rows.

Writes {"sum": <signed total>, "ids": [<ids in original order>]} to OUTPUT.
IDs are ordered row identities: order is preserved and repeats are kept.
The input file is only read, never written.
"""
import json
import sys


def summarize(rows):
    return {
        "sum": sum(row["value"] for row in rows),
        "ids": [row["id"] for row in rows],
    }


def main(argv):
    if len(argv) != 3:
        print("usage: summarize.py INPUT.json OUTPUT.json", file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as handle:
        rows = json.load(handle)
    with open(argv[2], "w", encoding="utf-8") as handle:
        json.dump(summarize(rows), handle)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
