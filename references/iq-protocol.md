# IQ Protocol — Reference File

## 1. Purpose

The Installation Qualification (IQ) protocol verifies that a system has been installed correctly and that the installed configuration matches what was specified in the Design Specification (DS). It is the direct V-model mirror of the DS: every infrastructure and deployment decision documented in the DS should have a corresponding IQ verification.

**Vendor framing:** The vendor authors the IQ protocol; the customer executes it in their validated environment. The vendor's job is to make execution unambiguous — every test case must be executable by someone who did not write it, with binary pass/fail outcomes and no room for interpretation.

**Regulatory context:** GAMP 5 (2nd Edition, 2022) positions IQ as the first qualification protocol executed after installation. FDA CSA guidance (Sept 2025) allows risk-based scaling of IQ depth, but does not eliminate it. 21 CFR Part 11 and EU GMP Annex 11 both expect documented evidence that infrastructure components are installed as specified.

---

## 2. Predecessor Dependencies

| Dependency | Why Required |
|---|---|
| **Design Specification (DS)** | IQ verifies what DS specifies. Every IQ test case must trace to a DS section. Without an approved DS, IQ has no authoritative source to verify against. |
| **Validation Plan (VP)** | VP defines the overall qualification strategy, including IQ scope, acceptance criteria, and roles. IQ must align with VP-defined approach. |

**Hard rule:** Do not generate IQ content until a DS exists (at minimum in draft). If the user requests IQ without a DS, coach them to create the DS first, or offer to infer DS-equivalent content from available sources before proceeding.

---

## 3. Required Sections

Generate every IQ document with these sections. Mark sections as `[REQUIRED]` or `[RECOMMENDED]` — required sections cannot be removed via overrides.

| # | Section | Status | Content Guidance |
|---|---|---|---|
| 1 | Cover Page | `[REQUIRED]` | Document title, document ID, system name, version, author, date, approval signature block (prepared by, reviewed by, approved by, QA approval) |
| 2 | Revision History | `[REQUIRED]` | Table: version, date, author, description of changes. First row is always "1.0 — Initial release" |
| 3 | Table of Contents | `[REQUIRED]` | Auto-generated from headings |
| 4 | Purpose and Scope | `[REQUIRED]` | What is being qualified, what is excluded, regulatory drivers, reference to VP and DS |
| 5 | References | `[REQUIRED]` | DS document ID and version, VP document ID, vendor installation guide, applicable SOPs, regulatory standards |
| 6 | Definitions and Abbreviations | `[REQUIRED]` | Project-specific terms plus standard glossary references |
| 7 | Roles and Responsibilities | `[REQUIRED]` | Who executes, who reviews, who approves. RACI for IQ activities |
| 8 | Prerequisites Checklist | `[REQUIRED]` | Conditions that must be true before execution begins (see Section 6 below) |
| 9 | System Description | `[REQUIRED]` | Brief description of system under test — pulled from DS, not rewritten |
| 10 | Test Environment | `[REQUIRED]` | Target environment details: production, staging, or validation instance; network zone; access method |
| 11 | Test Cases | `[REQUIRED]` | The core of the protocol — structured verification steps (see Section 5 below) |
| 12 | Pass/Fail Criteria | `[REQUIRED]` | Overall protocol acceptance rules (see Section 7 below) |
| 13 | Deviation Log | `[REQUIRED]` | Blank template for recording deviations during execution (see Section 10 below) |
| 14 | Execution Summary | `[REQUIRED]` | Post-execution sign-off: total tests, passed, failed, deviations, overall result, signatures |
| 15 | Appendices | `[RECOMMENDED]` | Screenshots, configuration exports, license certificates, installation logs, baseline capture records |

### Override Points

- Sections 1-14 are locked. Section 15 (Appendices) can be extended or removed.
- Additional sections can be injected between sections 10 and 11 (e.g., company-specific "Environmental Monitoring" or "Clean Room Verification" sections).
- Cover page signature block roles are configurable via manifest overrides.

---

## 4. Verification Domains

IQ test cases are organized into 10 verification domains. Not every domain applies to every system — scale by GAMP category and system architecture.

