# Governance and Assurance Registers

These registers instantiate the missing Appendices A-E referenced by the brief. They are proposed controls, not evidence that SRG has adopted them. Role holders are existing job titles; the brief provides no named employees.

## Assumptions Register

| ID | Assumption / decision | Rationale | Validation owner | Revisit trigger |
| --- | --- | --- | --- | --- |
| A-01 | Only the brief PDF was available; supplied datasets, detailed templates, and broken-job log were absent. | Prevents synthetic artifacts being passed off as instructor evidence. | Student / lecturer | Obtain source package. |
| A-02 | Demo data are synthetic with seed 20261004 and dates Jan-Jun 2025. | Enables reproducible code and dashboard tests. | Analytics lead | Replace with supplied data. |
| A-03 | “Five transactional sources” means store POS (23 instances treated as one logical source), e-commerce, loyalty, Odoo inventory, and mobile-money transaction/settlement files. CRM is a governed reference/enrichment source. | Brief lists more than five platforms and does not name the exact five. | Data Governance Council | Confirm source inventory with owners. |
| A-04 | The UGX 480M figure is treated as the total cap for the 18-month D1 plan, although scenario also calls it an annual budget. | More conservative and consistent with D1's explicit envelope wording. | CFO / Board | Written budget interpretation. |
| A-05 | Fixed FX values in the demo are planning-only: UGX 1, KES 28.5, RWF 2.85. | Demo must not sum mixed denominations without conversion. | Finance owner | Replace with approved effective-dated rates. |
| A-06 | DPPA applies to Uganda operations; GDPR applicability to the EU relationship is assessed by establishment, targeting, processing, and contract, not presumed. | Partnership requirement alone does not establish every GDPR territorial trigger. | Privacy owner / counsel | EU data-flow and contract review. |
| A-07 | CCPA/CPRA is comparative only unless SRG's US nexus and statutory thresholds are established. | The scenario does not establish California operations or thresholds. | Privacy owner / counsel | US customer or business expansion. |
| A-08 | Store-edge POS remains operational during outages; customer IDs created offline are provisional, not golden. | Preserve sales continuity and avoid ignoring connectivity. | Retail IT lead | Pilot outage/replay results. |
| A-09 | A customer may hold more than one program account; a household relation is optional and many-to-many, never inferred solely from address. | Avoid collapsing individual identity and loyalty history. | Customer data owner | Customer research and program rules. |
| A-10 | Sales extract alone cannot explain 8.4% physical-stock variance. Inventory snapshots, receipts, transfers, counts, adjustments, and outage logs are required. | The brief gives a variance but no root-cause evidence. | Inventory owner | Obtain full movement/count data. |
| A-11 | Demo measures are descriptive; no margin, consent, stock-on-hand, cost, reliable customer activity history, or payment-event timestamps are available. | Limits the claims and recommendations a prototype dashboard can make. | CFO / analytics owner | Supply governed subject-area data. |
| A-12 | Static dashboard hosting is a deployable demonstration, but the brief names Power BI or Tableau Public. | InfinityFree hosting was requested by the user; rubric acceptance is unconfirmed. | Student / lecturer | Confirm platform requirement before final submission. |
| A-13 | Demo HR workbook includes synthetic identifiers and salary amounts only to demonstrate classification/masking. | No real employee data provided. | HR owner | Replace only in restricted environment. |

## Governance Charter

**Vision:** SRG's critical data is understood, protected, consistently defined, and fit for the decisions that run retail operations.

**Scope:** customer, product, supplier, store, order/sales, inventory, payment, HR, metadata, quality, security, and analytics across 23 stores, digital channels, HQ, and contracted processors.

**Principles:** business ownership; minimum necessary collection; purpose limitation; capture quality at source; reusable enterprise IDs; local continuity with controlled synchronization; least privilege; measurable controls; reversible merges; evidence-led investment; no real-time processing without a latency-driven business case.

**Decision cadence:** 45-minute monthly Data Governance Council, chaired by the Head of IT; urgent privacy incidents bypass the monthly cadence and escalate immediately. Each domain owner approves definitions/rules; stewards resolve routine exceptions; material conflicts go to the Council. No new governance hires are assumed.

