from pathlib import Path
with Path("effects.jsonl").open("a") as f:
 f.write('{"request_id":"invoice-export-17","artifact":"export.json","status":"created"}\n')
