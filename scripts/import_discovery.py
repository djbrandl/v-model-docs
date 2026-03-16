#!/usr/bin/env python3
"""Import discovery-answers.json into the V-model manifest.

Reads a discovery-answers.json exported from the HTML playground and updates
the manifest with: accepted requirements (with auto-assigned IDs), confirmed
components, environment details, overrides, and role definitions.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone


def _next_id(prefix: str, existing_ids: set[str]) -> str:
    """Generate the next sequential ID for a given prefix."""
    max_num = 0
    for eid in existing_ids:
        if eid.startswith(f"{prefix}-"):
            suffix = eid[len(prefix) + 1:]
            try:
                max_num = max(max_num, int(suffix))
            except ValueError:
                continue
    return f"{prefix}-{max_num + 1:03d}"


def import_discovery(answers_path: str, manifest_path: str) -> dict:
    """Merge discovery answers into the manifest. Returns updated manifest."""
    with open(answers_path, "r", encoding="utf-8") as fh:
        answers = json.load(fh)

    with open(manifest_path, "r", encoding="utf-8") as fh:
        manifest = json.load(fh)

    existing_ids = {r["id"] for r in manifest.get("requirements", [])}

    # --- System identity ---
    if "system_identity" in answers:
        si = answers["system_identity"]
        if si.get("project_name"):
            manifest["project"]["name"] = si["project_name"]
        if si.get("description"):
            manifest["project"]["description"] = si["description"]
        if si.get("gamp_category"):
            manifest["project"]["gamp_category"] = si["gamp_category"]
        if si.get("regulatory_context"):
            manifest["project"]["regulatory_context"] = si["regulatory_context"]

    # --- Accepted requirements ---
    if "requirements" in answers:
        for req in answers["requirements"]:
            if req.get("status") == "rejected":
                continue
            req_id = req.get("id") or _next_id("URS", existing_ids)
            existing_ids.add(req_id)
            manifest["requirements"].append({
                "id": req_id,
                "text": req.get("text", ""),
                "source_document": "urs",
                "traces_to": [],
                "tested_by": [],
            })

    # --- Components (store as project metadata) ---
    if "components" in answers:
        manifest["project"]["components"] = [
            c for c in answers["components"]
            if c.get("scope") != "out-of-scope"
        ]

    # --- User roles ---
    if "user_roles" in answers:
        manifest["project"]["user_roles"] = answers["user_roles"]

    # --- Environment ---
    if "environment" in answers:
        manifest["project"]["environment"] = answers["environment"]

    # --- Overrides ---
    if "overrides" in answers:
        for doc_type, override in answers["overrides"].items():
            manifest["overrides"][doc_type] = override

    # --- Write back ---
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest["project"]["last_discovery_import"] = now

    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")

    req_count = sum(1 for r in answers.get("requirements", []) if r.get("status") != "rejected")
    comp_count = len([c for c in answers.get("components", []) if c.get("scope") != "out-of-scope"])
    print(f"Imported {req_count} requirements, {comp_count} components into manifest.")
    print(f"Updated: {manifest_path}")

    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import discovery-answers.json into the V-model manifest.",
    )
    parser.add_argument("--answers", required=True, help="Path to discovery-answers.json")
    parser.add_argument("--manifest", required=True, help="Path to v-model-manifest.json")
    args = parser.parse_args()

    if not os.path.isfile(args.answers):
        print(f"ERROR: Answers file not found: {args.answers}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(args.manifest):
        print(f"ERROR: Manifest not found: {args.manifest}", file=sys.stderr)
        sys.exit(1)

    import_discovery(args.answers, args.manifest)


if __name__ == "__main__":
    main()