### Operating roles (existing job titles)

| Role | SRG position | Accountability |
| --- | --- | --- |
| Executive sponsor | CFO | Budget, risk acceptance, cross-functional escalation. |
| Council chair / platform owner | Head of IT | Standards, access, architecture, issue escalation. |
| Customer data owner | Head of Marketing / CRM lead | Customer purpose, consent, survivorship, quality. |
| Product and supplier owner | Procurement Manager | Product taxonomy, SKU and supplier master. |
| Sales/payment owner | Finance Manager | Revenue definitions, tender mapping, settlement reconciliation. |
| Inventory/store owner | Head of Retail Operations | Stock movement controls, cycle counts, store adoption. |
| Workforce-data owner | HR Manager | HR classification, lawful access, retention. |
| Privacy coordinator | Existing Legal/Compliance Officer (or named management delegate) | PDPO liaison, rights requests, DPIA and breach register. |
| Data stewards | Nominated CRM, procurement, finance, and store-supervisor staff | Queue triage, evidence capture, approved corrections. |
| Technical custodian | IT analyst assigned by Head of IT | Pipelines, backups, encryption, logs, role provisioning. |

If SRG has no Legal/Compliance Officer, the CFO appoints an existing senior manager as interim privacy coordinator and records the capacity limitation; this proposal does not create a sixth hire.

### RACI (A=accountable, R=responsible, C=consulted, I=informed)

| Activity | CFO | Head IT | Domain owner | Steward | Privacy coord. | Store manager |
| --- | --- | --- | --- | --- | --- | --- |
| Customer record creation | I | C | A | C | C | R |
| Customer master merge / unmerge | I | C | A | R | C | I |
| New customer attribute approval | I | C | A | R | C | I |
| Product/SKU creation | I | C | A | R | I | C |
| Data-quality rule change | I | R | A | C | C | C |
| Warehouse KPI definition | C | R | A | C | I | C |
| Role/access approval | I | R | A | I | C | I |
| HR data disclosure | I | C | A | I | C | I |
| Retention schedule approval | C | C | A | R | R | I |
| Retention/deletion execution | I | R | A | C | C | I |
| Data-subject rights request | I | C | C | R | A | I |
| Suspected breach escalation | I | R | C | I | A | R |
| Breach declaration / PDPO notice | A | C | C | I | R | I |
| Pipeline failure / replay | I | A/R | C | C | I | I |
| Physical inventory count approval | I | C | A | C | I | R |

## Enforceable Policy Requirements

### 1. Data Access and Classification

- **Owner:** Head of IT; data owners approve access to their domains; privacy coordinator reviews restricted personal data.
- Classify each dataset Public, Internal, Confidential, or Restricted before production use. Names plus purchase history, phone, email, national ID, payroll, and payment references are Confidential or Restricted as specified in the dictionary.
- Grant named accounts through role groups; prohibit shared user accounts. Analysts receive masked or aggregated views by default. HR direct identifiers and exact salary are denied to the analytics role.
- Require MFA for cloud/SaaS administrators, encryption at rest for laptops and removable media, TLS in transit, and centrally recoverable keys. No customer export may be stored unencrypted on an endpoint or personal device.
- Review privileged access monthly and all other access quarterly; remove leavers within one business day. Log exports and access to Restricted fields; alert on bulk extraction.
- **Enforcement:** IT disables non-compliant exports, revokes role membership, records approved exceptions with expiry, and reports overdue access reviews to the Council monthly.

### 2. Data Quality

- **Owner:** relevant domain owner; stewards operate the exception queues.
- Apply `docs/validation_rules.csv` at capture and again before warehouse publication. Required quality gates: 100% valid source keys; at least 99.5% fact-to-dimension resolution; unsupported currency count = 0; all failed rows quarantined; payment-reference exception below 1% per mobile-money provider pending Finance baseline approval.
- Publish weekly domain scorecards for uniqueness, completeness, consistency, timeliness, validity, and accuracy evidence/proxy. Every breach has a named owner, due date, root-cause code, and remediation status.
- **Enforcement:** reject or quarantine invalid inputs; do not publish a failed partition; repeated source failures trigger owner escalation and a change request, not a silent manual override.

