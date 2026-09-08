"""Recheck saved business artifacts; does not replay or simulate native sessions."""
import hashlib
import json
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "deep-final/sources"
EXPECTED = [
    {"currency": "EUR", "invoice_count": 1, "total_cents": 100, "invoice_ids": ["001"]},
    {"currency": "USD", "invoice_count": 3, "total_cents": 105, "invoice_ids": ["001", "002", "001"]},
]


def check_invoice(name):
    before = {p.name: p.read_bytes() for p in SOURCES.iterdir() if p.is_file()}
    with tempfile.TemporaryDirectory() as temp:
        output = Path(temp) / "result.json"
        command = [sys.executable, str(ROOT / name / "invoice_summary.py")]
        subprocess.run(command + [str(SOURCES / "invoices.csv"), str(output)], check=True)
        assert json.loads(output.read_text()) == EXPECTED, name
        good = output.read_bytes()
        failed = subprocess.run(command + [str(SOURCES / "malformed.csv"), str(output)], capture_output=True)
        assert failed.returncode != 0, name
        assert output.read_bytes() == good, name
    assert all((SOURCES / name).read_bytes() == value for name, value in before.items())
    print(f"PASS: {name} A1-A4 real CLI and failure preservation")


def main():
    assert hashlib.sha256((SOURCES / "invoices.csv").read_bytes()).hexdigest() == (SOURCES / "input.sha256").read_text().strip()
    check_invoice("task-solo")
    check_invoice("chain-task")
    subprocess.run([sys.executable, "verification/check.py"], cwd=ROOT / "ultra-solo", check=True)
    with tempfile.TemporaryDirectory() as temp:
        shutil.copytree(ROOT / "send-solo", Path(temp) / "send")
        subprocess.run([sys.executable, "check.py"], cwd=Path(temp) / "send", check=True)
    print("PASS: saved business evidence; native host coverage is reported separately")


if __name__ == "__main__":
    main()
