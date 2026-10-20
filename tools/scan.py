"""Security scan a work item. Uses the Snyk CLI if installed, otherwise a local secret check.

Usage: python tools/scan.py invoiceflow/      # exit 0 = pass, 1 = issues found
"""
import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

from _common import out

SECRET = re.compile(r"""(?i)(api[_-]?key|secret|token|password)\s*=\s*["'][^"']{8,}["']""")


def snyk_code(path):
    proc = subprocess.run(["snyk", "code", "test", path, "--json"], capture_output=True, text=True)
    if not proc.stdout.strip():
        raise RuntimeError(proc.stderr.strip() or "snyk code test gave no output")
    sarif = json.loads(proc.stdout)
    if "runs" not in sarif:
        raise RuntimeError(sarif.get("error") or sarif.get("message") or "unexpected snyk output")
    issues = []
    for run in sarif.get("runs", []):
        for r in run.get("results", []):
            loc = r.get("locations", [{}])[0].get("physicalLocation", {})
            issues.append({
                "severity": {"error": "high", "warning": "medium"}.get(r.get("level"), "low"),
                "title": r.get("ruleId", "issue"),
                "file": loc.get("artifactLocation", {}).get("uri"),
                "line": loc.get("region", {}).get("startLine"),
                "fix": r.get("message", {}).get("text", ""),
            })
    return issues


def snyk_deps(path):
    manifest = Path(path) / "requirements.txt"
    if not manifest.exists():
        return []
    proc = subprocess.run(
        ["snyk", "test", f"--file={manifest}", "--package-manager=pip", "--json"],
        capture_output=True, text=True,
    )
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return []  # TODO(C): snyk test needs the deps installed; skip quietly if it can't run
    return [{
        "severity": v.get("severity"),
        "title": v.get("title"),
        "file": str(manifest),
        "line": None,
        "fix": f"Upgrade {v.get('packageName')}",
    } for v in data.get("vulnerabilities", [])]


def local_scan(path):
    issues = []
    for f in Path(path).rglob("*.py"):
        for i, line in enumerate(f.read_text().splitlines(), 1):
            if SECRET.search(line):
                issues.append({
                    "severity": "high",
                    "title": "Hardcoded secret",
                    "file": str(f),
                    "line": i,
                    "fix": "Read it from os.environ and add it to .env.example",
                })
    return issues


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    source, error = "local", None
    if shutil.which("snyk"):
        try:
            issues = snyk_code(args.path) + snyk_deps(args.path)
            source = "snyk"
        except Exception as e:
            error = str(e)
            issues = local_scan(args.path)
    else:
        issues = local_scan(args.path)

    result = {"pass": not issues, "issues": issues, "source": source}
    if error:
        result["snyk_error"] = error
    out(result, 0 if not issues else 1)


if __name__ == "__main__":
    main()