### 3. Retention and Deletion

- **Owner:** domain owner; privacy coordinator maintains the schedule; IT executes deletion and evidence capture.
- Approve a purpose-specific schedule before collection. Legal holds suspend deletion only for documented cases. Customer profiles are reviewed after 24 months of inactivity; deletion/anonymization timing must be reconciled with tax, consumer, and contract retention duties before adoption. Transactional financial records follow Finance-approved statutory schedules; HR records follow employment/legal schedules.
- Process verified correction/deletion requests through a tracked ticket; search source systems, MDM crosswalks, caches, exports, backups, and processors. Propagate suppression/deletion while retaining only a minimal audit tombstone where legally permitted.
- **Enforcement:** monthly overdue-item report to owners; quarterly sample proves execution; failed deletion is a Council exception and privacy incident review.

## Compliance Obligations and Gap Register

The legal references below are a research starting point, not a substitute for counsel checking the current Act, regulations, PDPO guidance, and cross-border contracts.

| Priority | Obligation / reference | Current evidence from brief | Gap and required action | Owner / target |
| --- | --- | --- | --- | --- |
| Critical | Uganda DPPA 2019 s.7: consent/conditions for collection or processing | Customer data used across POS, loyalty, CRM; no purpose/consent evidence supplied | Inventory purposes and legal conditions; separate service processing from optional marketing; keep consent event, notice version, withdrawal and objection. | Privacy coordinator, M3 |
| Critical | Uganda DPPA s.23: notification of data-security breach | Unencrypted 9,000-row export stolen; internal report 11 days late; no notification | Immediate internal escalation and prompt PDPO notification on reasonable belief; preserve timeline and follow PDPO direction on affected-person notice. | Privacy coordinator, immediate |
| Critical | Uganda DPPA s.29: registration obligations | Scenario says PDPO registration applies; status unknown | Confirm controller/processor registrations, renewals, and processor arrangements; keep proof. | Privacy coordinator, M2 |
| High | Uganda DPPA s.16: correction/deletion rights | Duplicate profiles and incorrect loyalty allocation | Rights-request workflow, identity verification, correction propagation, deletion record and response tracking. | Customer owner, M4 |
| High | Uganda DPPA s.19: transfer outside Uganda | EU distributor partnership / cloud SaaS possible | Map data locations and subprocessors; verify destination safeguards and consent/other statutory requirements before transfer. | Privacy coordinator, before EU flow |
| High | GDPR Arts. 5, 6, 7, 12-22, 25, 28, 32, 33-35, 44-49 (only if territorial trigger/contract applies) | EU partner requests GDPR-equivalent practice; applicability untested | Complete territorial-scope and controller/processor assessment, lawful-basis matrix, rights handling, processor clauses, security, DPIA, 72-hour supervisory notice process, high-risk subject communication, and transfer mechanism. | Counsel/privacy coordinator, M6 |
| Medium | CCPA/CPRA comparative: Cal. Civ. Code §§1798.100, .105, .110, .115, .120, .135, .140; applicability depends on California nexus and thresholds | No California activity described | Use as comparison only; do not claim binding obligation without applicability assessment. Map notice, access/delete/correct, opt-out, sensitive PI and vendor terms if triggered. | Privacy coordinator, annual review |
| High | Uganda DPPA security safeguards / accountability duties; GDPR Art. 32 benchmark where applicable | Laptop export unencrypted, weak escalation; control evidence absent | Full-disk encryption, managed devices, least privilege, export restrictions, incident drills, vendor inventory, and evidence. Confirm exact Uganda regulation provisions with counsel. | Head IT, M1-M3 |

**Breach response sequence:** (1) employee reports immediately to manager and IT/security hotline; (2) incident lead timestamps, preserves evidence, isolates device/accounts and stops further disclosure; (3) privacy coordinator assesses data types, people, access/encryption, likely harm, processors and jurisdictions; (4) notify PDPO promptly under DPPA s.23 on reasonable belief and follow its decision/direction for data-subject communications; (5) if GDPR applies, controller notifies the competent supervisory authority within 72 hours of awareness unless risk is unlikely, and informs affected subjects without undue delay where high risk; (6) notify contractual partners/processors as required; (7) document decisions, remediation, and lessons. Uganda's statutory wording is not replaced by GDPR's 72-hour clock.

