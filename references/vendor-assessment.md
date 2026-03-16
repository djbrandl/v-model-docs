# Vendor Assessment Package

## Purpose

The vendor assessment package provides your customer's QA team with everything they need to qualify you as a supplier. Regulated life sciences companies must demonstrate that their software vendors operate under a controlled quality system before they can use vendor-supplied software in GxP processes. This is not optional — it is a prerequisite to the customer beginning their own validation work.

This package is vendor-owned. Prepare it proactively, maintain it as a living document set, and provide it to every prospective customer during supplier qualification. A well-prepared package reduces vendor audit intensity, accelerates sales cycles, and signals validation maturity.

The customer's QA team needs to answer three questions: (1) does this vendor operate under a quality management system, (2) does this vendor's lifecycle produce software that can be validated, and (3) can we maintain a validated state when the vendor releases updates? If your package answers all three convincingly, you pass supplier qualification without a lengthy on-site audit.

### Predecessor Dependencies

None. This package describes your organization and practices, not a particular system. Prepare it once, update it periodically, reuse it across customers.

---

## Document 1: Supplier Quality Questionnaire Response

Customers send their own questionnaires, but 80% of the questions overlap. Maintain a comprehensive pre-written response and you can turn around customer questionnaires in days instead of weeks.

### Required Sections

**1.1 Company Information:** Legal entity name, headquarters address, year established, employee count (total and dev/QA), key contacts (quality lead, technical lead, support lead), regulated industries served, 2-3 named customer references in life sciences.

**1.2 Quality Management System:** Name the standard (ISO 9001, ISO 13485, or your own documented QMS). Describe structure, document control system, record retention policy (expect 10-15 years), internal audit frequency, and CAPA process for audit findings. Never write "we follow industry best practices" — auditors cannot verify that.

**1.3 Development Lifecycle:** Map your process to recognized frameworks. Explain how requirements trace to design, design traces to code, code traces to tests — regardless of whether you use Agile, V-model, or hybrid. Describe version control, branching strategy, code review process, and merge requirements.

**1.4 Change Control:** How changes are initiated, assessed for impact on validated customer environments, classified (major/minor/patch), approved, and communicated to customers before release.

**1.5 Testing Practices:** Cover unit, integration, system, and regression testing. Who writes tests, who executes them, how results are documented, pass/fail criteria. Emphasize regression — customers need assurance that new releases do not break validated functionality.

**1.6 Defect Management:** Tracking system, severity/priority classification, escalation process, and your process for notifying customers of defects discovered post-release that affect validated functionality.

**1.7 Training:** Program for development and QA staff, including GxP awareness training. How training records are maintained and how you ensure ongoing competency.

**1.8 Data Integrity and Security:** Address ALCOA+ elements (Attributable, Legible, Contemporaneous, Original, Accurate, Complete, Consistent, Enduring, Available) as they apply to your system. Cover authentication, role-based access, encryption (at rest and in transit), penetration testing frequency, and vulnerability management.

**1.9 Disaster Recovery:** Backup frequency, verification/testing schedule, RTO, RPO, geographic redundancy, and business continuity plan.

**1.10 Regulatory Experience:** Number of regulated customers, standards familiarity (GAMP 5, 21 CFR Part 11, Annex 11), audit history and outcomes, and whether you provide validation support documentation.

---

## Document 2: GAMP Category Justification

Provide a per-component classification table so customers can determine appropriate validation effort without weeks of their own analysis.

### Table Format

| Component Name | GAMP Category | Rationale | Validation Implications |
|---|---|---|---|
| Operating System | Cat 1 — Infrastructure | Industry-standard, not configured for GxP | Verify correct version installed |
| Database Engine | Cat 1 — Infrastructure | Standard platform; GxP logic resides in application layer | Verify version and configuration; backup/restore testing |
| COTS Reporting Tool | Cat 3 — Non-Configured | Used as-is, no GxP-affecting configuration | Verify installation; minimal functional testing |
| Application Platform | Cat 4 — Configured | Business rules, workflows, calculations configured per customer | Configuration verification; full IQ/OQ |
| Custom Integration | Cat 5 — Custom | Bespoke code for specific requirements | Full lifecycle docs, design review, comprehensive testing |

### Classification Guidance

