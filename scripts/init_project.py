#!/usr/bin/env python3
"""Initialize a V-model documentation project by scaffolding the manifest."""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

MANIFEST_REL_PATH = os.path.join("docs", "v-model", "v-model-manifest.json")

DOCUMENT_TYPES = ("urs", "fs", "ds", "vp", "iq", "oq", "pq", "traceability", "risk_assessment", "vendor_assessment", "vsr")

VALID_GAMP_CATEGORIES = ("3", "4", "5", "none")
VALID_REGULATORY_CONTEXTS = {"21_CFR_11", "annex_11", "csa", "none"}
VALID_AUDIENCES = ("mixed", "technical")


def init_project(
	name: str,
	description: str,
	gamp_category: str,
	regulatory_context: list[str],
	audience: str,
	base_dir: str | None = None,
) -> str:
	"""Create the V-model manifest and return the absolute path to it.

	Raises SystemExit if a manifest already exists, ValueError on bad inputs.
	"""
	if gamp_category not in VALID_GAMP_CATEGORIES:
		raise ValueError(f"gamp_category must be one of {VALID_GAMP_CATEGORIES}, got '{gamp_category}'")
	for ctx in regulatory_context:
		if ctx not in VALID_REGULATORY_CONTEXTS:
			raise ValueError(f"Invalid regulatory context '{ctx}'. Valid: {sorted(VALID_REGULATORY_CONTEXTS)}")
	if audience not in VALID_AUDIENCES:
		raise ValueError(f"audience must be one of {VALID_AUDIENCES}, got '{audience}'")

	base = base_dir or os.getcwd()
	manifest_path = os.path.join(base, MANIFEST_REL_PATH)

	if os.path.exists(manifest_path):
		print(f"ERROR: Manifest already exists at {manifest_path}", file=sys.stderr)
		print("Remove it manually if you want to re-initialize.", file=sys.stderr)
		sys.exit(1)

	now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

	documents = {
		dt: {"status": "not_started", "path": "", "last_updated": now, "version": "0.0"}
		for dt in DOCUMENT_TYPES
	}

	manifest = {
		"project": {
			"name": name,
			"description": description,
			"gamp_category": gamp_category,
			"regulatory_context": regulatory_context,
			"audience": audience,
		},
		"documents": documents,
		"requirements": [],
		"overrides": {},
	}

	os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
	os.makedirs(os.path.join(os.path.dirname(manifest_path), "documents"), exist_ok=True)

	with open(manifest_path, "w", encoding="utf-8") as fh:
		json.dump(manifest, fh, indent=2)
		fh.write("\n")

	return manifest_path


def _build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(
		description="Scaffold a V-model documentation project (manifest + directory structure).",
	)
	parser.add_argument("--name", required=True, help="Project name (e.g. 'Acme LIMS')")
	parser.add_argument("--description", required=True, help="One-line project description")
	parser.add_argument(
		"--gamp-category",
		required=True,
		choices=VALID_GAMP_CATEGORIES,
		help="GAMP 5 software category",
	)
	parser.add_argument(
		"--regulatory-context",
		required=True,
		help="Comma-separated regulatory frameworks: 21_CFR_11,annex_11,csa",
	)
	parser.add_argument(
		"--audience",
		required=True,
		choices=VALID_AUDIENCES,
		help="Target audience for generated documents",
	)
	return parser


def main() -> None:
	parser = _build_parser()
	args = parser.parse_args()

	reg_ctx = [token.strip() for token in args.regulatory_context.split(",") if token.strip()]

	path = init_project(
		name=args.name,
		description=args.description,
		gamp_category=args.gamp_category,
		regulatory_context=reg_ctx,
		audience=args.audience,
	)

	print(f"Manifest created: {path}")
	print()
	print("Suggested next steps:")
	print("  1. Review the manifest at docs/v-model/v-model-manifest.json")
	print("  2. Run discovery to populate requirements (or start writing the VP)")
	print("  3. Generate documents in order: VP -> URS -> FS -> DS -> IQ -> OQ -> PQ")


if __name__ == "__main__":
	main()