## Risk Register

Scale: likelihood and impact 1-5; inherent score = L x I. Residual score is an estimate after controls and must be recalibrated from incidents and audit results.

| ID | Risk | L | I | Inherent | Mitigation | Residual |
| --- | --- | ---: | ---: | ---: | --- | ---: |
| R1 | Unencrypted endpoint/export loss exposes customer history | 4 | 5 | 20 | Managed-device encryption, export approval, DLP, remote revoke, drills | 8 |
| R2 | Breach is reported late or not escalated | 4 | 5 | 20 | 24/7 named contact, 1-hour internal SLA, escalation tree, tabletop | 8 |
| R3 | False customer merge transfers loyalty/personal history | 3 | 5 | 15 | Conservative matching, manual review, reversible links, audit | 6 |
| R4 | Offline POS sync loses or duplicates transactions | 4 | 4 | 16 | Durable encrypted outbox, idempotency keys, watermark/count reconciliation | 8 |
| R5 | Product-ID/unit mismatch distorts stock and sales | 4 | 4 | 16 | MDM alias crosswalk, controlled units, owner approval | 6 |
| R6 | Stock variance continues unnoticed | 4 | 4 | 16 | Cycle-count fact, threshold alerts, movement reason/approval, recount | 8 |
| R7 | Analysts expose HR/customer restricted fields | 3 | 5 | 15 | Column grants, masked views, quarterly role review, access tests | 5 |
| R8 | Cross-border transfer breaches Uganda/GDPR conditions | 3 | 5 | 15 | Flow inventory, legal review, processor terms, transfer safeguards | 6 |
| R9 | ETL reports success after partial load | 4 | 4 | 16 | Atomic publish, row/amount gates, quarantine, alert on partial state | 4 |
| R10 | Vendor outage/price change exceeds small-team capacity/budget | 3 | 4 | 12 | Cost alerts, exit/export plan, capped pilot, managed-service review | 6 |
| R11 | Footfall analytics becomes identifiable surveillance | 2 | 5 | 10 | Aggregate at edge, no image/device ID retention, notice and DPIA | 4 |
| R12 | Team cannot operate complex platform | 4 | 4 | 16 | Managed PostgreSQL/batch, runbooks, training, staged scope, support SLA | 8 |

## DPIA | Loyalty App EU-facing Rollout (Draft)

**Processing:** loyalty account registration, purchase/points history, optional marketing preferences, support and fraud prevention. **People:** Uganda, Kenya, Rwanda, and potentially EU-resident customers reached by the service. **Controller/processor roles:** SRG is likely controller for its purposes; cloud/app vendors may be processors, subject to contract and actual purpose.

**Purpose and necessity:** administer membership and points; fulfill purchases; optional direct marketing only under a separately recorded legal basis/preferences. Do not collect full payment credentials or precise location for basic points. Match customer records only when needed to prevent points misallocation and provide service.

**Data:** contact identifiers, loyalty ID, transaction references, preferences, and coarse location/district. Special-category data should not be collected for the stated purpose. Footfall events stay aggregate and are not linked to loyalty IDs.

**Risks:** false identity merge; excessive marketing; unauthorized export; stolen/offline device; processor or cross-border exposure; rights/deletion propagation failure; profiling bias; sensor re-identification. **Controls:** opt-in purpose separation, clear notice, reversible MDM links, role-based access, masked analytics, encrypted endpoints/transit/storage, processor contracts, access logs, retention schedule, rights queue, data minimization, and no person-level footfall join.

**International flows:** list storage, support, backups, analytics and subprocessors; determine Uganda DPPA s.19 transfer conditions and GDPR Arts. 44-49 if applicable before launch. **Consultation:** privacy coordinator, customer owner, IT, EU partner, processor, and affected-customer representatives. **Residual risk:** medium until legal transfer and consent evidence are verified. **Decision:** do not enable EU-facing loyalty processing until high risks have owners, transfer mechanism, customer notices, breach contacts, and a tested rights workflow. Review after pilot and annually.