- **Category 1 (Infrastructure):** Does the component execute GxP logic, or merely provide a platform? If platform, it is Category 1.
- **Category 3 (Non-Configured):** COTS products used as delivered. No configuration changes GxP-relevant behavior.
- **Category 4 (Configured):** Configuration (not custom code) determines GxP behavior. Where most commercial life sciences software falls.
- **Category 5 (Custom):** Custom-developed code. Highest validation burden — every line needs traceability from requirement to design to test.
- **Mixed-Category Products:** Break into components and classify each independently. Do not over-classify the entire system as Category 5 when only one module warrants it.

---

## Document 3: Development Lifecycle Summary

Tell the customer's QA team how you build, test, and release software, so they can assess whether your lifecycle produces output that can be validated.

### Required Sections

**3.1 Lifecycle Model:** Map your phases to V-model equivalents — requirements gathering (URS/FS input), architecture/design (DS equivalent), implementation (coding), testing (OQ/PQ equivalent), release (deployment). If Agile, explain how you maintain traceability within sprints.

**3.2 Code Review:** Who reviews, what criteria (functionality, security, test coverage), how reviews are recorded, whether reviews are mandatory for all changes.

**3.3 Version Control:** System, branching strategy, release branch protection, who can merge, how you ensure only reviewed/tested code reaches production, release tagging.

**3.4 CI/CD:** Automated checks per commit (linting, unit tests, integration tests, security scans), gates before merge, and how pipelines do not bypass quality controls. If no CI/CD, describe manual build/deploy process with equivalent controls.

**3.5 GAMP 5 Lifecycle Alignment:** Map to GAMP 5 2nd Edition phases — planning, specification, build/configuration, verification, reporting, and release management. Auditors look for this mapping explicitly.

---

## Document 4: Release Notes Template

Structured release notes bridge your development process and the customer's validated state. Every release must tell the customer what changed and whether their validation is affected.

### Template Structure

```
RELEASE NOTES — [Product Name] v[X.Y.Z] — [YYYY-MM-DD]
Classification: [Major | Minor | Patch | Hotfix]

1. SUMMARY
   [2-3 sentence overview]

2. NEW FEATURES
   - [FEAT-001] Title | Affected modules | Revalidation: Yes/No
     [Description. If yes: new functionality requires OQ test cases]

3. ENHANCEMENTS
   - [ENH-001] Title | Affected modules | Revalidation: Yes/No
     [Description. If yes: modified behavior in validated workflow]

4. BUG FIXES
   - [FIX-001] Title | Affected modules | Severity | Revalidation: Yes/No
     [What was wrong, how fixed. Yes if fix changes validated behavior;
      No if fix restores originally validated behavior]

5. KNOWN ISSUES
   - [KNOWN-001] Description | Workaround | Planned resolution

6. IMPACT ON VALIDATED STATE
   If revalidation needed: affected protocols, recommended scope,
   whether vendor provides updated protocols.
   If not: rationale and regression test confirmation.

7. UPGRADE INSTRUCTIONS
   Prerequisites, numbered steps, post-upgrade verification,
   estimated downtime.

8. ROLLBACK PROCEDURE
   Numbered revert steps, data migration reversibility,
   rollback verification.
```

---

## Document 5: Support and Maintenance Summary

Define the operational relationship after go-live: how issues are handled, how updates are delivered, and how both parties maintain the validated state.

### 5.1 Support Tiers and SLAs

| Severity | Definition | Response | Resolution Target |
|---|---|---|---|
| S1 Critical | System down or data integrity risk in GxP environment | 1 hour | 4h workaround, 24h fix |
| S2 High | Major feature unavailable, GxP workflow blocked | 2 hours | 8h workaround, 3 days fix |
| S3 Medium | Feature impaired, workaround available | 4 business hours | 5 business days |
| S4 Low | Cosmetic, enhancement request, non-GxP | 1 business day | Next scheduled release |

*Set these to your actual commitments. SLAs in a quality agreement become contractual obligations.*

### 5.2 Patch and Upgrade Cadence

- **Hotfixes:** Emergency patches for S1/S2 issues, released outside standard cadence, customers notified individually.
- **Patch releases (X.Y.Z):** Bug fixes, released on regular schedule, cumulative.
- **Minor releases (X.Y.0):** New features, include updated validation docs when validated workflows are affected.
- **Major releases (X.0.0):** Significant capabilities or architecture changes, always include updated protocols and revalidation guidance.

### 5.3 Change Communication

Pre-release notification (30 days minor, 90 days major) with draft release notes and revalidation impact assessment. Emergency notifications for critical post-release defects or security vulnerabilities. End-of-life notifications at least 12 months before version support ends.

