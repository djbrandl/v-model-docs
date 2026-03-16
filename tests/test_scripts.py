"""Test suite for v-model-docs Python scripts.

Covers init_project.py, traceability_check.py, and import_discovery.py.
Uses tmp_path for filesystem isolation; each test is independent.
"""

import json
import os
import sys

import pytest

# Ensure the scripts package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "scripts"))

from init_project import init_project, DOCUMENT_TYPES
from traceability_check import analyse, validate_manifest, _prefix, _is_critical_req, main as trace_main
from import_discovery import import_discovery, _next_id


# =========================================================================
# init_project.py
# =========================================================================

class TestInitProject:
	"""Tests for init_project.init_project()."""

	def test_creates_manifest_with_correct_schema(self, tmp_path):
		path = init_project(
			name="Acme LIMS",
			description="Laboratory information management system",
			gamp_category="5",
			regulatory_context=["21_CFR_11"],
			audience="mixed",
			base_dir=str(tmp_path),
		)
		assert os.path.isfile(path)
		with open(path, encoding="utf-8") as fh:
			data = json.load(fh)

		assert data["project"]["name"] == "Acme LIMS"
		assert data["project"]["description"] == "Laboratory information management system"
		assert data["project"]["gamp_category"] == "5"
		assert data["project"]["regulatory_context"] == ["21_CFR_11"]
		assert data["project"]["audience"] == "mixed"
		assert isinstance(data["requirements"], list)
		assert data["requirements"] == []
		assert isinstance(data["overrides"], dict)

	def test_manifest_contains_all_document_types(self, tmp_path):
		init_project(
			name="P", description="D", gamp_category="4",
			regulatory_context=["csa"], audience="technical",
			base_dir=str(tmp_path),
		)
		manifest_path = os.path.join(str(tmp_path), "docs", "v-model", "v-model-manifest.json")
		with open(manifest_path, encoding="utf-8") as fh:
			data = json.load(fh)

		for dt in DOCUMENT_TYPES:
			assert dt in data["documents"], f"Missing document type: {dt}"
			doc = data["documents"][dt]
			assert doc["status"] == "not_started"
			assert "last_updated" in doc
			assert doc["version"] == "0.0"

	def test_refuses_to_overwrite_existing_manifest(self, tmp_path):
		init_project(
			name="P", description="D", gamp_category="5",
			regulatory_context=["21_CFR_11"], audience="mixed",
			base_dir=str(tmp_path),
		)
		with pytest.raises(SystemExit) as exc_info:
			init_project(
				name="P2", description="D2", gamp_category="5",
				regulatory_context=["21_CFR_11"], audience="mixed",
				base_dir=str(tmp_path),
			)
		assert exc_info.value.code == 1

	def test_validates_gamp_category_invalid(self, tmp_path):
		with pytest.raises(ValueError, match="gamp_category"):
			init_project(
				name="P", description="D", gamp_category="99",
				regulatory_context=["21_CFR_11"], audience="mixed",
				base_dir=str(tmp_path),
			)

	def test_validates_gamp_category_none(self, tmp_path):
		path = init_project(
			name="P", description="D", gamp_category="none",
			regulatory_context=["21_CFR_11"], audience="mixed",
			base_dir=str(tmp_path),
		)
		with open(path, encoding="utf-8") as fh:
			data = json.load(fh)
		assert data["project"]["gamp_category"] == "none"

	def test_validates_regulatory_context_invalid(self, tmp_path):
		with pytest.raises(ValueError, match="Invalid regulatory context"):
			init_project(
				name="P", description="D", gamp_category="5",
				regulatory_context=["bogus_framework"], audience="mixed",
				base_dir=str(tmp_path),
			)

	def test_validates_regulatory_context_none(self, tmp_path):
		path = init_project(
			name="P", description="D", gamp_category="5",
			regulatory_context=["none"], audience="mixed",
			base_dir=str(tmp_path),
		)
		with open(path, encoding="utf-8") as fh:
			data = json.load(fh)
		assert data["project"]["regulatory_context"] == ["none"]

	def test_validates_audience_invalid(self, tmp_path):
		with pytest.raises(ValueError, match="audience"):
			init_project(
				name="P", description="D", gamp_category="5",
				regulatory_context=["21_CFR_11"], audience="executive",
				base_dir=str(tmp_path),
			)

	def test_validates_audience_values(self, tmp_path):
		for audience in ("mixed", "technical"):
			# Use a fresh subdirectory per iteration
			sub = tmp_path / audience
			sub.mkdir()
			path = init_project(
				name="P", description="D", gamp_category="5",
				regulatory_context=["21_CFR_11"], audience=audience,
				base_dir=str(sub),
			)
			with open(path, encoding="utf-8") as fh:
				data = json.load(fh)
			assert data["project"]["audience"] == audience

	def test_creates_directory_structure(self, tmp_path):
		init_project(
			name="P", description="D", gamp_category="5",
			regulatory_context=["21_CFR_11"], audience="mixed",
			base_dir=str(tmp_path),
		)
		vmodel_dir = tmp_path / "docs" / "v-model"
		assert vmodel_dir.is_dir()
		assert (vmodel_dir / "v-model-manifest.json").is_file()


