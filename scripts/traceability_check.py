#!/usr/bin/env python3
"""V-Model traceability gap analysis.

Reads a v-model-manifest.json, walks every requirement's forward and backward
trace links, classifies gaps by type and severity, computes coverage metrics,
and outputs a structured report (markdown or JSON).

Exit code 0 = no critical gaps.  Exit code 1 = critical gaps found.
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SPEC_PREFIXES = {"FS", "DS"}
TEST_PREFIXES = {"IQ", "OQ", "PQ"}

# Regulatory / criticality tags that elevate severity to critical
CRITICAL_TAGS = {
	"gmp_critical", "regulatory", "safety", "21_cfr_11", "annex_11",
	"data_integrity", "electronic_signature", "alcoa",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _prefix(req_id: str) -> str:
	"""Extract the document-type prefix from a requirement ID.

	Handles both simple IDs (URS-001) and category-prefixed IDs (URS-FUN-001).
	Always returns the first segment before the first dash.
	"""
	parts = req_id.split("-")
	return parts[0] if parts and parts[0].isalpha() else ""


def _is_critical_req(req: dict) -> bool:
	"""Return True if the requirement carries regulatory / safety tags."""
	tags = set()
	for field in ("tags", "risk", "regulatory_context"):
		val = req.get(field, [])
		if isinstance(val, str):
			tags.add(val.lower())
		elif isinstance(val, list):
			tags.update(v.lower() for v in val)
	return bool(tags & CRITICAL_TAGS)

# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------

def validate_manifest(data: dict) -> list[str]:
	"""Return a list of schema validation errors (empty = valid)."""
	errors = []
	if not isinstance(data, dict):
		return ["Manifest root must be a JSON object"]
	if "project" not in data:
		errors.append("Missing top-level 'project' key")
	if "requirements" not in data:
		errors.append("Missing top-level 'requirements' key")
	elif not isinstance(data["requirements"], list):
		errors.append("'requirements' must be an array")
	else:
		for i, req in enumerate(data["requirements"]):
			if not isinstance(req, dict):
				errors.append(f"requirements[{i}] must be an object")
				continue
			if "id" not in req:
				errors.append(f"requirements[{i}] missing 'id'")
			if "traces_to" in req and not isinstance(req["traces_to"], list):
				errors.append(f"requirements[{i}] 'traces_to' must be an array")
			if "tested_by" in req and not isinstance(req["tested_by"], list):
				errors.append(f"requirements[{i}] 'tested_by' must be an array")
	if "documents" in data and not isinstance(data.get("documents"), dict):
		errors.append("'documents' must be an object")
	return errors

# ---------------------------------------------------------------------------
# Core analysis
# ---------------------------------------------------------------------------

def analyse(manifest: dict) -> dict:
	"""Run full gap analysis. Returns a results dict."""
	requirements = manifest.get("requirements", [])
	all_ids = {r["id"] for r in requirements if "id" in r}

	# Build backward maps: target -> list of source IDs
	traced_from: dict[str, list[str]] = defaultdict(list)
	tested_from: dict[str, list[str]] = defaultdict(list)
	for req in requirements:
		for t in req.get("traces_to", []):
			traced_from[t].append(req["id"])
		for t in req.get("tested_by", []):
			tested_from[t].append(req["id"])

	gaps: list[dict] = []

	for req in requirements:
		rid, prefix = req["id"], _prefix(req["id"])
		traces_to = req.get("traces_to", [])
		tested_by = req.get("tested_by", [])
		is_crit = _is_critical_req(req)

		# Broken traces: referenced ID does not exist
		for ref in traces_to + tested_by:
			if ref not in all_ids:
				gaps.append({"type": "broken_trace", "requirement": rid,
					"detail": f"Referenced ID '{ref}' does not exist in manifest",
					"severity": "critical" if is_crit else "major"})

		# Untraced requirement: URS with no forward trace
		if prefix == "URS" and not traces_to:
			gaps.append({"type": "untraced_requirement", "requirement": rid,
				"detail": "URS requirement has no forward trace to any specification",
				"severity": "critical" if is_crit else "major"})

		# Untested spec: FS/DS with no test link (forward or backward)
		if prefix in SPEC_PREFIXES and not tested_by and rid not in tested_from:
			gaps.append({"type": "untested_spec", "requirement": rid,
				"detail": f"{prefix} item has no linked test protocol",
				"severity": "critical" if is_crit else "major"})

		# Orphan test: test with no backward trace to any spec/req
		if prefix in TEST_PREFIXES and rid not in traced_from and rid not in tested_from:
			gaps.append({"type": "orphan_test", "requirement": rid,
				"detail": "Test case traces to no requirement or specification",
				"severity": "minor"})

		# Depth gap: URS traces directly to test, skipping spec level
		if prefix == "URS":
			for t in traces_to:
				if _prefix(t) in TEST_PREFIXES:
					gaps.append({"type": "depth_gap", "requirement": rid,
						"detail": f"URS traces directly to {t} ({_prefix(t)}), bypassing specification level",
						"severity": "major" if is_crit else "minor"})

	# ID naming issues (informational)
	id_pat = re.compile(r"^(?:.*-)?[A-Z]{2,3}-\d{3,}$")
	for rid in all_ids:
		if not id_pat.match(rid):
			gaps.append({"type": "id_naming", "requirement": rid,
				"detail": f"ID '{rid}' does not follow the {{PREFIX}}-{{NNN}} convention",
				"severity": "informational"})

	# Duplicate trace detection (informational)
	for req in requirements:
		for field in ("traces_to", "tested_by"):
			refs = req.get(field, [])
			if len(refs) != len(set(refs)):
				gaps.append({"type": "duplicate_trace", "requirement": req["id"],
					"detail": f"Duplicate entries in '{field}'",
					"severity": "informational"})

	# Compute metrics
	urs_reqs = [r for r in requirements if _prefix(r["id"]) == "URS"]
	total_urs = len(urs_reqs)
	traced_count = sum(1 for r in urs_reqs if r.get("traces_to"))
	verified_count = sum(1 for r in urs_reqs if r.get("tested_by"))
	orphan_count = sum(1 for g in gaps if g["type"] == "orphan_test")
	test_reqs = [r for r in requirements if _prefix(r["id"]) in TEST_PREFIXES]
	by_severity = defaultdict(int)
	for g in gaps:
		by_severity[g["severity"]] += 1

	metrics = {
		"total_requirements": len(requirements),
		"total_urs": total_urs,
		"coverage_pct": round(traced_count / total_urs * 100, 1) if total_urs else 0.0,
		"verification_pct": round(verified_count / total_urs * 100, 1) if total_urs else 0.0,
		"orphan_count": orphan_count,
		"orphan_rate": round(orphan_count / len(test_reqs) * 100, 1) if test_reqs else 0.0,
		"gaps_by_severity": dict(by_severity),
		"total_gaps": len(gaps),
	}
	return {"gaps": gaps, "metrics": metrics, "requirements": requirements}

# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------

def render_markdown(results: dict, verbose: bool = False) -> str:
	"""Render the gap analysis as a markdown report."""
	gaps, m = results["gaps"], results["metrics"]
	lines = ["# Traceability Gap Analysis Report", "", "## Metrics", "",
		"| Metric | Value |", "|---|---|",
		f"| Total requirements | {m['total_requirements']} |",
		f"| URS requirements | {m['total_urs']} |",
		f"| Coverage | {m['coverage_pct']}% |",
		f"| Verification | {m['verification_pct']}% |",
		f"| Orphan tests | {m['orphan_count']} ({m['orphan_rate']}%) |",
		f"| Total gaps | {m['total_gaps']} |", ""]
	for sev in ("critical", "major", "minor", "informational"):
		lines.append(f"- **{sev.capitalize()}**: {m['gaps_by_severity'].get(sev, 0)}")
	lines.append("")
	if not gaps:
		lines.append("**No traceability gaps detected.**")
		return "\n".join(lines)
	lines += ["## Gaps", ""]
	for sev in ("critical", "major", "minor", "informational"):
		sev_gaps = [g for g in gaps if g["severity"] == sev]
		if not sev_gaps:
			continue
		lines += [f"### {sev.capitalize()} ({len(sev_gaps)})", ""]
		by_type = defaultdict(list)
		for g in sev_gaps:
			by_type[g["type"]].append(g)
		for gtype, items in sorted(by_type.items()):
			lines += [f"**{gtype.replace('_', ' ').title()}**", ""]
			lines += [f"- `{it['requirement']}`: {it['detail']}" for it in items]
			lines.append("")
	if verbose:
		lines += ["## Per-Requirement Trace Details", "",
			"| ID | traces_to | tested_by |", "|---|---|---|"]
		for req in results["requirements"]:
			fwd = ", ".join(req.get("traces_to", [])) or "--"
			tst = ", ".join(req.get("tested_by", [])) or "--"
			lines.append(f"| {req['id']} | {fwd} | {tst} |")
		lines.append("")
	return "\n".join(lines)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
	parser = argparse.ArgumentParser(description="V-Model traceability gap analysis")
	parser.add_argument("--manifest", required=True, help="Path to v-model-manifest.json")
	parser.add_argument("--output", default=None, help="Save report to file (optional)")
	parser.add_argument("--json", action="store_true", dest="json_output",
		help="Output machine-readable JSON instead of markdown")
	parser.add_argument("--verbose", action="store_true",
		help="Include per-requirement trace details")
	args = parser.parse_args()

	# Load manifest
	manifest_path = Path(args.manifest)
	if not manifest_path.is_file():
		print(f"Error: manifest not found at {manifest_path}", file=sys.stderr)
		return 1
	try:
		data = json.loads(manifest_path.read_text(encoding="utf-8"))
	except (json.JSONDecodeError, OSError) as exc:
		print(f"Error: failed to read manifest: {exc}", file=sys.stderr)
		return 1

	# Validate schema
	errors = validate_manifest(data)
	if errors:
		print("Manifest validation errors:", file=sys.stderr)
		for err in errors:
			print(f"  - {err}", file=sys.stderr)
		return 1

	# Handle empty requirements
	requirements = data.get("requirements", [])
	if not requirements:
		empty = {"gaps": [], "metrics": {
			"total_requirements": 0, "total_urs": 0, "coverage_pct": 0.0,
			"verification_pct": 0.0, "orphan_count": 0, "orphan_rate": 0.0,
			"gaps_by_severity": {}, "total_gaps": 0}, "requirements": []}
		report = json.dumps(empty, indent=2) if args.json_output else \
			"# Traceability Gap Analysis Report\n\nNo requirements found in manifest.\n"
		print(report)
		if args.output:
			Path(args.output).write_text(report, encoding="utf-8")
		return 0

	# Run analysis and render
	results = analyse(data)
	report = json.dumps(results, indent=2) if args.json_output else \
		render_markdown(results, verbose=args.verbose)
	print(report)
	if args.output:
		Path(args.output).write_text(report, encoding="utf-8")
		print(f"\nReport saved to {args.output}", file=sys.stderr)

	# Exit code: 1 if critical gaps exist
	return 1 if results["metrics"]["gaps_by_severity"].get("critical", 0) > 0 else 0


if __name__ == "__main__":
	sys.exit(main())