| # | Domain | What It Verifies | Typical DS Source Section |
|---|---|---|---|
| 1 | **Hardware** | Server specs (CPU, RAM, disk), physical or virtual infrastructure, cloud instance types | DS infrastructure / deployment architecture |
| 2 | **Operating System** | OS version, patch level, required OS features/roles enabled | DS platform requirements |
| 3 | **Database** | DBMS type, version, instance configuration, character set, collation, allocated storage | DS data architecture |
| 4 | **Middleware** | Application server, web server, message broker, runtime versions (JRE, .NET, Node.js) | DS technology stack |
| 5 | **Application** | Software version installed, build number, file checksums, directory structure, configuration files | DS application architecture |
| 6 | **Security** | User accounts created, role assignments, password policies, encryption at rest/in transit, certificate installation | DS security architecture |
| 7 | **Network** | Firewall rules, port accessibility, DNS resolution, load balancer configuration, SSL/TLS endpoints | DS network architecture |
| 8 | **Backup** | Backup jobs configured, retention policies set, backup storage accessible, test restore capability | DS backup/recovery |
| 9 | **Documentation** | Installation guide present, release notes present, admin guide version matches, SOPs referenced | DS deliverables |
| 10 | **Environment** | Environment variables set, integration endpoints reachable, external service connectivity, time synchronization | DS deployment configuration |

### Domain Applicability by System Type

| System Type | Always Include | Include If Applicable | Rarely Needed |
|---|---|---|---|
| On-premise server | 1-10 all | — | — |
| Cloud SaaS | 5, 6, 9, 10 | 3, 4, 7, 8 | 1, 2 |
| Desktop application | 2, 5, 6, 9 | 1, 3, 10 | 4, 7, 8 |
| Embedded / instrument | 1, 2, 5, 6, 9 | 3, 8, 10 | 4, 7 |

### SaaS / Cloud Shared Responsibility Model

For SaaS products, the vendor manages infrastructure the customer cannot access or verify directly. The IQ protocol must document the responsibility boundary:

**Vendor certifies (evidence provided to customer):**
- Infrastructure qualification (servers, network, storage) — typically via SOC 2 Type II report, ISO 27001 certificate, or vendor-managed IQ summary
- Platform software versions and patch levels
- Database engine and configuration
- Backup and disaster recovery infrastructure
- Physical and network security controls

**Customer verifies (IQ test cases the customer executes):**
- Tenant configuration matches DS (application settings, workflow rules, business parameters)
- User provisioning and role assignment (RBAC matches security matrix)
- Integration endpoints reachable from customer network (SSO, API, data feeds)
- Data residency and retention settings match regulatory requirements
- Audit trail enabled and accessible

**IQ protocol framing for SaaS:** Structure the IQ with two sections — "Vendor-Certified Infrastructure" (evidence attachments, not executable test cases) and "Customer-Verified Configuration" (executable test cases). The vendor delivers both sections; the customer executes only the second.

---

## 5. Test Case Format

Every IQ test case follows a three-part structure: header, steps table, and footer.

### Header

```
Test Case ID:    IQ-{NNN}
Title:           {Concise description of what is verified}
Domain:          {One of the 10 verification domains}
DS Trace:        {DS section or requirement ID being verified}
Priority:        {Critical | Major | Minor}
Prerequisites:   {Any test-specific prerequisites beyond the protocol-level checklist}
```

### Steps Table

| Step | Action | Expected Result | Actual Result | Pass/Fail | Executed By | Date |
|---|---|---|---|---|---|---|
| 1 | {Specific, unambiguous instruction} | {Observable, measurable outcome} | {Filled during execution} | {P/F} | {Initials} | {Date} |
| 2 | ... | ... | | | | |

### Footer

```
Overall Result:  [ ] Pass  [ ] Fail
Executed By:     _________________ Date: _________
Reviewed By:     _________________ Date: _________
Comments:        {Free text for observations, screenshots referenced, deviation IDs}
```

### Test Step Writing Rules

