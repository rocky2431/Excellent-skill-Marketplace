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

Keep the explicitly selected record, then reuse a fitting existing document or section,
then use the invoked Skill's standalone default. Arming UltraGoal does not transfer
ownership. Match task identity and scope, not recency or installed Skills.
Deep Thinking preserves working reasoning and an independently understandable
result; its standalone defaults remain `THOUGHTS.md` and `RESULT.md`, while bounded
embedded inquiries can reuse existing sections. Task State preserves borrowed headings,
edits only mutable state and follows that document's lifecycle, without moving a goal
into `.tasks/archive/`. Goals retain their paired decisions and frozen clauses.

| Selected capabilities | Current content and necessary artifacts |
|---|---|
| Deep Thinking | Inquiry state and reasoning; an independently understandable result |
| Task State | One existing record or the standalone `.tasks/<id>.md` |
| UltraGoal | Confirmed goal, paired decisions, Carry-over and actual acceptance evidence |
| Deep Thinking + Task State | Maintain the inquiry record in place; retain the needed result |
| Deep Thinking + UltraGoal | Research informs terms; selected record or Carry-over owns main task state |
| Task State + UltraGoal | Maintain Carry-over, or retain an existing note referenced by Carry-over |
| All three | Reuse the same direction, plan, goal and state; add research only for a distinct purpose |

This describes content ownership, not fixed file counts. A research branch can track
its own question and evidence; the main record retains its relevance, handoff and
integrated result without copying its entire ledger. An independently delivered or
versioned report remains separately readable. Each installed package carries its own
minimum reuse rules; this Marketplace document is not a runtime dependency.

## Connect direction, milestones and current work

Preserve owner intent above the adopted approach, and the approach above current state.
These are scope relationships, not one Skill per time horizon or a new file hierarchy.

| Information | Existing source to reuse | Read or revise when |
|---|---|---|
| Long-term direction and boundaries | Adopted project intent; optionally `NORTH_STAR.md` when actually needed | Planning, material owner steering or a new phase |
| Medium-term outcomes and approach | Adopted result/plan or roadmap, with milestone exit conditions | Milestone transition or changed approach assumptions |
| Current milestone's goal | Existing task terms; confirmed `.goal.md` when using UltraGoal | Execution, recovery, review; frozen changes use explicit Modify |
| Current understanding and progress | One chosen record and writer | Evidence changes, work advances, recovery or handoff |

An adopted `RESULT.md` can itself be the plan. Do not copy it into a second plan or
invent absent project layers for a simple task. Cite applicable upstream sources by
path/section and date or revision in the existing record; no relationship registry is
needed. File location does not grant authority or automatic host loading.

A milestone may be one goal or contain several independently accepted outcomes;
ordinary steps do not each require a goal. Lower-level goals explain their contribution,
and the parent links acceptance evidence rather than daily task lists. A completed step
does not prove milestone completion or long-term value. Frozen goal clauses retain
their confirmed meaning locally, with source references as supplements, never mutable
links in place of Intent, Boundary or Acceptance.

New evidence revises supported judgments and authorized means. Explicit owner revisions
to direction, scope or success criteria trigger review of affected milestones and goals
through their existing change process. Preserve unaffected work and evidence whose
conditions still hold. Candidate recommendations do not silently become requirements.

## Separate state ownership from recovery

Choose one recovery provider for each selected task using existing bindings. If UltraGoal
restores its contract and an external state locator, the agent reads that state in full;
Task State can maintain it without also activating its hook. Deactivate only that session's
Task State selection when switching, or change its host launch selector when applicable.
Other tasks and sessions retain their selections. There is no shared runtime, registry
or automatic cross-plugin arbitration.

External Carry-over keeps an accessible state path, necessary run facts and an explicit
Next instruction to read, reconcile and then act on that record. Any last-observed action
summary names its source and time/revision; it is derived context, not a competing list.
References must terminate in real content. Keep original observations, confirmation and
independent review evidence separately identifiable; summaries do not replace receipts.

Large Task State previews prioritize Current understanding, Current position and Carry-over
when whole sections fit. A partial preview still requires reading the complete record;
an oversized section is not silently treated as absent work. Host behavior needs direct
verification, beyond merely inspecting the generated recovery text.

## Interpret delegation results at the consumer

Retain `delegation_id`, the terminal receipt and output references in the existing
record. A wait timeout ends one observation: keep watching the same ID. If execution
is unknown, inspect native state and actual effects before retrying. A normal model
turn (`success`) and a business check passing are separate facts.

UltraGoal's command hook observes recognized direct `agent-delegate run` calls and
the bundled `python3 "/absolute/skill/scripts/agent_delegate.py" run` form. Resolve
the script from the caller host's loaded Agent Delegation Skill, not another host's
cache or an independently installed global implementation.
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