# =========================================================================
# traceability_check.py  (highest priority)
# =========================================================================

class TestPrefix:
	"""Tests for the _prefix helper."""

	def test_simple_id(self):
		assert _prefix("URS-001") == "URS"

	def test_category_prefixed_id(self):
		assert _prefix("URS-FUN-001") == "URS"

	def test_fs_prefix(self):
		assert _prefix("FS-002") == "FS"

	def test_oq_prefix(self):
		assert _prefix("OQ-010") == "OQ"

	def test_empty_string(self):
		assert _prefix("") == ""

	def test_numeric_start(self):
		assert _prefix("123-ABC") == ""


class TestIsCriticalReq:
	"""Tests for severity classification via _is_critical_req."""

	def test_gmp_critical_tag(self):
		req = {"id": "URS-001", "tags": ["gmp_critical"]}
		assert _is_critical_req(req) is True

	def test_regulatory_tag(self):
		req = {"id": "URS-002", "tags": ["regulatory"]}
		assert _is_critical_req(req) is True

	def test_safety_tag(self):
		req = {"id": "URS-003", "tags": ["safety"]}
		assert _is_critical_req(req) is True

	def test_21_cfr_11_in_regulatory_context(self):
		req = {"id": "URS-004", "regulatory_context": ["21_cfr_11"]}
		assert _is_critical_req(req) is True

	def test_string_risk_field(self):
		req = {"id": "URS-005", "risk": "gmp_critical"}
		assert _is_critical_req(req) is True

	def test_functional_no_critical_tags(self):
		req = {"id": "URS-006", "tags": ["functional", "usability"]}
		assert _is_critical_req(req) is False

	def test_no_tags_at_all(self):
		req = {"id": "URS-007"}
		assert _is_critical_req(req) is False


class TestValidateManifest:
	"""Tests for validate_manifest schema checks."""

	def test_valid_manifest(self, minimal_manifest):
		errors = validate_manifest(minimal_manifest)
		assert errors == []

	def test_missing_project_key(self):
		data = {"requirements": []}
		errors = validate_manifest(data)
		assert any("project" in e for e in errors)

	def test_missing_requirements_key(self):
		data = {"project": {}}
		errors = validate_manifest(data)
		assert any("requirements" in e for e in errors)

	def test_requirements_not_array(self):
		data = {"project": {}, "requirements": "bad"}
		errors = validate_manifest(data)
		assert any("array" in e for e in errors)

	def test_requirement_missing_id(self):
		data = {"project": {}, "requirements": [{"text": "no id"}]}
		errors = validate_manifest(data)
		assert any("id" in e for e in errors)

	def test_traces_to_not_array(self):
		data = {"project": {}, "requirements": [{"id": "URS-001", "traces_to": "FS-001"}]}
		errors = validate_manifest(data)
		assert any("traces_to" in e and "array" in e for e in errors)

	def test_tested_by_not_array(self):
		data = {"project": {}, "requirements": [{"id": "URS-001", "tested_by": "OQ-001"}]}
		errors = validate_manifest(data)
		assert any("tested_by" in e and "array" in e for e in errors)