1. **One verification per step.** Never combine "check version AND check license" into a single step.
2. **Specify the exact command or navigation path.** "Run `SELECT @@VERSION;` in SQL Server Management Studio" not "Check the database version."
3. **Expected results must be literals or ranges.** "Version 14.0.3456.2 or higher" not "correct version."
4. **No judgment calls.** The executor should never need to decide if something "looks right."
5. **Include negative space.** If something should NOT be present (e.g., default admin account disabled), state that explicitly.

---

## 6. Prerequisites Checklist

Include this 11-item checklist at the start of every IQ protocol. Items are verified before any test case execution begins.

| # | Prerequisite | Verified (Y/N) | Verified By | Date |
|---|---|---|---|---|
| 1 | Installation completed per vendor installation guide version {X.X} | | | |
| 2 | Design Specification {DS-DOC-ID} version {X.X} approved and available | | | |
| 3 | Validation Plan {VP-DOC-ID} approved and available | | | |
| 4 | Test environment matches target environment specified in DS section {X} | | | |
| 5 | All required user accounts created per DS security architecture | | | |
| 6 | Network connectivity to all required endpoints confirmed | | | |
| 7 | Backup infrastructure operational and accessible | | | |
| 8 | Execution personnel trained on IQ protocol procedures | | | |
| 9 | Blank deviation log forms available | | | |
| 10 | Screen capture / evidence collection tools available | | | |
| 11 | Previous qualification protocols (if any) completed or waived with justification | | | |

**Coaching note:** Items 1-3 are non-negotiable. Items 4-11 can be tailored — for a SaaS system, items 6-7 may be replaced with "Tenant provisioned and accessible" and "Vendor backup SLA documentation reviewed."

---

## 7. Pass/Fail Criteria Design Principles

The IQ protocol must define unambiguous pass/fail criteria at two levels:

### Test Case Level

- **Pass:** All steps within the test case have "Pass" recorded, and actual results match expected results.
- **Fail:** Any step records "Fail." A deviation must be logged immediately.

### Protocol Level

Define the overall protocol acceptance rule. Three common patterns:

| Pattern | Rule | When to Use |
|---|---|---|
| **Zero-tolerance** | All test cases must pass. Any failure blocks approval. | GAMP Cat 5 critical systems, safety-critical |
| **Deviation-tolerant** | All critical and major test cases must pass. Minor test case failures accepted with approved deviations. | GAMP Cat 4 most systems |
| **Risk-based** | All critical test cases must pass. Major and minor failures accepted with approved deviations and impact assessment. | GAMP Cat 3 infrastructure |

### Design Principles

1. **Pre-define the pattern.** Never decide the acceptance rule after seeing results.
2. **Tie to priority classification.** Every test case must have a priority (Critical/Major/Minor) assigned before execution.
3. **Require deviation closure.** No protocol can be approved with open deviations — they must be resolved, accepted-with-justification, or deferred-to-next-release with documented risk assessment.
4. **Separate "protocol pass" from "system release."** IQ approval is one input to the release decision, not the release decision itself.

---

## 8. GAMP-Scaled Depth

IQ depth scales with GAMP 5 software category. The differences are in volume, evidence rigor, and verification method — not in structure.

### Test Case Count Ranges

| GAMP Category | Test Case Range | Rationale |
|---|---|---|
| **Category 3** (non-configured) | 5-15 | Infrastructure-only. Verify installation matches vendor spec. No configuration to test. |
| **Category 4** (configured) | 15-40 | Infrastructure plus configuration verification. Each configurable parameter is a test candidate. |
| **Category 5** (custom) | 30-100+ | Infrastructure, configuration, and custom deployment artifacts. Custom scripts, integrations, and build verification. |

### Scaling Differences by Category

| Dimension | Cat 3 | Cat 4 | Cat 5 |
|---|---|---|---|
| **Verification method** | Visual confirmation, version checks | Visual + configuration export comparison | Visual + config export + checksum + automated script output |
| **Evidence type** | Screenshots | Screenshots + config file copies | Screenshots + config files + build logs + checksum reports |
| **Security depth** | Account existence | Account + role assignment + permission matrix | Account + role + permission + penetration test evidence |
| **Database checks** | Version only | Version + instance config + schema presence | Version + config + schema + stored procedures + seed data |
| **Network checks** | Port accessibility | Port + firewall rule export | Port + firewall + load balancer config + SSL certificate chain |
| **Backup verification** | Job configured | Job configured + test backup | Job + test backup + test restore + retention validation |
| **Documentation** | Release notes present | Release notes + admin guide | Release notes + admin guide + API docs + deployment runbook |
| **Pass/fail pattern** | Risk-based | Deviation-tolerant | Zero-tolerance (critical), deviation-tolerant (major/minor) |

