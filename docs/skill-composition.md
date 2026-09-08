# Independent skills and optional handoffs

Deep Thinking, Task State with Files, Agent Delegation and UltraGoal each retain an
independent entry point. Install only the capabilities needed for the task. A host
still supplies its model, tools, permissions and continuation; a Skill package does
not supply another host's runtime or make an unavailable worker usable.

| Skill | Complete standalone responsibility | Optional reuse |
|---|---|---|
| Deep Thinking | Clarify and research a question, then deliver a supported result | An ordinary agent or another Skill can read an actionable result |
| Task State | Preserve understanding, decisions, evidence and next action; restore the selected task | Read an existing business note or goal Carry-over instead of creating another record |
| Agent Delegation | Submit a mission to an available agent, retain its ID and collect its actual result | Carry a result, selected task record or goal terms to the worker |
| UltraGoal | Prepare and carry a complete goal, coordinate available workers, and check completion evidence | Reuse existing research, state or delegation tools without requiring their Skills |

UltraGoal's own clarification, necessary research, Carry-over, coordination and
verification remain available without the other three. Its `design-critic`, `review`
and `critic` roles serve specification review, result review and review critique;
each has a bounded responsibility, not a copy of the three companion Skills.

## Pass artifacts, not a mandatory workflow

A useful handoff names the outcome and exclusions, accepted requirements and their
evidence conditions, key corrections, open decisions, existing authority, accessible
source paths, actual workspace/revision and one next action. Preserve acceptance IDs
and meanings. Test cases belong with the evidence they supply; recommendations do not
silently become owner requirements. Receiving a result is not authorization to execute.

Use ordinary prose and existing files. No shared database, imported SDK, global active
pointer, mandatory handoff file or common execution engine is required. Typical paths:

- Deep Thinking result → Task note → a fresh agent reads it and completes the next step.
- Deep Thinking result → UltraGoal reads settled terms and adds missing goal conditions.
- A failed task → Agent Delegation returns a receipt and artifacts → the task owner
  verifies the result and updates the same record.
- Execution reveals a new research question → return to Deep Thinking within the
  current authority, retaining existing goal terms and execution state.

## Select recovery explicitly

From Task State 0.4.0, files merely existing do not activate hooks. Select a task in
the host's launch environment (`TASK_STATE_TASK` or `TASK_STATE_FILE`, optionally
`TASK_STATE_ROOT`), or bind an existing record to its actual native session:

```bash
python3 "<task-skill-dir>/scripts/task_state.py" activate \
  --task export-ready --session <native-session-id> --root <project-root>
python3 "<task-skill-dir>/scripts/task_state.py" read \
  --task export-ready --root <project-root>
python3 "<task-skill-dir>/scripts/task_state.py" deactivate \
  --session <native-session-id> --root <project-root>
```

Use `--file` for an existing note. The local `.tasks/.sessions/` selections are ignored
by Git and are separate for each native session. A new session must select its task.
`init`, `read` and the legacy `bind` do not activate hooks. Manual `read`/`resolve`
retain legacy and single-record discovery; invalid explicit choices never fall back.
If a host cannot expose its session ID, use launch selectors or manual full reading.
Changing a child shell's environment does not change its already-running parent host.

UltraGoal retains its existing goal/session ownership. Unselected or unrelated
sessions must not consume another task's state. A silent hook may still have a process
startup cost; it does not execute business work or schedule another turn.

## Keep one current execution record

Research history belongs in the inquiry draft; accepted goal terms belong in the goal
contract when UltraGoal is used. Choose one record and writer for current execution
understanding and next action. If a Task note owns it, UltraGoal Carry-over keeps the
locator and essential run facts and directs recovery to read the note. If Carry-over
owns it, do not create a parallel Task ledger. Workers return evidence to that writer.

Use an explicitly requested path, then existing task documents, then the repository's
business-document convention (`docs/` or `documents/`). New projects without one may
use `documents/<work-id>/`. Existing `thinking/` inquiries, `.tasks/`, `.goals/` and
private runtime receipts stay at their valid paths. Only create files that this task
needs; links and IDs cannot transfer uncommitted files to another workspace.

## Interpret delegation results at the consumer

Retain `delegation_id`, the terminal receipt and output references in the existing
record. A wait timeout ends one observation: keep watching the same ID. If execution
is unknown, inspect native state and actual effects before retrying. A normal model
turn (`success`) and a business check passing are separate facts.

UltraGoal's command hook observes recognized direct `agent-delegate run` calls only.
The asynchronous `submit`/`wait`/`status` path and shell wrappers require the caller to
read terminal receipts. Missing hook events do not prove success. Required independent
review still needs its own current evidence; a transport receipt cannot replace it.

## Validate behavior and the distributed version

Verify one real task using each package's standalone path before testing handoffs.
Then check that the receiving agent preserves requirement meanings and corrections,
finds the evidence, and completes an actual step. A readable file, matching ID set,
green package check or normally ended model turn is insufficient on its own.

The upstream repositories contain runtime regressions. Marketplace tests execute
the shipped Task hook and selection CLI from the pinned ZIP. Native-host exercises
and their observed limits belong with release acceptance evidence; a script packet
test is not proof of every host's compaction or unattended lifecycle.

Update source repositories first, then selected pins and generated catalogs/packages.
Keep full source SHAs, matching versions and reproducible artifacts. Updating this
marketplace does not automatically update the user's installed plugin copies.