class TestAnalyse:
	"""Tests for the core analyse() gap-analysis function."""

	def _make_manifest(self, requirements):
		return {
			"project": {"name": "T", "gamp_category": "5"},
			"requirements": requirements,
		}

	# --- Untraced requirements ---

	def test_detects_untraced_urs(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "text": "The system shall do X"},
		])
		result = analyse(manifest)
		gap_types = [g["type"] for g in result["gaps"]]
		assert "untraced_requirement" in gap_types
		untraced = [g for g in result["gaps"] if g["type"] == "untraced_requirement"]
		assert untraced[0]["requirement"] == "URS-001"

	def test_traced_urs_has_no_untraced_gap(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "traces_to": ["FS-001"]},
			{"id": "FS-001"},
		])
		result = analyse(manifest)
		untraced = [g for g in result["gaps"] if g["type"] == "untraced_requirement"]
		assert len(untraced) == 0

	# --- Untested specs ---

	def test_detects_untested_fs(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "traces_to": ["FS-001"]},
			{"id": "FS-001"},
		])
		result = analyse(manifest)
		untested = [g for g in result["gaps"] if g["type"] == "untested_spec"]
		assert len(untested) == 1
		assert untested[0]["requirement"] == "FS-001"

	def test_fs_with_tested_by_is_not_untested(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "traces_to": ["FS-001"]},
			{"id": "FS-001", "tested_by": ["OQ-001"]},
			{"id": "OQ-001"},
		])
		result = analyse(manifest)
		untested = [g for g in result["gaps"] if g["type"] == "untested_spec"]
		assert len(untested) == 0

	def test_ds_untested(self):
		manifest = self._make_manifest([
			{"id": "DS-001"},
		])
		result = analyse(manifest)
		untested = [g for g in result["gaps"] if g["type"] == "untested_spec"]
		assert any(g["requirement"] == "DS-001" for g in untested)

	# --- Orphan tests ---

	def test_detects_orphan_test(self):
		manifest = self._make_manifest([
			{"id": "OQ-099"},
		])
		result = analyse(manifest)
		orphans = [g for g in result["gaps"] if g["type"] == "orphan_test"]
		assert len(orphans) == 1
		assert orphans[0]["requirement"] == "OQ-099"
		assert orphans[0]["severity"] == "minor"

	def test_test_referenced_by_tested_by_is_not_orphan(self):
		manifest = self._make_manifest([
			{"id": "FS-001", "tested_by": ["OQ-001"]},
			{"id": "OQ-001"},
		])
		result = analyse(manifest)
		orphans = [g for g in result["gaps"] if g["type"] == "orphan_test"]
		assert len(orphans) == 0

	def test_test_referenced_by_traces_to_is_not_orphan(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "traces_to": ["OQ-001"]},
			{"id": "OQ-001"},
		])
		result = analyse(manifest)
		orphans = [g for g in result["gaps"] if g["type"] == "orphan_test"]
		assert len(orphans) == 0

	# --- Broken traces ---

	def test_detects_broken_trace_in_traces_to(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "traces_to": ["FS-GHOST"]},
		])
		result = analyse(manifest)
		broken = [g for g in result["gaps"] if g["type"] == "broken_trace"]
		assert len(broken) == 1
		assert "FS-GHOST" in broken[0]["detail"]

	def test_detects_broken_trace_in_tested_by(self):
		manifest = self._make_manifest([
			{"id": "FS-001", "tested_by": ["OQ-MISSING"]},
		])
		result = analyse(manifest)
		broken = [g for g in result["gaps"] if g["type"] == "broken_trace"]
		assert len(broken) == 1
		assert "OQ-MISSING" in broken[0]["detail"]

	def test_valid_references_no_broken(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "traces_to": ["FS-001"]},
			{"id": "FS-001", "tested_by": ["OQ-001"]},
			{"id": "OQ-001"},
		])
		result = analyse(manifest)
		broken = [g for g in result["gaps"] if g["type"] == "broken_trace"]
		assert len(broken) == 0

	# --- Depth gaps ---

	def test_detects_depth_gap_urs_to_oq(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "traces_to": ["OQ-001"]},
			{"id": "OQ-001"},
		])
		result = analyse(manifest)
		depth = [g for g in result["gaps"] if g["type"] == "depth_gap"]
		assert len(depth) == 1
		assert "OQ" in depth[0]["detail"]

	def test_detects_depth_gap_urs_to_iq(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "traces_to": ["IQ-001"]},
			{"id": "IQ-001"},
		])
		result = analyse(manifest)
		depth = [g for g in result["gaps"] if g["type"] == "depth_gap"]
		assert len(depth) == 1

	def test_detects_depth_gap_urs_to_pq(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "traces_to": ["PQ-001"]},
			{"id": "PQ-001"},
		])
		result = analyse(manifest)
		depth = [g for g in result["gaps"] if g["type"] == "depth_gap"]
		assert len(depth) == 1

	def test_urs_to_fs_no_depth_gap(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "traces_to": ["FS-001"]},
			{"id": "FS-001"},
		])
		result = analyse(manifest)
		depth = [g for g in result["gaps"] if g["type"] == "depth_gap"]
		assert len(depth) == 0

	# --- Severity classification ---

	def test_critical_severity_for_gmp_critical_untraced(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "tags": ["gmp_critical"]},
		])
		result = analyse(manifest)
		untraced = [g for g in result["gaps"] if g["type"] == "untraced_requirement"]
		assert untraced[0]["severity"] == "critical"

	def test_major_severity_for_functional_untraced(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "tags": ["functional"]},
		])
		result = analyse(manifest)
		untraced = [g for g in result["gaps"] if g["type"] == "untraced_requirement"]
		assert untraced[0]["severity"] == "major"

	def test_critical_severity_broken_trace_gmp(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "traces_to": ["FS-GHOST"], "tags": ["gmp_critical"]},
		])
		result = analyse(manifest)
		broken = [g for g in result["gaps"] if g["type"] == "broken_trace"]
		assert broken[0]["severity"] == "critical"

	def test_major_severity_broken_trace_non_gmp(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "traces_to": ["FS-GHOST"], "tags": ["usability"]},
		])
		result = analyse(manifest)
		broken = [g for g in result["gaps"] if g["type"] == "broken_trace"]
		assert broken[0]["severity"] == "major"

	def test_depth_gap_severity_major_when_critical_req(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "traces_to": ["OQ-001"], "tags": ["gmp_critical"]},
			{"id": "OQ-001"},
		])
		result = analyse(manifest)
		depth = [g for g in result["gaps"] if g["type"] == "depth_gap"]
		assert depth[0]["severity"] == "major"

	def test_depth_gap_severity_minor_when_non_critical(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "traces_to": ["OQ-001"], "tags": ["usability"]},
			{"id": "OQ-001"},
		])
		result = analyse(manifest)
		depth = [g for g in result["gaps"] if g["type"] == "depth_gap"]
		assert depth[0]["severity"] == "minor"

	# --- Category-prefixed IDs ---

	def test_category_prefixed_urs_detected_untraced(self):
		manifest = self._make_manifest([
			{"id": "URS-FUN-001"},
		])
		result = analyse(manifest)
		untraced = [g for g in result["gaps"] if g["type"] == "untraced_requirement"]
		assert any(g["requirement"] == "URS-FUN-001" for g in untraced)

	def test_category_prefixed_fs_detected_untested(self):
		manifest = self._make_manifest([
			{"id": "FS-CFG-001"},
		])
		result = analyse(manifest)
		untested = [g for g in result["gaps"] if g["type"] == "untested_spec"]
		assert any(g["requirement"] == "FS-CFG-001" for g in untested)

	def test_category_prefixed_oq_orphan(self):
		manifest = self._make_manifest([
			{"id": "OQ-SEC-001"},
		])
		result = analyse(manifest)
		orphans = [g for g in result["gaps"] if g["type"] == "orphan_test"]
		assert any(g["requirement"] == "OQ-SEC-001" for g in orphans)

	# --- Empty manifest ---

	def test_empty_requirements_no_crash(self):
		manifest = self._make_manifest([])
		result = analyse(manifest)
		assert result["gaps"] == []
		assert result["metrics"]["total_requirements"] == 0
		assert result["metrics"]["total_urs"] == 0
		assert result["metrics"]["coverage_pct"] == 0.0
		assert result["metrics"]["verification_pct"] == 0.0

	# --- Coverage metrics ---

	def test_coverage_metrics_full_trace(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "traces_to": ["FS-001"], "tested_by": ["OQ-001"]},
			{"id": "URS-002", "traces_to": ["FS-002"], "tested_by": ["OQ-002"]},
			{"id": "FS-001", "tested_by": ["OQ-001"]},
			{"id": "FS-002", "tested_by": ["OQ-002"]},
			{"id": "OQ-001"},
			{"id": "OQ-002"},
		])
		result = analyse(manifest)
		m = result["metrics"]
		assert m["total_requirements"] == 6
		assert m["total_urs"] == 2
		assert m["coverage_pct"] == 100.0
		assert m["verification_pct"] == 100.0

	def test_coverage_metrics_partial_trace(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "traces_to": ["FS-001"]},
			{"id": "URS-002"},  # not traced
			{"id": "FS-001", "tested_by": ["OQ-001"]},
			{"id": "OQ-001"},
		])
		result = analyse(manifest)
		m = result["metrics"]
		assert m["total_urs"] == 2
		assert m["coverage_pct"] == 50.0
		# URS-001 has no tested_by, URS-002 has no tested_by
		assert m["verification_pct"] == 0.0

	def test_orphan_rate_metric(self):
		manifest = self._make_manifest([
			{"id": "OQ-001"},  # orphan
			{"id": "OQ-002"},  # orphan
			{"id": "IQ-001"},  # orphan
		])
		result = analyse(manifest)
		m = result["metrics"]
		assert m["orphan_count"] == 3
		assert m["orphan_rate"] == 100.0

	def test_gaps_by_severity_in_metrics(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "tags": ["gmp_critical"]},  # critical untraced
			{"id": "URS-002"},  # major untraced
		])
		result = analyse(manifest)
		sev = result["metrics"]["gaps_by_severity"]
		assert sev.get("critical", 0) >= 1
		assert sev.get("major", 0) >= 1

	# --- Duplicate trace detection ---

	def test_duplicate_trace_detected(self):
		manifest = self._make_manifest([
			{"id": "URS-001", "traces_to": ["FS-001", "FS-001"]},
			{"id": "FS-001", "tested_by": ["OQ-001"]},
			{"id": "OQ-001"},
		])
		result = analyse(manifest)
		dups = [g for g in result["gaps"] if g["type"] == "duplicate_trace"]
		assert len(dups) >= 1


