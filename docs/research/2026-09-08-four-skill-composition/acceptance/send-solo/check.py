import json, subprocess, sys
from pathlib import Path
before=Path("input.json").read_bytes()
subprocess.run([sys.executable,"report.py","input.json","report.json"],check=True)
assert json.loads(Path("report.json").read_text())=={"net":9,"ids":["001","001","002"]}
assert Path("input.json").read_bytes()==before
print("PASS: signed totals, original IDs and input preservation")
