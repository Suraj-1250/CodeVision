# CodeVision

CodeVision is a small, Python-first code execution visualizer. Write a snippet, run it, and inspect the traced line, local variables, and printed output one step at a time.

## Run locally

Requires Python 3.10 or newer.

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000. Use the arrows to move through the trace, Play to animate it, and the example menu to load another snippet. Ctrl+Enter (Cmd+Enter on Mac) runs the code.

## What is included

- Flask API with Python line tracing (`sys.settrace`)
- Browser editor with line numbers, starter examples, and current-line highlighting
- Previous/next/play controls, local variable snapshots, and captured standard output
- Syntax error and runtime error display
- Responsive dark interface

## Scope and safety

This is a local learning prototype. The trace endpoint executes submitted Python inside the Flask process; it is **not a sandbox** and must not be exposed to the public internet or used with untrusted code. Before deployment, move execution into a separately isolated worker/container with CPU, memory, time, filesystem, and network limits. The current trace cap limits recorded states, not execution time.

## Next steps

Add an isolated execution worker, call-stack visualization, tests for loops/functions/errors, and then array/search/sort visualizations. This prototype currently supports Python snippets only.