### Category 3 Specific Guidance

For COTS infrastructure (Cat 3), IQ may be the only qualification protocol the vendor provides. Focus on:
- Correct version installed
- License valid
- Default security hardened (default passwords changed, unnecessary services disabled)
- Vendor-recommended configuration applied

### Category 5 Specific Guidance

For custom applications (Cat 5), IQ must also verify:
- Build artifacts match the released build (checksum verification)
- Custom configuration files deployed correctly
- Database migration scripts executed successfully
- Integration endpoints configured for the target environment
- Custom scheduled jobs / background services registered and configured

---

## 9. Example Test Cases

### Example 1: Application Version Verification

**Header:** `IQ-001 | Domain: Application | DS Trace: DS-4.2.1 | Priority: Critical`

| Step | Action | Expected Result |
|---|---|---|
| 1 | Log in to the application as an administrator | Login successful |
| 2 | Navigate to Help > About (or Settings > System Information) | System info page displayed |
| 3 | Record the displayed application version number | Version is {X.Y.Z} per DS-4.2.1 |
| 4 | Record the displayed build number | Build is {BUILD} per DS-4.2.1 |

Each step also has columns for Actual Result, Pass/Fail, Executed By, and Date (omitted here for brevity). Footer includes Overall Result checkboxes, Executed By / Reviewed By signature lines, and Comments.

### Example 2: License Verification

**Header:** `IQ-005 | Domain: Application | DS Trace: DS-4.3.1 | Priority: Critical`

| Step | Action | Expected Result |
|---|---|---|
| 1 | Navigate to license management (Settings > License) | License info displayed |
| 2 | Record the license type | Type is "{Enterprise/Professional}" per DS-4.3.1 |
| 3 | Record the license expiration date | On or after {YYYY-MM-DD} |
| 4 | Record the licensed user/seat count | Capacity is {N} per DS-4.3.1 |
| 5 | Verify no license warnings or errors displayed | No warning banners, errors, or "trial mode" indicators |

### Example 3: Access Control Verification

**Header:** `IQ-012 | Domain: Security | DS Trace: DS-6.1 | Priority: Critical`

| Step | Action | Expected Result |
|---|---|---|
| 1 | Navigate to user management (Admin > Users) | User list displayed |
| 2 | Verify each account in DS-6.1 Table 3 exists | All DS-specified accounts present |
| 3 | Select first user and view assigned roles | Role matches DS-6.1 Table 3 |
| 4 | Attempt login with default admin credentials | Login fails (default password changed) |
| 5 | Verify no unexpected accounts beyond DS-6.1 | No extra accounts beyond DS-specified and system/service accounts |

### Security Architecture Verification (IEC 62443)

For OT/SCADA/ICS systems where the DS includes IEC 62443 security architecture, the following IQ test cases verify that the installed security controls match the DS zone/conduit model. Include these test cases when `regulatory_context` includes IEC 62443 or the system type is OT/SCADA/ICS.

**IQ-SEC-001: Zone Boundary Verification**

**Header:** `IQ-SEC-001 | Domain: Network + Security | DS Trace: DS Security Architecture (Zone/Conduit Model) | Priority: Critical`

| Step | Action | Expected Result |
|---|---|---|
| 1 | Document the installed zone topology by capturing network diagrams, VLAN assignments, and firewall zone definitions | Zone topology matches DS zone/conduit design |
| 2 | Export firewall rules for each zone boundary and compare against DS-specified allowed communication paths | Firewall rules enforce zone boundaries per DS |
| 3 | Attempt cross-zone communication not specified in the DS (e.g., ping or connection attempt from enterprise zone to process control zone on non-permitted port) | Unauthorized cross-zone traffic is blocked |
| 4 | Verify that blocked cross-zone attempts are logged by the firewall or network monitoring system | Rejected cross-zone traffic is logged with source, destination, port, and timestamp |