class TestTraceabilityCLI:
	"""Tests for the traceability_check CLI (main function)."""

	def test_exit_code_0_when_no_critical_gaps(self, tmp_path, monkeypatch):
		manifest = {
			"project": {"name": "T"},
			"requirements": [
				{"id": "URS-001", "traces_to": ["FS-001"]},
				{"id": "FS-001", "tested_by": ["OQ-001"]},
				{"id": "OQ-001"},
			],
		}
		mp = tmp_path / "manifest.json"
		mp.write_text(json.dumps(manifest), encoding="utf-8")
		monkeypatch.setattr(
			"sys.argv",
			["traceability_check.py", "--manifest", str(mp)],
		)
		exit_code = trace_main()
		assert exit_code == 0

	def test_exit_code_1_when_critical_gaps(self, tmp_path, monkeypatch):
		manifest = {
			"project": {"name": "T"},
			"requirements": [
				{"id": "URS-001", "tags": ["gmp_critical"]},
			],
		}
		mp = tmp_path / "manifest.json"
		mp.write_text(json.dumps(manifest), encoding="utf-8")
		monkeypatch.setattr(
			"sys.argv",
			["traceability_check.py", "--manifest", str(mp)],
		)
		exit_code = trace_main()
		assert exit_code == 1

	def test_json_output_mode(self, tmp_path, monkeypatch, capsys):
		manifest = {
			"project": {"name": "T"},
			"requirements": [
				{"id": "URS-001", "traces_to": ["FS-001"]},
				{"id": "FS-001", "tested_by": ["OQ-001"]},
				{"id": "OQ-001"},
			],
		}
		mp = tmp_path / "manifest.json"
		mp.write_text(json.dumps(manifest), encoding="utf-8")
		monkeypatch.setattr(
			"sys.argv",
			["traceability_check.py", "--manifest", str(mp), "--json"],
		)
		exit_code = trace_main()
		assert exit_code == 0
		captured = capsys.readouterr()
		data = json.loads(captured.out)
		assert "gaps" in data
		assert "metrics" in data
		assert "requirements" in data

	def test_empty_manifest_json_output(self, tmp_path, monkeypatch, capsys):
		manifest = {
			"project": {"name": "T"},
			"requirements": [],
		}
		mp = tmp_path / "manifest.json"
		mp.write_text(json.dumps(manifest), encoding="utf-8")
		monkeypatch.setattr(
			"sys.argv",
			["traceability_check.py", "--manifest", str(mp), "--json"],
		)
		exit_code = trace_main()
		assert exit_code == 0
		captured = capsys.readouterr()
		data = json.loads(captured.out)
		assert data["metrics"]["total_requirements"] == 0
		assert data["gaps"] == []

	def test_empty_manifest_markdown_output(self, tmp_path, monkeypatch, capsys):
		manifest = {
			"project": {"name": "T"},
			"requirements": [],
		}
		mp = tmp_path / "manifest.json"
		mp.write_text(json.dumps(manifest), encoding="utf-8")
		monkeypatch.setattr(
			"sys.argv",
			["traceability_check.py", "--manifest", str(mp)],
		)
		exit_code = trace_main()
		assert exit_code == 0
		captured = capsys.readouterr()
		assert "No requirements found" in captured.out

	def test_missing_manifest_returns_1(self, tmp_path, monkeypatch):
		monkeypatch.setattr(
			"sys.argv",
			["traceability_check.py", "--manifest", str(tmp_path / "nope.json")],
		)
		exit_code = trace_main()
		assert exit_code == 1

	def test_invalid_json_returns_1(self, tmp_path, monkeypatch):
		bad = tmp_path / "bad.json"
		bad.write_text("{not json}", encoding="utf-8")
		monkeypatch.setattr(
			"sys.argv",
			["traceability_check.py", "--manifest", str(bad)],
		)
		exit_code = trace_main()
		assert exit_code == 1

	def test_output_file_written(self, tmp_path, monkeypatch):
		manifest = {
			"project": {"name": "T"},
			"requirements": [
				{"id": "URS-001", "traces_to": ["FS-001"]},
				{"id": "FS-001", "tested_by": ["OQ-001"]},
				{"id": "OQ-001"},
			],
		}
		mp = tmp_path / "manifest.json"
		mp.write_text(json.dumps(manifest), encoding="utf-8")
		out = tmp_path / "report.md"
		monkeypatch.setattr(
			"sys.argv",
			["traceability_check.py", "--manifest", str(mp), "--output", str(out)],
		)
		trace_main()
		assert out.is_file()
		content = out.read_text(encoding="utf-8")
		assert "Traceability Gap Analysis" in content


