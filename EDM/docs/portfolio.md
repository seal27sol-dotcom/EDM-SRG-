# Project Savanna | Enterprise Data Management Turnaround

**Consultancy portfolio draft | Individual capstone | October 2026**

## Executive Summary

Savanna Retail Group's difficulty is enterprise-wide: twenty-three separate POS databases, e-commerce, loyalty, CRM, Odoo inventory, HR spreadsheets, supplier workbooks, and manual mobile-money files do not share reliable identifiers, controls, or operating ownership. The documented effects are estimated 23% duplicate customer records, misallocated loyalty points, five identifiers for some products, 11 days of monthly manual reporting, 8.4% stock variance, uneven stock availability, unanswered customer-growth/churn questions, and a stolen unencrypted export involving 9,000 people that was escalated internally 11 days late with no breach notification.

The recommended turnaround is a modest hub-and-spoke platform with store-edge buffering, coexistence MDM, governed batch integration, a PostgreSQL analytical warehouse, strong device/access controls, and a month-6 reporting quick win. The plan caps the full 18 months at UGX 480M because Task D1 names that envelope, even though the scenario also describes UGX 480M as an annual budget. It uses SRG's existing staff roles and defers broad streaming, expensive catalog software, and regional rollout until evidence justifies them.

**Evidence boundary:** The assignment PDF was the only provided input. All generated data, cleansed metrics, dashboard values, ETL error lines, and HR examples in this workspace are synthetic and labeled as such. They demonstrate a reproducible method; they do not verify SRG's actual data quality or root causes. The instructor datasets and Appendices A-E are not present. See [Assumptions Register](registers.md#assumptions-register).

### Extended portfolio framing and evidence method

This portfolio is written as a consultancy recommendation for an operational turnaround rather than a purely technical database repair. The evidence base is deliberately limited to the case brief, the synthetic demo dataset, and the governance artifacts created in this workspace. That limitation is important: it prevents unsupported claims about SRG's real customer records, product master, or breach response, while still enabling a credible consultant-style intervention plan. The real value of this submission is not in pretending to have the absent source files; it is in proving that the problem can be framed, prioritized, and resolved in a defensible governance structure using a repeatable data-management method.

The portfolio therefore treats the business problem as an enterprise operating-model issue. Duplicate customer records are not only a data-cleansing problem but also a product-ownership, matching-control, and stewardship problem. The same logic applies to product identifiers, stock variance, delayed reporting, and finance/operations risk. A technical database fix alone would not resolve accountability gaps, poor retention controls, or the absence of a common data contract. The correct response is to establish standards, owners, quality gates, and integration controls so that defects are prevented rather than endlessly repaired after the fact.

The recommended design follows a staged maturity model. During phase 1, the organization aligns owners, policies, and endpoint security. During phase 2, it proves a quick-win dashboard using cleansed, reconciled extracts. During phase 3, it introduces master-data governance and a warehouse. By phase 4, the platform is operationally assured and audited, and only then is wider rollout justified. That sequencing matters because SRG's immediate instability originates from shared process failure, not from a single missing database server or an isolated ETL bug.

The project also demonstrates a disciplined approach to quality metrics and synthetic evidence. Measures such as duplicate row percentages and structural consistency are useful as demonstration indicators, but they are not treated as real empirical facts about the organization. Their purpose is to show how data-quality control should be measured in a portfolio or production setting. This distinction is especially important in a briefing where legal risk, privacy exposure, and customer rights are at the center of the operational concern.

### Tools used

- **AI-assisted research, drafting, and coding support:** ChatGPT, Kimi, Claude, GitHub Copilot, and Kiro. AI-generated suggestions were treated as assistance, not evidence; the author is responsible for checking claims, calculations, citations, and final wording against the case brief and referenced sources.
- **Development and source management:** Visual Studio Code (VS Code) for editing and running project scripts; GitHub for repository and version-control work.
- **Business intelligence:** Tableau was used in the BI workflow. The deliverables here are the browser-based dashboard and BI-ready CSV; a native Tableau workbook is not included.
- **Data preparation:** Python scripts generate the synthetic demonstration data, profile and clean records, and mask the HR example. All resulting measures remain synthetic, as described in the evidence boundary above.