## Decision Log (8+ required entries)

| ID | Decision and alternatives | Evidence / criteria | Choice | What would change the decision? |
| --- | --- | --- | --- | --- |
| D-01 | Hub-and-spoke vs centralized, federated, decentralized | 23 stores, hours-long outages, 4 IT staff, budget; connectivity and run cost weighted highest | Hub-and-spoke with durable store outbox | Stable connectivity plus a lower-cost managed central platform and tested latency. |
| D-02 | Coexistence MDM vs registry, consolidation, centralized | Operational systems cannot be replaced in 18 months | Coexistence with golden IDs and source crosswalk | Source APIs and field ownership mature enough for consolidation. |
| D-03 | Batch vs real-time everything | Board reporting is monthly; inventory/payment signals have localized latency value | Batch analytics; pilot selected CDC/stream use cases | Measured loss or fraud cost proves shorter latency has positive ROI. |
| D-04 | Auto-merge threshold | False merge can misallocate points and expose another person's data | Exact-key auto-link only; fuzzy score >=95 with strong phone evidence and no conflicts; 75-94 steward review; below 75 remain separate | Reviewed precision/recall sample and appeal rate. |
| D-05 | Warehouse normalization vs star schema | Operational integrity vs dashboard scan speed | Normalized operational core; star schema analytical copy | Query performance or write contention measured in pilot. |
| D-06 | Static demo host vs Power BI/Tableau | User asks InfinityFree; brief specifically names Power BI/Tableau Public | Build portable static dashboard; obtain lecturer approval or publish a compliant BI copy | Lecturer confirms host/platform acceptance or institution provides a BI tenant. |
| D-07 | Open-source catalog vs commercial catalog | Four-person IT team and UGX cap | Begin with versioned dictionary/lineage in repo; pilot low-admin open-source only if operational owner exists | Costed vendor proof-of-concept shows reduced total ownership cost. |
| D-08 | Accuracy metric | No independent ground-truth records were supplied | Report structural plausibility proxy and mark factual accuracy unverified | Trusted source-of-truth sample or audited reference data. |
| D-09 | Total 18-month spend | Annual budget phrasing conflicts with D1's 480M envelope | Cap the full roadmap at UGX 480M | CFO confirms annual funding beyond this envelope. |

## CFO Memo | Governance as Loss Prevention

**To:** CFO, SRG **Subject:** Why a small governance control set is not bureaucracy

The Jinja incident already demonstrates an avoidable control failure: 9,000 customer records containing names, phones, and purchase history left the controlled environment unencrypted; internal escalation took 11 days; no notification was made. The exact legal and response cost cannot be calculated from the case because no forensic, regulator, customer-remediation, or contract data were supplied. That uncertainty is a reason to instrument controls, not invent a fine.

A transparent workload scenario makes the reporting cost concrete. If two analysts each spend 11 working days per monthly cycle reconciling spreadsheets, at 8 hours/day and UGX 25,000 fully loaded cost/hour, that is 2 x 11 x 8 x 12 x 25,000 = **UGX 52.8M per year** in staff capacity. If only one analyst is involved, the same assumption is UGX 26.4M; if four, UGX 105.6M. These are planning estimates, not observed payroll cost. They exclude the cost of delayed decisions and inventory errors.

External cases show that security failures can produce material enforcement and remediation costs: the Equifax settlement included up to USD 575M; the UK ICO fined British Airways GBP 20M; and Marriott was fined GBP 18.4M. Those companies, legal regimes, incident facts, and scales differ sharply from SRG, so the figures are context, not a forecast or direct comparator.

The highest-value day-one policy is managed endpoint encryption and export control, implemented as a default technical setting with a narrow, logged exception path. It would have protected the stolen laptop's readable contents if recovery keys and device controls were managed. The policy most likely to be breached in daily habits is access/classification: spreadsheets and exports are convenient, so a rule alone will fail. Make the safe path the easy path: provide masked approved views, disable local unencrypted exports, require business justification and expiry for bulk access, alert on unusual downloads, and review exception logs monthly. Governance pays when it changes defaults and assigns an owner; a committee that produces no enforceable changes is bureaucracy.
