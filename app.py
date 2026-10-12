"""Local CodeVision demo: trace a Python snippet one line at a time."""
from __future__ import annotations

import contextlib
import io
import json
import sys
import traceback
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="static")
MAX_SOURCE = 8_000
MAX_STEPS = 250


def trace_source(source: str) -> dict:
    """Execute a short snippet and capture local/global values at each line."""
    steps: list[dict] = []
    output = io.StringIO()
    filename = "<codevision>"
    code = compile(source, filename, "exec")
    namespace = {"__name__": "__main__"}
    previous = sys.gettrace()

    def tracer(frame, event, arg):
        if frame.f_code.co_filename != filename:
            return tracer
        if event == "line" and len(steps) < MAX_STEPS:
            values = {k: repr(v)[:300] for k, v in frame.f_locals.items() if not k.startswith("__")}
            steps.append({"line": frame.f_lineno, "locals": values, "event": "line"})
        elif event == "return" and len(steps) < MAX_STEPS:
            values = {k: repr(v)[:300] for k, v in frame.f_locals.items() if not k.startswith("__")}
            steps.append({"line": frame.f_lineno, "locals": values, "event": "return", "value": repr(arg)[:300]})
        return tracer

    error = None
    try:
        with contextlib.redirect_stdout(output):
            sys.settrace(tracer)
            exec(code, namespace)
    except Exception as exc:  # surfaced in the UI as an execution error
        error = f"{type(exc).__name__}: {exc}"
    finally:
        sys.settrace(previous)
    return {"steps": steps[:MAX_STEPS], "stdout": output.getvalue(), "error": error}


@app.get("/")
def index():
    return send_from_directory("static", "index.html")


@app.post("/api/trace")
def trace():
    payload = request.get_json(silent=True) or {}
    source = payload.get("code", "")
    if not isinstance(source, str) or not source.strip():
        return jsonify(error="Add some Python code first."), 400
    if len(source) > MAX_SOURCE:
        return jsonify(error=f"Code is limited to {MAX_SOURCE} characters."), 413
    try:
        result = trace_source(source)
    except SyntaxError as exc:
        result = {"steps": [], "stdout": "", "error": f"SyntaxError on line {exc.lineno}: {exc.msg}"}
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=False, port=5000)