### 5.4 Customer's Role During Upgrades

Be explicit: review release notes, schedule upgrade per their change control, execute post-upgrade verification (IQ re-execution minimum), re-execute affected OQ/PQ if revalidation indicated, update validation documentation, retain upgrade qualification evidence.

### 5.5 Emergency Fix Process

Customer reports via agreed channel, vendor acknowledges within SLA, root cause analysis communicated, fix developed and internally tested, delivered with interim release notes, customer deploys per their change control, vendor follows up with formal documentation.

---

## Quality Agreement Guidance

Most regulated customers require a quality agreement (QA/QTA) defining responsibilities for both parties.

**Typical vendor obligations:** Maintain QMS and notify of significant changes; provide change notifications before releasing updates affecting validated functionality; support customer audits with reasonable notice (define a number — 10-15 business days); notify of post-release defects affecting data integrity; maintain records per retention policy; provide validation support docs; notify before end-of-life.

**Typical customer obligations:** Maintain their own validated environment; apply updates within reasonable timeframes (especially security patches); report defects through agreed channel; conduct own PQ testing; manage own access controls.

**Typical shared obligations:** Annual quality agreement review; joint change control for hosted infrastructure changes; defined escalation paths; mutual confidentiality of audit findings.

---

## Coaching Prompts

- "Would your customer's QA team accept this package as sufficient for supplier qualification, or would they still need to schedule a full on-site audit?"
- "Could you demonstrate each claim if audited? For every statement about your QMS, testing, or change control — can you produce the record within 24 hours?"
- "Does this package reflect how your organization actually operates today, or how you intend to operate? Auditors verify current state, not roadmaps."
- "Have your quality lead and development lead both reviewed this? Disconnects between those perspectives are exactly what auditors probe."
- "For each GAMP category assignment, could you defend the classification with evidence? Auditors respect reasoned decisions more than category labels."

---

## Anti-Patterns

### 1. Vague QMS Claims
"We follow industry best practices." An auditor cannot verify that. Name the standard, describe the structure, provide evidence (certifications, audit history, procedure list).

### 2. Missing Change Control
The package describes development and testing but nothing about post-release change control. Without it, every release is a revalidation risk with no guidance. Document the full lifecycle: initiation, impact assessment, approval, implementation, verification, customer communication.

### 3. No Revalidation Guidance
Release notes list changes but do not indicate whether the customer needs to revalidate. The validation lead will either skip the upgrade or demand a call for every release. Every release note entry must include a revalidation impact statement.

### 4. SLAs Without Definitions
"24/7 support with 99.9% uptime." What counts as uptime? Scheduled maintenance excluded? What is the measurement period? Remedies for breach? Define every term.

### 5. Generic Security Statements
"We take security seriously." 21 CFR Part 11 and Annex 11 require specific technical controls. Enumerate: encryption algorithms, authentication mechanisms, access control model, audit trail implementation, penetration testing schedule.

### 6. No Deployment Model Distinction
Responsibility boundaries differ between SaaS and on-premise. Infrastructure qualification, backup responsibility, access control, and security obligations all shift. State your deployment model(s) and specify responsibility per model.

### 7. GAMP Misclassification
Claiming Category 3 for software with customer-configurable business rules. If configuration changes GxP behavior, it is Category 4 minimum. Break the system into components and classify each honestly.

---

## Override Points

- **SQQ sections:** Add or remove question categories based on customer questionnaires. The ten sections above cover the common core.
- **SLA tiers:** Adjust severity definitions and response times to match your actual support model.
- **Release cadence:** Modify to reflect your actual schedule.
- **GAMP table:** Replace example components with your actual system architecture.
- **Quality agreement terms:** Tailor to your legal and commercial framework.

---

## GAMP 5 Addenda

When regulatory context includes GAMP 5 (2nd Edition, 2022):

- **Supplier assessment is a formal GAMP 5 lifecycle activity.** Section 7 covers supplier assessment and management. Your package should map to its expectations: QMS evidence, development lifecycle evidence, support capability evidence.
- **Risk-based depth.** Assessment depth should be proportionate to GAMP category and software criticality. Category 5 custom systems warrant deeper assessment than Category 3 COTS. Provide the comprehensive version and let the customer scale back per their risk assessment.
- **CSA alignment.** Per FDA's September 2025 CSA guidance, focus shifts from documentation volume to assurance activities proportionate to risk. Demonstrate that your quality system produces reliable software, not just compliant paperwork.
