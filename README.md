# v-model-docs

An AI-powered skill for generating V-model documentation packages. Built for **software vendors** who need to provide validation-ready documentation to life sciences customers (pharma, biotech, medical device).

## What It Does

Guides you through producing a complete V-model documentation package:

| Document | Ownership | Description |
|---|---|---|
| **URS** | Customer-assist | User Requirements Specification — starter template for your customer |
| **FS** | Vendor-owned | Functional Specification — your primary promise of system behavior |
| **DS** | Vendor-owned | Design Specification — technical blueprint |
| **VP** | Customer-assist | Validation Plan — vendor input section |
| **Risk Assessment** | Vendor-owned | FMEA-based risk analysis driving test depth |
| **IQ Protocol** | Vendor-owned | Installation Qualification — customer-executable |
| **OQ Protocol** | Vendor-owned | Operational Qualification — customer-executable |
| **PQ Protocol** | Customer-assist | Performance Qualification — recommended scenarios |
| **Traceability Matrix** | Vendor-owned | Computed from manifest — gap analysis included |
| **Vendor Assessment** | Vendor-owned | Supplier questionnaire, GAMP classification, release notes |
| **VSR** | Customer-assist | Vendor evidence summary for customer's Validation Summary Report |

### Key Features

- **Discovery mode** — point it at an existing codebase and it scans for components, requirements candidates, test coverage, and GAMP classification
- **Coached refinement** — walks through documents section by section, flagging weak requirements and missing content
- **Fast draft mode** — generates the complete package with minimal interruption when you need breadth over depth
- **Traceability engine** — automatic gap analysis with 5 gap types and 4 severity levels
- **Vendor perspective** — coaching tone frames everything as "your customer's QA team expects..." not "you must..."
- **Non-regulated mode** — works for non-pharma customers too (clean V-model docs without regulatory overhead)
- **Publish to .docx** — professional formatting with TOC, signature blocks, revision history

### Standards Coverage

- GAMP 5 (2nd Edition, 2022) with CSA alignment
- 21 CFR Part 11 / EU GMP Annex 11
- ISO/IEC/IEEE 12207
- INCOSE requirements writing / NASA forbidden words
- ISA-18.2 alarm management
- IEC 62443 (for SCADA/OT systems)

---

## Installation

### Prerequisites

- Python 3.10+
- `python-docx` for .docx publishing:
  ```bash
  pip install -r requirements.txt
  ```

### Claude Code

**Option A — Install as a skill (recommended):**

```bash
claude skill add /path/to/v-model-docs
```

Or add to your project's `.claude/skills/` directory:

```bash
# From your project root
cp -r /path/to/v-model-docs .claude/skills/v-model-docs
```

**Option B — Reference directly:**

Add to your project's `CLAUDE.md`:

```markdown
For V-model documentation tasks, use the skill at: /path/to/v-model-docs
```

### Cursor IDE

The repo includes a `.cursor/rules/v-model-docs.mdc` file. To use it:

**Option A — Clone into your project:**

```bash
# From your project root
git clone https://github.com/djbrandl/v-model-docs.git .v-model-docs

# Copy the Cursor rule
cp .v-model-docs/.cursor/rules/v-model-docs.mdc .cursor/rules/v-model-docs.mdc
```

Then update the `@` references in the `.mdc` file to point to `.v-model-docs/` paths:

```
@.v-model-docs/SKILL.md
@.v-model-docs/references/fs.md
```

**Option B — Use as a standalone project:**

Clone this repo and open it directly in Cursor. The `.cursor/rules/` directory is already configured. When generating docs, the AI will read the reference files and follow the SKILL.md orchestrator.

---

## Usage

### Start a New Project

```
"I'm building a SCADA system for a pharma customer. Help me set up V-model docs.
GAMP Category 4, 21 CFR Part 11 applies."
```

The skill will:
1. Initialize the project manifest
2. Ask clarifying questions about scope
3. Begin generating documents in dependency order

### Discover an Existing Project

```
"Scan my codebase at ./src and figure out what V-model docs we need for our
pharma customer."
```

The skill will scan your code, present a discovery report, and bootstrap the manifest.

### Generate a Specific Document

```
"Write the Functional Specification for our batch management module."
```

### Generate the Full Package

```
"Generate all the V-model docs in fast draft mode."
```

### Check Traceability

```
"Run a traceability gap analysis on my V-model docs."
```

### Publish to .docx

```
"Publish all documents to .docx."
```

### Non-Regulated Customer

```
"Set up V-model docs for a food & beverage customer — no GAMP needed,
just good documentation structure."
```

---

## Scripts

| Script | Purpose | Usage |
|---|---|---|
| `init_project.py` | Scaffold manifest and directory structure | `python scripts/init_project.py --name "My System" --description "..." --gamp-category 4 --regulatory-context 21_CFR_11,annex_11 --audience mixed` |
| `traceability_check.py` | Gap analysis engine | `python scripts/traceability_check.py --manifest docs/v-model/v-model-manifest.json` |
| `publish_docx.py` | Markdown to .docx conversion | `python scripts/publish_docx.py --input docs/v-model/fs.md --manifest docs/v-model/v-model-manifest.json --mode single` |
| `import_discovery.py` | Import playground answers into manifest | `python scripts/import_discovery.py --answers discovery-answers.json --manifest docs/v-model/v-model-manifest.json` |
| `generate_playground.py` | Interactive HTML discovery questionnaire | `python scripts/generate_playground.py --input discovery-report.json` |
| `generate_template.py` | One-off: generate the .docx template | `python scripts/generate_template.py` |

---

## Project Structure

```
v-model-docs/
├── SKILL.md                          # Orchestrator (Claude Code skill entry point)
├── README.md                         # This file
├── requirements.txt                  # Python dependencies
├── .cursor/rules/v-model-docs.mdc    # Cursor IDE rules
│
├── references/                       # Document templates and coaching guidance
│   ├── glossary.md                   # V-model, GAMP 5, FDA, ALCOA+ terms
│   ├── urs.md                        # User Requirements Specification
│   ├── fs.md                         # Functional Specification
│   ├── ds.md                         # Design Specification
│   ├── vp.md                         # Validation Plan
│   ├── risk-assessment.md            # FMEA / Risk Assessment
│   ├── iq-protocol.md                # Installation Qualification
│   ├── oq-protocol.md                # Operational Qualification
│   ├── pq-protocol.md                # Performance Qualification
│   ├── traceability-matrix.md        # Traceability Matrix
│   ├── vendor-assessment.md          # Vendor Assessment Package
│   └── vsr.md                        # Validation Summary Report
│
├── scripts/                          # Deterministic automation
│   ├── init_project.py               # Project scaffolding
│   ├── traceability_check.py         # Gap analysis engine
│   ├── publish_docx.py               # Markdown → .docx
│   ├── import_discovery.py           # Playground → manifest
│   ├── generate_playground.py        # Interactive HTML questionnaire
│   └── generate_template.py          # One-off .docx template generator
│
├── assets/
│   └── docx_template.docx            # Professional .docx template
│
└── tests/
    ├── conftest.py                   # Shared test fixtures
    └── test_scripts.py               # 86 tests for all scripts
```

---

## Testing

```bash
pip install pytest
python -m pytest tests/ -v
```

---

## License

MIT