**IQ-SEC-002: Security Level Verification**

**Header:** `IQ-SEC-002 | Domain: Security | DS Trace: DS Security Architecture (Security Level Targets) | Priority: Critical`

| Step | Action | Expected Result |
|---|---|---|
| 1 | For each zone, verify the authentication mechanism matches the target Security Level (SL-T): SL1 — single-factor; SL2 — multi-factor; SL3 — multi-factor + certificate; SL4 — multi-factor + hardware token | Authentication mechanism meets or exceeds SL-T per DS |
| 2 | For each zone, verify authorization granularity matches SL-T requirements (role-based, attribute-based, or individual permissions) | Authorization granularity meets or exceeds SL-T per DS |
| 3 | For each zone, verify audit logging depth matches SL-T requirements (event types logged, log retention, log protection) | Audit logging depth meets or exceeds SL-T per DS |
| 4 | For each zone, verify encryption at rest and in transit matches SL-T requirements | Encryption controls meet or exceed SL-T per DS |

**IQ-SEC-003: Conduit Protection Verification**

**Header:** `IQ-SEC-003 | Domain: Network + Security | DS Trace: DS Interface Inventory Matrix | Priority: Critical`

| Step | Action | Expected Result |
|---|---|---|
| 1 | For each cross-zone conduit defined in the DS Interface Inventory Matrix, verify protocol restrictions are enforced (only permitted protocols/ports allowed) | Protocol restrictions match DS specifications |
| 2 | Verify encryption is enabled on each conduit as specified in the DS | Conduit encryption matches DS specifications |
| 3 | Verify authentication is required for each conduit endpoint as specified in the DS | Conduit authentication matches DS specifications |
| 4 | Verify data integrity checks are configured for each conduit as specified in the DS | Data integrity controls match DS specifications |
| 5 | Verify logging is enabled for each conduit as specified in the DS | Conduit activity logging matches DS specifications |

**IQ-SEC-004: OT-Specific Access Control**

**Header:** `IQ-SEC-004 | Domain: Security | DS Trace: DS Security Architecture (OT Access Controls) | Priority: Critical`

| Step | Action | Expected Result |
|---|---|---|
| 1 | Verify remote access to the OT environment is disabled or secured per DS specifications (VPN, jump host, or equivalent) | Remote access controls match DS security design |
| 2 | Verify USB/portable media controls are configured per DS (disabled, whitelisted, or monitored) | Portable media controls match DS security design |
| 3 | Verify wireless access controls are configured per DS (disabled, WPA3, 802.1X, or equivalent) | Wireless access controls match DS security design |
| 4 | Verify physical access logging is configured per DS (if applicable — badge reader logs, camera system, access log) | Physical access logging matches DS security design (if applicable) |

### EU GMP Annex 11 IQ Considerations

For systems subject to EU GMP regulations, the IQ protocol must address the following Annex 11 clauses. These considerations ensure that the IQ evidence package supports Annex 11 compliance from the first qualification stage.

**Clause 3 (Supplier/Service Provider):** IQ should verify that the installed system matches the vendor's specifications — version numbers, configuration files, and build checksums must match the Vendor Assessment deliverables. Record the vendor name, product version, and build identifier verified during IQ and cross-reference against the Vendor Assessment documentation.

**Clause 4 (Validation):** IQ is the first qualification stage in the Annex 11 validation lifecycle — IQ evidence feeds into the Validation Summary Report. Ensure the IQ protocol's document ID, execution date, and outcome are structured to roll up into the VSR.

**Clause 7.1 (Data Protection):** IQ must verify backup configuration — backup jobs scheduled, retention periods configured, restore capability verified. At minimum, verify that a backup job exists, runs on the DS-specified schedule, targets the DS-specified storage, and that a test restore produces a usable system state.

**Clause 10 (Change and Configuration Management):** IQ must verify the installed configuration baseline — all configurable settings documented, checksums recorded, configuration management tool (if any) operational. This directly supports the Post-IQ Baseline Capture (Section 11) and provides the foundation for ongoing change control.

