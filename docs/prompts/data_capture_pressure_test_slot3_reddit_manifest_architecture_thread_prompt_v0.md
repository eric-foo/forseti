# Slot 3 Reddit Manifest Architecture Thread Prompt v0

Use this prompt to start a new Codex thread for framing the Reddit B1 manifest architecture and selection strategy.

```text
We are in C:\Users\vmon7\Desktop\projects\orca.

Follow Orca project instructions. Before project work, read:
- AGENTS.md
- .agents/workflow-overlay/README.md
- any overlay source-loading instructions required by the README

Context:
- This is ORCA Data Capture Spine pressure-test Slot 3 B1.
- The operator can manually access Reddit thread JSON that agents/browser tools could not reliably access.
- Raw Reddit captures are being saved under:
  docs\_inbox\data_capture_pressure_test_operator_supplied_2026_05_29\slot3_reddit_b1\raw\thread_json
- Mechanical source-projected outputs are intended under:
  docs\_inbox\data_capture_pressure_test_operator_supplied_2026_05_29\slot3_reddit_b1\cleansed\threads
- The mechanical source-projection prompt is:
  docs\prompts\data_capture_pressure_test_reddit_mechanical_source_projection_worker_prompt_v0.md
- The folder segment `cleansed` is legacy naming for this batch; treat the contents as source-projected files, not Cleaning Spine outputs.

Current architectural question:
How should we design the thread-selection manifest so the capture workflow knows why each Reddit thread matters without contaminating mechanical source projection or letting an agent silently select only content it considers important?

Important boundary:
- Do not make the source-projection worker decide relevance.
- Do not summarize, classify obligations, judge thread content, or remove evidence rows as part of source projection.
- Preserve raw thread JSON untouched.
- Use the manifest to record selection rationale and expected signal.
- Use later signal-indexing, if needed, to point to rows in source-projected outputs by row/comment id.

Known raw-file caveat to verify before any processing:
- Some operator-saved files may be `.md`, empty, or non-JSON because of Windows/editor save behavior.
- First inspect file names, byte sizes, extensions, and whether payloads are valid Reddit JSON.
- If files are invalid or zero-byte, report a visible blocker and give exact operator correction steps.

Task:
1. Frame the manifest architecture for this Slot 3 Reddit B1 lane.
2. Define the minimal manifest schema.
3. Define how a manifest row should be filled for each thread.
4. Define how raw-file validity should be checked before a row is considered usable.
5. Explain how the manifest connects to raw JSON, source-projected JSONL, readable markdown, and any later signal index.
6. Do not run broad implementation, package installation, web browsing, or content analysis unless explicitly authorized in the new thread.

Desired output:
- A concise architecture recommendation.
- A CSV header or table schema.
- One example row using a known thread if available.
- A correction protocol for invalid raw files.
- A clear next action for the operator.
```
