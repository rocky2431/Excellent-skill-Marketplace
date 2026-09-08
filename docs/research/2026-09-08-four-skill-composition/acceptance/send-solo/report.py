import json, sys
from pathlib import Path
rows=json.loads(Path(sys.argv[1]).read_text())
Path(sys.argv[2]).write_text(json.dumps({"net":sum(r["delta"] for r in rows),"ids":[r["id"] for r in rows]})+"\n")