**Clause 12 (Security):** IQ must verify security controls are installed correctly — user accounts configured per DS RBAC design, password policies enforced, session timeouts configured, failed login lockout configured. Each security control specified in the DS must have a corresponding IQ verification step with a binary pass/fail outcome.

**Clause 16 (Business Continuity):** IQ must verify BC/DR infrastructure is in place — failover mechanisms configured, DR site reachable, monitoring alerts configured. Verify that the DR infrastructure exists and is reachable; functional DR testing (actual failover and recovery) is an OQ activity.

> **Note:** IQ verifies that the system is INSTALLED correctly per the Design Specification. Annex 11 compliance at IQ focuses on infrastructure, configuration, and security foundations. Functional compliance (Clauses 5, 9, 14) is verified during OQ.

---

## 10. Deviation Handling

When a test step fails, a deviation is recorded immediately. The following 10-step process governs deviation lifecycle:

1. **Detect** — Tester records "Fail" in the actual result column and stops the test case.
2. **Log** — Tester opens a new row in the deviation log (format below).
3. **Classify** — Tester assigns initial severity: Critical / Major / Minor.
4. **Notify** — Tester notifies the IQ lead and QA representative per protocol roles.
5. **Investigate** — IQ lead and vendor (if applicable) determine root cause.
6. **Impact Assess** — Determine impact on other test cases, system functionality, and data integrity.
7. **Resolve** — Implement corrective action (fix, reconfigure, accept-with-justification).
8. **Re-test** — Execute the failed test case from step 1 after correction. Record in a new execution column.
9. **Close** — QA reviews deviation record, confirms resolution is adequate, signs off.
10. **Summarize** — Include deviation in the Execution Summary with final disposition.

### Deviation Log Format

| Field | Description |
|---|---|
| Deviation ID | DEV-IQ-{NNN} (sequential within this protocol execution) |
| Test Case ID | The IQ test case that failed |
| Step Number | The specific step that failed |
| Date Detected | Date of failure observation |
| Detected By | Name and role of tester |
| Description | What happened vs. what was expected — factual, no interpretation |
| Severity | Critical / Major / Minor |
| Root Cause | Category: installation error / configuration error / environmental issue / specification error / vendor defect |
| Corrective Action | What was done to resolve |
| Re-test Result | Pass / Fail after correction (with date and tester) |
| Impact Assessment | Effect on other test cases and system functionality |
| Closed By | QA reviewer name, signature, and date |

### Deviation Severity Definitions

| Severity | Definition | Protocol Impact |
|---|---|---|
| **Critical** | System cannot function as intended; data integrity at risk; regulatory requirement unmet | Protocol execution halted until resolved |
| **Major** | Significant functionality affected but workaround exists; non-critical regulatory gap | Protocol execution may continue for unrelated test cases |
| **Minor** | Cosmetic issue, documentation discrepancy, non-functional deviation | Protocol execution continues; deviation resolved before approval |

---

## 11. Post-IQ Baseline Capture

After all IQ test cases pass (or deviations are resolved), capture a verified baseline of the installed system. This baseline serves as the reference point for change control — any future modification is compared against it.

### Baseline Artifacts

| Artifact | Capture Method | Storage |
|---|---|---|
| Application version and build | Screenshot or system info export | Appended to IQ protocol as appendix |
| Configuration file snapshots | File copy with checksums (SHA-256) | Archived in validation evidence repository |
| Database schema export | Schema comparison tool output or DDL export | Archived with IQ evidence |
| User account and role list | Admin panel export or query output | Appended to IQ protocol |
| Network configuration snapshot | Firewall rule export, DNS records | Archived with IQ evidence |
| Installed component inventory | Package list / dependency manifest | Archived with IQ evidence |
| Backup configuration | Backup job definition export | Archived with IQ evidence |
| Environment variable snapshot | Sanitized export (no secrets) | Archived with IQ evidence |

### Baseline Rules