# =========================================================================
# import_discovery.py
# =========================================================================

class TestNextId:
	"""Tests for the _next_id helper."""

	def test_first_id(self):
		assert _next_id("URS", set()) == "URS-001"

	def test_increments_existing(self):
		assert _next_id("URS", {"URS-001", "URS-002"}) == "URS-003"

	def test_ignores_other_prefixes(self):
		assert _next_id("FS", {"URS-001", "URS-002", "FS-005"}) == "FS-006"

	def test_handles_non_numeric_suffixes(self):
		assert _next_id("URS", {"URS-001", "URS-FUN-001"}) == "URS-002"


class TestImportDiscovery:
	"""Tests for import_discovery.import_discovery()."""

	def test_imports_accepted_requirements(self, minimal_manifest, write_manifest, write_answers):
		mp = write_manifest(minimal_manifest)
		ap = write_answers({
			"requirements": [
				{"id": "URS-001", "text": "System shall authenticate users", "status": "accepted"},
				{"id": "URS-002", "text": "System shall log actions", "status": "accepted"},
			]
		})
		result = import_discovery(ap, mp)
		req_ids = [r["id"] for r in result["requirements"]]
		assert "URS-001" in req_ids
		assert "URS-002" in req_ids

	def test_skips_rejected_requirements(self, minimal_manifest, write_manifest, write_answers):
		mp = write_manifest(minimal_manifest)
		ap = write_answers({
			"requirements": [
				{"id": "URS-001", "text": "Keep this", "status": "accepted"},
				{"id": "URS-002", "text": "Reject this", "status": "rejected"},
			]
		})
		result = import_discovery(ap, mp)
		req_ids = [r["id"] for r in result["requirements"]]
		assert "URS-001" in req_ids
		assert "URS-002" not in req_ids

	def test_auto_assigns_ids_when_not_provided(self, minimal_manifest, write_manifest, write_answers):
		mp = write_manifest(minimal_manifest)
		ap = write_answers({
			"requirements": [
				{"text": "First requirement", "status": "accepted"},
				{"text": "Second requirement", "status": "accepted"},
			]
		})
		result = import_discovery(ap, mp)
		req_ids = [r["id"] for r in result["requirements"]]
		assert "URS-001" in req_ids
		assert "URS-002" in req_ids

	def test_auto_assigns_ids_respects_existing(self, minimal_manifest, write_manifest, write_answers):
		minimal_manifest["requirements"] = [
			{"id": "URS-001", "text": "Existing", "source_document": "urs", "traces_to": [], "tested_by": []},
		]
		mp = write_manifest(minimal_manifest)
		ap = write_answers({
			"requirements": [
				{"text": "New requirement", "status": "accepted"},
			]
		})
		result = import_discovery(ap, mp)
		req_ids = [r["id"] for r in result["requirements"]]
		assert "URS-001" in req_ids
		assert "URS-002" in req_ids

	def test_imports_components(self, minimal_manifest, write_manifest, write_answers):
		mp = write_manifest(minimal_manifest)
		ap = write_answers({
			"components": [
				{"name": "Auth Module", "scope": "in-scope"},
				{"name": "Legacy DB", "scope": "out-of-scope"},
				{"name": "Reporting", "scope": "in-scope"},
			]
		})
		result = import_discovery(ap, mp)
		components = result["project"]["components"]
		names = [c["name"] for c in components]
		assert "Auth Module" in names
		assert "Reporting" in names
		assert "Legacy DB" not in names

	def test_imports_overrides(self, minimal_manifest, write_manifest, write_answers):
		mp = write_manifest(minimal_manifest)
		ap = write_answers({
			"overrides": {
				"urs": {"tone": "formal", "extra_sections": ["appendix"]},
				"fs": {"detail_level": "high"},
			}
		})
		result = import_discovery(ap, mp)
		assert result["overrides"]["urs"]["tone"] == "formal"
		assert result["overrides"]["fs"]["detail_level"] == "high"

	def test_does_not_overwrite_existing_requirements(self, minimal_manifest, write_manifest, write_answers):
		minimal_manifest["requirements"] = [
			{"id": "URS-001", "text": "Original", "source_document": "urs", "traces_to": [], "tested_by": []},
		]
		mp = write_manifest(minimal_manifest)
		ap = write_answers({
			"requirements": [
				{"id": "URS-010", "text": "New one", "status": "accepted"},
			]
		})
		result = import_discovery(ap, mp)
		texts = {r["id"]: r["text"] for r in result["requirements"]}
		assert texts["URS-001"] == "Original"
		assert texts["URS-010"] == "New one"

	def test_does_not_overwrite_existing_overrides(self, minimal_manifest, write_manifest, write_answers):
		minimal_manifest["overrides"] = {"urs": {"tone": "casual"}}
		mp = write_manifest(minimal_manifest)
		ap = write_answers({
			"overrides": {
				"fs": {"detail_level": "high"},
			}
		})
		result = import_discovery(ap, mp)
		# urs override replaced by absence in answers, fs added
		assert result["overrides"]["fs"]["detail_level"] == "high"
		# Original urs override is still present because answers only has fs
		assert result["overrides"]["urs"]["tone"] == "casual"

	def test_imports_user_roles(self, minimal_manifest, write_manifest, write_answers):
		mp = write_manifest(minimal_manifest)
		ap = write_answers({
			"user_roles": [
				{"name": "Admin", "permissions": ["all"]},
				{"name": "Viewer", "permissions": ["read"]},
			]
		})
		result = import_discovery(ap, mp)
		assert len(result["project"]["user_roles"]) == 2

	def test_imports_environment(self, minimal_manifest, write_manifest, write_answers):
		mp = write_manifest(minimal_manifest)
		ap = write_answers({
			"environment": {"hosting": "cloud", "database": "PostgreSQL"}
		})
		result = import_discovery(ap, mp)
		assert result["project"]["environment"]["hosting"] == "cloud"

	def test_updates_system_identity(self, minimal_manifest, write_manifest, write_answers):
		mp = write_manifest(minimal_manifest)
		ap = write_answers({
			"system_identity": {
				"project_name": "New Name",
				"description": "Updated desc",
				"gamp_category": "4",
				"regulatory_context": ["annex_11"],
			}
		})
		result = import_discovery(ap, mp)
		assert result["project"]["name"] == "New Name"
		assert result["project"]["description"] == "Updated desc"
		assert result["project"]["gamp_category"] == "4"
		assert result["project"]["regulatory_context"] == ["annex_11"]

	def test_sets_last_discovery_import_timestamp(self, minimal_manifest, write_manifest, write_answers):
		mp = write_manifest(minimal_manifest)
		ap = write_answers({"requirements": []})
		result = import_discovery(ap, mp)
		assert "last_discovery_import" in result["project"]
		# Should be an ISO-ish timestamp
		ts = result["project"]["last_discovery_import"]
		assert ts.endswith("Z")
		assert "T" in ts

	def test_manifest_file_updated_on_disk(self, minimal_manifest, write_manifest, write_answers):
		mp = write_manifest(minimal_manifest)
		ap = write_answers({
			"requirements": [
				{"id": "URS-001", "text": "Disk check", "status": "accepted"},
			]
		})
		import_discovery(ap, mp)
		with open(mp, encoding="utf-8") as fh:
			on_disk = json.load(fh)
		assert any(r["id"] == "URS-001" for r in on_disk["requirements"])


