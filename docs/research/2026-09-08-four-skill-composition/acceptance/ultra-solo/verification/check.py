import json, subprocess, sys, tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
before=(root/"input.json").read_bytes()
with tempfile.TemporaryDirectory() as tmp:
 output=Path(tmp)/"result.json"
 subprocess.run([sys.executable,str(root/"summarize.py"),str(root/"input.json"),str(output)],check=True)
 assert json.loads(output.read_text())=={"sum":5,"ids":["a","b","a"]}
 assert (root/"input.json").read_bytes()==before
print("PASS: actual CLI result, signed sum, input order and duplicate IDs; input unchanged")