1. **Capture immediately after IQ approval.** Not before (system may change during deviation resolution), not days later.
2. **Checksum everything.** Every captured file gets a SHA-256 hash recorded in the baseline manifest.
3. **Sanitize secrets.** Passwords, API keys, and connection strings are replaced with `[REDACTED]` in captured artifacts. Note which fields were redacted.
4. **Version the baseline.** Baseline is tagged with the IQ protocol execution ID and date. Future IQ executions create new baselines.
5. **Customer owns the baseline.** The vendor provides the capture procedure; the customer stores and maintains the baseline in their document management system.

---

## 12. Coaching Questions

Use these questions during Phase 2 (Coached Refinement) to strengthen the IQ protocol before finalization.

### Completeness

- "Does every section of the DS have at least one corresponding IQ test case? Let's walk through the DS table of contents and check."
- "Are there any infrastructure components mentioned in the FS or VP that aren't covered in the DS — and therefore missing from IQ?"
- "For cloud-hosted systems: which verification domains are the vendor's responsibility vs. the customer's? Are the boundaries documented?"

### Executability

- "Could a qualified tester who has never seen this system execute every test case without calling the vendor? If not, which steps need more detail?"
- "Are there any expected results that use relative terms like 'appropriate,' 'sufficient,' or 'as expected'? These must be replaced with measurable criteria."
- "Do test cases specify the exact navigation path, command, or query — or do they assume the executor knows the system?"

### Traceability

- "Every IQ test case must trace to a DS section. Are there any test cases that verify something not documented in the DS? If so, the DS needs updating."
- "Are there DS sections with no corresponding IQ test case? Either they don't need verification (document why) or test cases are missing."

### Risk Alignment

- "Are critical test cases actually testing critical functionality? Walk through each 'Critical' test case and confirm it maps to a risk-assessed DS requirement."
- "Is the pass/fail pattern (zero-tolerance, deviation-tolerant, risk-based) appropriate for this system's GAMP category?"

### Evidence Sufficiency

- "For each test case, is the evidence type sufficient? An auditor will ask to see proof — is a screenshot enough, or do you need a configuration export?"
- "Are baseline capture procedures defined? After IQ passes, how will the customer prove the system hasn't changed?"

---

## 13. Anti-Patterns

The reviewer agent checks for these common IQ mistakes. Each anti-pattern includes what's wrong and how to fix it.

| # | Anti-Pattern | What's Wrong | Fix |
|---|---|---|---|
| 1 | **Vague expected results** | "System is configured correctly" — not verifiable | Replace with literal values: "Version is 14.0.3456.2" |
| 2 | **Multi-verification steps** | One step checks version AND license AND config | Split into one verification per step |
| 3 | **Missing DS trace** | Test cases with no `DS Trace` field or "N/A" trace | Every IQ test case must trace to DS. If it can't, question whether the test belongs in IQ |
| 4 | **Copy-paste from DS** | DS content pasted into IQ without converting to testable steps | DS describes what should be; IQ describes how to verify it. Transform specifications into actions |
| 5 | **No negative testing** | Only verifies things are present, never that wrong things are absent | Add checks: default accounts disabled, test data removed, debug modes off |
| 6 | **Screenshot-only evidence for configs** | Screenshots of config screens can be fabricated and are hard to diff | Supplement screenshots with configuration exports or command-line output |
| 7 | **Protocol-level pass/fail undefined** | Individual test cases have pass/fail but no overall acceptance rule | Define the protocol-level acceptance pattern (Section 7) before execution |
| 8 | **No baseline capture** | IQ passes but no record of installed state for change control | Add Post-IQ Baseline Capture section (Section 11) |
| 9 | **Mixing IQ and OQ** | Test cases verify functionality ("user can log in and create a record") instead of installation ("user account exists with correct role") | IQ verifies installation state, not operational behavior. Move functional tests to OQ |
| 10 | **Orphan domains** | Including all 10 domains for a SaaS system where hardware/OS are irrelevant | Scale domains to system type using the applicability table in Section 4 |
| 11 | **Undated/unsigned execution records** | Steps executed but no initials, dates, or reviewer signatures | Every step requires executed-by and date; every test case requires reviewer sign-off |
| 12 | **Deviation-free claim on first attempt** | Zero deviations across 50+ test cases raises auditor suspicion | Not necessarily wrong, but document why — e.g., "pre-IQ dry run conducted on {date}" |