# =========================================================================
# Integration-level: full pipeline
# =========================================================================

class TestIntegrationPipeline:
	"""End-to-end: init -> import -> trace."""

	def test_init_import_trace_pipeline(self, tmp_path):
		# Step 1: init
		manifest_path = init_project(
			name="Pipeline Test",
			description="Integration test",
			gamp_category="5",
			regulatory_context=["21_CFR_11"],
			audience="mixed",
			base_dir=str(tmp_path),
		)

		# Step 2: import discovery
		answers = {
			"requirements": [
				{"id": "URS-001", "text": "Authenticate users", "status": "accepted"},
				{"id": "URS-002", "text": "Log all actions", "status": "accepted"},
				{"text": "Auto-ID test", "status": "accepted"},
				{"text": "Rejected", "status": "rejected"},
			],
			"components": [
				{"name": "Auth", "scope": "in-scope"},
			],
		}
		answers_path = str(tmp_path / "answers.json")
		with open(answers_path, "w", encoding="utf-8") as fh:
			json.dump(answers, fh)

		updated = import_discovery(answers_path, manifest_path)
		assert len(updated["requirements"]) == 3  # 2 explicit + 1 auto-assigned

		# Step 3: traceability check (all URS untraced -> gaps expected)
		result = analyse(updated)
		untraced = [g for g in result["gaps"] if g["type"] == "untraced_requirement"]
		assert len(untraced) == 3  # all 3 URS are untraced
		assert result["metrics"]["coverage_pct"] == 0.0