## A1 | EDM Diagnostic and Lifecycle

### Board memo

**To:** SRG Board **From:** Enterprise Data Management Consultant **Subject:** Fix the data operating model, not only the databases

Hiring two more DBAs may improve availability, backups, and query administration, but it does not create one trusted customer identity, govern five product identifiers, validate 14 supplier spreadsheets, define retention, prevent unencrypted exports, or reconcile mobile-money files. SRG's recurring issues cross systems, business processes, roles, and controls. The 11-day reporting delay is a coordination and integration process, not a single database outage. Wrong loyalty allocation is an identity and stewardship problem. The 8.4% inventory variance has no diagnosed cause and needs movement/count evidence, not an assumed database patch.

Enterprise data management (EDM) establishes accountable ownership, common definitions and identifiers, quality rules, lifecycle controls, integration, protection, metadata and decision use across the enterprise. Traditional database administration manages individual database operations: availability, performance, backup, schema, and access within a system. DBAs remain necessary, but they cannot independently decide which system wins for a phone number, whether a local record can be merged, who approves deletion, or when the Board's KPI is trusted.

The evidence points to a control chain: siloed systems and disconnected capture create inconsistent records; inconsistent identifiers make joins and reconciliation costly; manual spreadsheets delay decisions and hide lineage; absent or weak ownership allows defects to recur; endpoint and incident-control failures expose personal data. SRG should treat data as a managed business asset with named owners, measurable controls, and an evidence trail. Cleaning once without changing capture and synchronization merely resets the symptoms.

**First 90 days:** appoint existing data owners/stewards; inventory datasets and processing purposes; encrypt managed endpoints and constrain exports; baseline quality/reporting/stock measures; test a three-store offline-sync pilot; publish a governed first dashboard using reconciled batch extracts. Two additional DBAs alone are not the remedy.

### Customer lifecycle and DAMA-DMBOK

The lifecycle with systems, actors, and failure points is in [customer-lifecycle.mmd](../diagrams/customer-lifecycle.mmd). The principal failure points are no common ID at creation, insecure copies during storage/use, unclear purpose and access during sharing, no evidenced retention schedule, and unproven deletion across source systems and exports.
<!-- EMBED:customer-lifecycle -->

| DAMA-DMBOK area | SRG evidence and maturity judgment |
| --- | --- |
| Data governance | Owners, standards, and decision rights are not evidenced; recurring defects indicate weak accountability. |
| Data architecture | Siloed systems and disconnected stores; an enterprise target model is not evidenced. |
| Data modeling/design | Five product identifiers and customer duplicates show no consistent cross-system model. |
| Data storage/operations | 23 POS databases plus cloud/SaaS and HQ Odoo; local reliability needs explicit design. |
| Data security | Unencrypted stolen laptop, delayed incident reporting, and no breach notice are direct control failures. |
| Data integration/interoperability | Manual reporting/reconciliation and 11-day delay show weak integration. |
| Document/content management | 14 supplier workbooks and HR spreadsheets lack controlled document lifecycle evidence. |
| Reference/master data | Customer and product identifiers conflict; enterprise MDM is not evidenced. |
| Data warehousing/BI | Board cannot answer segment questions; reporting is manual. |
| Metadata | Definitions, lineage, and discovery are not evidenced; C1 supplies a minimum catalog design. |
| Data quality | Duplicate, missing, inconsistent, invalid, and stock-variance symptoms are explicit. |
| Data ethics | Purpose, loyalty consent, matching harms, and footfall notice require explicit safeguards. |

## A2 | Governance and Compliance

The operating charter, existing-role structure, 15-activity RACI, three enforceable policies, prioritized legal register, risk register, and DPIA draft are in [registers.md](registers.md). Core design choices:

- A monthly, 45-minute Data Governance Council chaired by the Head of IT, with CFO sponsorship and domain owners from marketing, procurement, finance, retail operations, and HR. Existing role holders are assigned; no six-person committee is hired.
- Enforce access/classification through managed devices, default masking, role groups, restricted exports, logged exceptions, and quarterly access reviews. Enforce quality through point-of-entry validation, quarantine, owners, measurable thresholds, and publication gates. Enforce retention through purpose-specific schedules, legal holds, verified propagation, and deletion evidence.
- Uganda DPPA is the current operating baseline. The legal map uses sections 7, 16, 19, 23 and 29 as research references; confirm exact consolidated text and regulations with counsel. GDPR Articles 5-7, 12-22, 25, 28, 32-35 and 44-49 are relevant if territorial scope or contract makes them applicable. CCPA/CPRA is comparative only pending a California nexus/threshold assessment.

The single day-one prevention control for the Jinja laptop event is a policy implemented as managed full-disk encryption and controlled export, not a decorative policy document. The daily-practice risk is spreadsheet extraction; the safe alternative must be approved masked views, exception logging, and bulk-export alerts. The CFO memo estimates manual reporting labor only under explicit assumptions and separates public case outcomes from SRG forecasts.

## B1 | Architecture and Data Model

### Pattern decision

Scores are 1 (poor) to 5 (strong). Weights total 100 and favor connectivity and operating capacity because SRG has 23 stores, hours-long outages, four IT staff, and no data engineers.

| Criterion | Weight | Centralized | Decentralized | Federated | Hub-and-spoke |
| --- | ---: | ---: | ---: | ---: | ---: |
| Budget / cost control | 25% | 2 | 4 | 3 | 4 |
| Offline resilience | 25% | 1 | 5 | 4 | 4 |
| Fit to current skills | 20% | 3 | 2 | 2 | 3 |
| Governance / consistent IDs | 15% | 5 | 1 | 3 | 4 |
| Reporting scalability | 15% | 4 | 1 | 3 | 4 |
| **Weighted score / 5** | **100%** | **2.70** | **2.95** | **3.05** | **3.80** |

Hub-and-spoke is recommended: retain operational systems initially, buffer store events locally, sync idempotently when connectivity returns, centralize mastered identifiers and analytical copies, and migrate only when evidence warrants it. A single central operational database would make outages a sales-blocking event; fully decentralized operation perpetuates fragmentation; federation leaves too much capability burden on the two SQL-capable staff.
<!-- EMBED:architecture -->

### ER model and normalization

