"""Shared fixtures for v-model-docs test suite."""

import json
import pytest


@pytest.fixture
def minimal_manifest():
	"""Return the smallest valid manifest dict."""
	return {
		"project": {
			"name": "Test Project",
			"description": "A test project",
			"gamp_category": "5",
			"regulatory_context": ["21_CFR_11"],
			"audience": "mixed",
		},
		"documents": {},
		"requirements": [],
		"overrides": {},
	}


@pytest.fixture
def write_manifest(tmp_path):
	"""Factory fixture: write a manifest dict to tmp_path and return the path."""
	def _write(manifest_dict, filename="v-model-manifest.json"):
		p = tmp_path / filename
		p.write_text(json.dumps(manifest_dict, indent=2), encoding="utf-8")
		return str(p)
	return _write


@pytest.fixture
def write_answers(tmp_path):
	"""Factory fixture: write a discovery-answers dict and return the path."""
	def _write(answers_dict, filename="discovery-answers.json"):
		p = tmp_path / filename
		p.write_text(json.dumps(answers_dict, indent=2), encoding="utf-8")
		return str(p)
	return _write