The [Crow's Foot ER source](../diagrams/srg-erd.mmd) includes Customer, Product, Store, SalesOrder, OrderLine, Payment, Supplier, SupplierProduct, and LoyaltyAccount. A customer can have zero or more orders and multiple program accounts; an order contains one or more lines and one or more payments; Product-Supplier is many-to-many through SupplierProduct. Digital orders may have no physical store. A household is a separately governed optional relationship and is never inferred just from a shared address.
<!-- EMBED:srg-erd -->

1. **UNF:** illustrative sales export has repeated item columns, mixed date/currency formats, and transaction plus customer/product labels in one row. It is not a claim about the absent source extract.
2. **1NF:** one row per transaction line; atomic IDs, quantity, unit price, payment method/reference, date, and currency; repeated items become separate rows.
3. **2NF:** separate Order header from OrderLine; line attributes depend on the full order-line key, not only order ID; customer, store, payment and date are referenced by keys.
4. **3NF:** move customer, product, store, supplier, payment method, and date descriptions into their own entities. Product category/supplier labels no longer depend transitively on a sales line key. Preserve source aliases in crosswalks.

**Justified denormalization:** a star-schema fact table stores transaction measures with dimension surrogate keys and selected descriptive attributes for scan-efficient Board reporting. It duplicates some labels and can lag the operational truth; dimensions remain mastered, refreshes are gated, and facts are rebuilt/reconciled from immutable raw data. This is not an argument to denormalize the transaction-entry core.

Model assumptions and break cases: (1) one loyalty account maps to one person; family phone-sharing can violate that, so retain separate person links and stewardship. (2) a sale has one currency; split tender may have multiple Payment rows. (3) one supplier owns one product; imports/private-label alternatives need SupplierProduct and effective dates. (4) a digital order belongs to a store; it may ship from a warehouse or third-party fulfillment, so store key is optional and fulfillment is modeled separately when available.

## B2 | Data Quality and Cleansing

Run `scripts/generate_demo_data.py` then `scripts/profile_clean.py`. The exact-match logic is normalized email OR normalized name plus phone; missing/ambiguous identity stays separate. No fuzzy merge was used in the measured demo.

| Demo metric | Customers before | Customers after | Products before | Products after |
| --- | ---: | ---: | ---: | ---: |
| Rows | 5,000 | 3,869 | 1,200 | 1,200 |
| Matched duplicate rows / duplicate SKUs | 22.62% | 0.00% | 4.92% | 0.00% |
| Accuracy proxy (structural plausibility only) | 8.16% | 93.12% | 100.00% | 100.00% |
| Consistency | 1.70% | 100.00% | 48.17% | 100.00% |
| Completeness | 96.28% | 96.95% | 100.00% | 100.00% |
| Validity | 8.16% | 93.12% | 48.17% | 100.00% |
| Timely within 90 days | 24.32% | 24.35% | 15.67% | 15.67% |
| Uniqueness | 77.38% | 100.00% | 95.08% | 100.00% |

These values are generated evidence, not SRG actuals. Duplicate-SKU conflicts are not auto-merged: all 1,200 product IDs remain, source codes are retained as aliases, and conflicting rows receive provisional unique warehouse SKUs pending stewardship. Customer aliases map through `data/cleaned/customer_crosswalk.csv`, preserving every source ID for replay and reversal. Timeliness uses synthetic `LastUpdatedAt` and a 90-day SLA as-of 2025-06-30; cleaning cannot make stale source data fresh. Accuracy cannot be proven without ground truth. `accuracy_proxy_pct` is a structural plausibility proxy and must not be reported as verified factual accuracy. Counts and variant classes are in `data/quality_before_after.csv`.

Root-cause reasoning and the fishbone are in [stock-fishbone.mmd](../diagrams/stock-fishbone.mmd). The brief gives 8.4% variance but no stock snapshots or movement logs; likely mechanisms are hypotheses. Collect time-aligned book/physical quantities, receipts, returns, transfers, adjustments, unit conversions, POS retry logs, and count evidence before ranking causes. The example broken ETL log in `data/etl_error_log_demo.txt` is synthetic: skipped store extract, duplicate product key, and a false `SUCCESS` after partial load. Production control is fail-closed status, checkpoints, idempotent replay, and quarantine.
<!-- EMBED:stock-fishbone -->

Twenty entry controls with owners and enforcement are in `docs/validation_rules.csv`. Monitoring: daily pipeline/source completeness and reconciliation; weekly customer/product scorecards; alert immediately on any unsupported currency, source-ID collision, missing partition, or breach escalation; alert at <99.5% fact/dimension match; alert if mobile-money payment-reference exception exceeds 1% per provider; inventory variance >2% or the Finance-approved value threshold triggers recount. Stewards own exceptions; domain owners own root cause; Head of IT owns pipeline replay; overdue critical issues go to Council.

## B3 | Customer MDM

Use **coexistence MDM**: golden identity and crosswalk are centrally governed, while POS/CRM/e-commerce/loyalty continue during transition. Reject registry-only because unresolved duplicates still reach operational workflows; reject immediate centralization because connectivity and source replacement are unrealistic; reject consolidation-only as insufficient for returning golden identifiers to operational use.

Golden record: enterprise ID; source ID crosswalks; full name; normalized phone; email; district/address; preferences and purpose-specific consent; provenance, confidence, last-verified time, effective dates, merge/unmerge audit. Attribute survivorship: current consent/preference wins only from the consent ledger; verified customer-updated contact beats stale CRM, then CRM over POS free text; name chooses highest-completeness verified CRM/loyalty evidence; address uses recent verified customer update; source values and provenance remain available rather than being overwritten.

Deterministic: exact normalized phone plus name, exact verified email, or existing enterprise crosswalk. Probabilistic review score: phone exact 40%, email exact 25%, normalized name similarity 20%, district 10%, DOB 5%. Auto-link only at >=95 with exact phone/email support and no conflicting DOB or protected attribute; 75-94 is manual review; <75 remains separate. Hard conflicts always block automatic merge. A false merge can destroy loyalty separation, expose purchase history, and impair rights; merges are reversible and logged.

The offline process is shown in [mdm-offline.mmd](../diagrams/mdm-offline.mmd): create a provisional local ID and encrypted outbox event, continue sale, then sync an idempotent upsert. The steward queue handles ambiguity. Local IDs are aliases, not competing golden IDs. Store managers co-design the workflow and receive an outage-safe reconciliation report; no store is penalized for connectivity-related provisional capture.
<!-- EMBED:mdm-offline -->

## B4 | Integration, Warehouse, Real-Time

[Warehouse star](../diagrams/warehouse-star.mmd) covers FactSales plus future FactInventorySnapshot and aggregate FactFootfall, with conformed Date, Customer, Product, Store, and Payment dimensions. The five logical sources assumption is documented above. Inventory fact is necessary to test variance and availability; it cannot be populated from sales alone.

**Batch workflow:** source-specific extract (POS checkpointed CSV/replica, PostgreSQL snapshot, loyalty API/export, Odoo incremental updated-at, payment-provider settlement file); immutable encrypted landing; schema/count/checksum/watermark checks; normalize ID/date/currency/unit; deterministic matching and crosswalk; load dimensions then facts; SCD2 effective-date product/store changes; count/amount/FK reconciliation; atomic partition publish; quarantine and owner alert on any failed gate. Store uploads resume from a durable local checkpoint. [etl-workflow.mmd](../diagrams/etl-workflow.mmd) and `sql/etl_transform.sql` implement the core flow.
<!-- EMBED:warehouse-star -->
<!-- EMBED:etl-workflow -->

| Criterion | ETL | ELT | SRG decision |
| --- | --- | --- | --- |
| Latency | Transform before load; predictable batch | Raw data lands quickly; transformation follows | Batch daily for finance/Board; smaller CDC only for operational alerts |
| Cost | Compute outside warehouse; more pipeline components | Warehouse compute can become expensive if uncontrolled | Compare total managed-service cost at pilot volume |
| Scalability | Separate workers scale independently | Warehouse scales transformation | Begin simple; benchmark before migration |
| Complexity | More jobs and schema mapping | SQL model/governance burden shifts to warehouse | Two SQL-capable IT staff favor managed, documented pipelines |
| Connectivity | Buffer at source and upload later | Same source ingestion issue remains | Edge outbox plus resumable batch; cloud choice does not fix outages |

**Streaming judgment:** use a narrow stream for inventory movement/stock availability only if POS/Odoo can emit reliable idempotent events and stores have store-and-forward; alert on stale inventory separately. Mobile-money fraud detection needs provider authorization/settlement events and measured fraud windows; footfall sensor events do not identify payment fraud. Pilot provider payment-event scoring with rules, not AI black-box decisions; process suspicious patterns within minutes only if loss evidence justifies cost. Footfall stays anonymized/aggregated at edge and supports occupancy planning, not person matching. Monthly customer segmentation, Board reporting, supplier reconciliation, and most quality checks remain batch.

## C1 | Metadata

`docs/data_dictionary.csv` provides 40+ business, technical, and administrative elements with lineage, owner, sensitivity, and quality rule. Tags: domain `{customer, product, sales, inventory, supplier, people, payment, footfall}`; sensitivity `{public, internal, confidential, restricted}`; quality `{unprofiled, monitored, exception, certified}`. The [KPI lineage](../diagrams/kpi-lineage.mmd) defines monthly active customer as distinct mastered customer IDs with qualifying transaction lines in the selected month; returns do not create separate customers and voids are excluded.
<!-- EMBED:kpi-lineage -->

Address schema change impact: ingestion mappings and MDM survivorship; POS/CRM/e-commerce sync; consent/rights workflows; masked views and access policies; customer dimension, SCD2 history, address quality rules; district segmentation, store-catchment analysis, and Board dashboard filters. Require versioned schema, dual-write/backfill plan, downstream dependency review, and owner sign-off before release.

Catalog comparison: OpenMetadata offers an open-source catalog and lineage surface but still needs hosting, connectors, upgrades, and an operator; Collibra offers managed governance workflows and support but license/implementation costs are disproportionate before ownership maturity is established. Start with versioned dictionary, owner registry, lineage diagrams, and issue log in the repository; run an OpenMetadata pilot only after a named technical custodian and connector inventory exist. Reassess total cost including support, not license alone.

## C2 | Security and Privacy

Threat model includes stolen/unmanaged endpoint, malicious or careless insider export, SaaS credential compromise, phishing/ransomware, store outage and delayed replay, duplicate-link disclosure, weak vendor/subprocessor control, stale backups, and footfall re-identification. The 12 scored risks and mitigations are in [registers.md](registers.md#risk-register).

Roles and least-privilege SQL are in `sql/access_controls.sql`; `sql/access_control_tests.sql` asserts analyst success for permitted customer fields and denial for email. Run both in a PostgreSQL test database and capture actual result output before claiming test evidence. `scripts/mask_hr.py` creates `data/cleaned/SRG_HR_analytics_masked.csv`: national ID and phone are partially masked, exact salary replaced by a band. Raw HR input remains restricted and must not be published.

Encrypt managed laptops/removable media at rest; TLS for source/warehouse traffic; centrally managed recoverable keys and rotation; restrict raw landing access to service accounts; mask or aggregate analytics; log export and privileged activity; test restore/revocation. Allocate first to endpoints/identity/backup/incident response, then data-platform controls; do not spend the small budget on universal streaming or encrypting public/aggregated data at a higher operational cost than risk reduction.

The draft EU loyalty DPIA and breach response are in `docs/registers.md`. Complete a production audit against the compliance register before month 12. The Uganda DPPA breach process is based on prompt PDPO notification under s.23; GDPR's 72-hour authority clock and high-risk subject communication apply only where relevant. The Act's local requirement is not replaced by that GDPR timeframe.

## C3 | Analytics, Dashboard, Emerging Technology

Board questions: (1) which customer cohorts become inactive under an approved recency definition? (2) which segments grow in active customers and contribution? (3) which store-product pairs stock out while elsewhere overstocked? (4) which payment patterns merit fraud review? (5) which districts/categories support Kenya/Rwanda expansion? The workflow is source → data contract and quality gates → conformed dimensions/facts → approved cohort/stock/payment method → role-filtered dashboard/alert → owner action and outcome measurement.

The static dashboard lives in `dashboard/`, supports period/channel/store/district/category filters, monthly trend, category mix, store ranking, quality checkpoint, transaction detail, pagination, and filtered CSV export. See [dashboard-insight-brief.md](dashboard-insight-brief.md). It answers descriptive synthetic sales questions only. Churn, stock optimization, fraud, margin, and expansion claims need additional source data; no conclusions are fabricated. The chart critique and replacement decision are in the insight brief.

Cloud stack assessment: **Google Cloud Storage + Dataflow/Dataproc only when justified + BigQuery + Looker Studio** is a plausible managed analytical option, but start with the smallest managed PostgreSQL/batch deployment; BigQuery/serverless spending, IAM, network egress, and cross-border configuration must be costed. Pilot a low-risk sales subject area, monthly cost alert, export test, and operational runbook before adoption. Decision: **pilot**, not immediate full migration.

AI-driven trend: AI-assisted anomaly and matching suggestions can prioritize steward queues, but no automatic customer merges, pricing/credit decisions, or protected-trait inference. Decision: **pilot offline on labeled synthetic/approved samples with precision/recall and subgroup review; reject autonomous decisions** until data rights, error costs, and fairness are evidenced. Maturity: currently fragmented/manual; month 6 repeatable batch and named owners; year 1 governed warehouse/quality monitoring; year 2 controlled self-service and selective event processing, contingent on people, legal, and cost readiness.

## C4 | Operating Model and Control Framework

### Data ownership and stewardship model

The organization cannot pursue enterprise governance successfully if the owners of customer, product, stock, and payment data remain unclear. The first design decision in this portfolio is to reuse existing roles: each source domain retains a domain owner for accountability, with a named data steward for daily review, a technical custodian for pipeline implementation, and a business sponsor for exception sign-off. This matches the evidence in the brief: SRG has existing leaders in IT, finance, procurement, store operations, marketing, and HR, but no visible operating data-governance structure. Ownership is therefore assigned to the people already responsible for the process rather than to newly hired enterprise roles that would not be sustainable after the initial pilot.

The model is simple. Product data is owned by procurement and category management because they govern supplier, product variants, and cost flows. Sales and customer data are owned by retail operations and marketing because they decide who is a customer, what is a loyalty record, and how customer value is measured. Inventory and stock data are owned by operations and finance because variance and availability impact revenue, margin, and reconciliation. Payments and financial records remain under finance and the payment-provider relationship, with system and security controls owned by IT. HR remains under HR and the privacy/people team, with legal review for the data retention and breach plan.

This pattern is important because governance does not stop at policy writing. Data owners must approve acceptable-quality thresholds, validate critical terms, review exceptions, and confirm retention rules. Without that chain, the dashboard may look credible while quietly publishing erroneous or outdated values. A stewardship queue therefore carries all unresolved duplicates, product disputes, supplier mismatches, and inconsistent loyalty IDs for argument-based review. A control board reviews recurring exceptions and decides whether the issue is a source-process problem, a quality rule problem, or a regulatory exposure.

### Service-level controls and operational assurance

Operational governance needs a set of service levels, not just a policy document. The portfolio assumes a monthly Board pack with a hard threshold that critical data assets must have a named owner, retention schedule, access class, and quality score. For example, critical dimensions such as Customer, Product, Store, and Inventory must have lineage and a quality score above 95% before they become trusted for Board reporting. Supplier and payment files have a stricter acceptance standard because a single bad file can distort reconciliation or trigger a financial control failure.

The following control stack operationalizes the governance model:

- Source validation: schema check, duplicate detection, required field validation, file checksum, and source watermark.
- Landing-zone controls: encrypted raw source store, read-only restricted access, immutable retention, and audit log.
- MDM controls: golden-ID crosswalk, reversible merge, conflict quarantine, and steward review queue.
- BI controls: dashboard access by role, row-level or field-level masking, publish approval, and refresh audit.
- Privacy controls: purpose limitation, consent traceability, retention period evidence, breach escalation clock, and deletion verification.
- Exception control: every unresolved quality issue has an owner, due date, and closure evidence.

The governance structure creates confidence for the board and reduces the risk that a clean dashboard simply repeats stale or disputed source assumptions. This is essential because the assignment also describes a loss of customer data and a delayed internal escalation. A technical solution without a decision process would not address the probability of recurrence.

### Data-retention, deletion, and legal defensibility

The legal part of the EDM strategy is often underdeveloped in practical project work, but it is central to this brief. SRG handles customer, loyalty, HR, payment, and operational data across retail and internal functions. That means the organization must distinguish data life cycles by purpose rather than by system. A sales line record may be required for financial reporting, while a loyalty preference may require explicit consent and a deletion window tied to that purpose. The same applies to employee records, where salary, phone, and ID details may be kept under employment law and local privacy obligations, but not reused for general analytics.

The portfolio therefore recommends that retention schedules become part of the data-contract layer. Each source table and report should carry a standard record: purpose, owner, legal basis, retention period, archive strategy, active subject rights, and deletion trigger. This must be reviewed with legal counsel and updated when source systems change. It also means the dashboard cannot use raw HR or full customer PII for analytics without prior de-identification and a defined purpose. The synthetic masked HR response in this project demonstrates the principle, but production deployment requires a formal review with the HR function and privacy lead.

A robust retention process reduces legal risk and supports information governance. It also reduces future confusion about which system is the system of record. When a record is deleted or merged, the organization must preserve lineage information so that audits, rights requests, and incident investigations remain traceable. This is especially important in the SRG case, where a stolen export triggered a delayed internal escalation and a reputational risk scenario.

## C5 | Portfolio Evaluation and Scenario Rigor

### Understanding the limits of the scenario and the evidence

This portfolio is intentionally transparent about limits. It does not claim to know the exact SRG customer base, product list, payroll records, or raw breach timeline. The absent PDF appendices mean that some material facts in the brief are necessarily interpreted and shaped into a consultant-like model. The assignment is not asking for a forensic reconstruction of a real company; instead, it is asking for data-management reasoning, policy design, architecture, governance, and a credible solution narrative. In that sense, the project acts as a structured demonstration of how an EDM consultant would diagnose, scope, and recommend a response to a fragmented and risky data environment.

This is a crucial distinction: evidence quality matters. A strong plan in data management is not judged by whether the consultant claims to have seen the exact organization-wide systems; it is judged by whether the plan is internally consistent, risk-based, operationally feasible, and resilient under realistic governance constraints. The portfolio reflects that standard. It distinguishes synthetic demonstration data from actual SRG data, states the assumptions, and makes the boundary visible in the narrative.

### Why the portfolio is credible despite missing source files

A credible EDM recommendation depends on four things: clear business symptoms, a plausible operating model, defensible control design, and a measured delivery roadmap. The scenario supplies all four. The symptoms are visible across customer duplicates, stock variance, manual processes, data exfiltration, and delayed reporting. The operating model is a staged hub-and-spoke architecture designed for a mid-sized retailer with limited technical capacity. The control design frames security, retention, stewardship, and issue ownership as part of the same enterprise data process rather than separate IT activities. The roadmap provides phases, gate decisions, and budget envelopes so the board can understand the next steps and the cost of delay.

The synthetic dataset, dashboard, and SQL scripts enrich that case by proving that the recommended techniques are runnable, measurable, and auditable. They do not replace the real system; they demonstrate the artifact chain a decision-maker expects: source, quality gate, MDM, warehouse, dashboard, and governance review. That is the core of EDM consulting work: not simply writing SQL or building a dashboard, but proving the business case for controlled data operations.

## D1 | 18-Month Roadmap and Budget

| Phase | Months | Allocation | Milestones / gate | Success measures |
| --- | --- | ---: | --- | --- |
| Stabilize and govern | 1-3 | UGX 70M | Charter, owners, endpoint encryption, breach drill, source inventory | 100% managed laptops encrypted; named owners for critical domains; incident drill completed |
| Visible quick wins | 4-6 | UGX 100M | Reproducible profiling, approved cleansed customer/product extract, first reconciled dashboard, three-store outbox pilot | Monthly report cycle <=4 days (baseline method confirmed); month-6 Board demo; zero partial-success publishes |
| Integrate and master | 7-9 | UGX 110M | Customer/product crosswalk, coexistence MDM, warehouse sales MVP, rule/exception queues | >=99.5% fact-to-dimension resolution; all merges reversible and logged |
| Assure and audit | 10-12 | UGX 90M | Metadata lineage, RBAC/masking, rights and retention rehearsal, PDPO audit pack | 100% critical datasets have owner/classification; access review complete; PDPO evidence ready |
| Scale selectively | 13-18 | UGX 110M | Extend stores, inventory snapshot fact, targeted event pilot, Kenya/Rwanda readiness gate | Stock variance baseline reproducible and trend improves toward <=5.5%; monthly reporting <=2 days; cost within cap |
| **Total** | **18 months** | **UGX 480M** | | |

Itemized envelope: existing staff backfill/training and short specialist support UGX 80M + managed platform/cloud/licenses UGX 115M + integration/quality/MDM delivery UGX 112M + endpoint/security/privacy controls UGX 58M + change/adoption UGX 30M + contingency UGX 85M = **UGX 480M**. Contingency is 17.7% of total and may be released only by CFO at stage gates. Amounts are planning estimates requiring vendor quotes and tax/FX validation. No additional permanent data-engineering hire is assumed. If CFO confirms the budget is annual and makes a separate second-year allocation, the Board must approve a revised total; this roadmap does not silently spend UGX 720M.

The [roadmap diagram](../diagrams/roadmap.mmd) sequences governance before quality, quality before MDM, MDM before integration, metadata through the lifecycle, security across all phases, and analytics as the measurable benefit. Each phase has a stop/go checkpoint; if a pilot misses access, quality, cost, or reliability gates, pause scale and fix the root cause.
<!-- EMBED:roadmap -->

## D2 | Decisions, Red Team, Reflection, Viva

The decision log has nine entries in `docs/registers.md`. The red-team challenge is in [red-team.md](red-team.md); the reflective essay draft is in [reflection.md](reflection.md). The [viva guide](viva-guide.md) provides a 15-minute defense path and likely challenge questions. Rewrite the reflection to your actual career goals and voice, verify legal references, and declare AI assistance according to KIU policy before submission.
