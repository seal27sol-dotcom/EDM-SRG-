# Sources and Verification Notes

## Assignment source

- `ENTERPRISE DATA MANAGEMENT.pdf`, Project Savanna: Enterprise Data Management Turnaround, supplied in this workspace. Pages 1-12 establish the scenario, resource list, deliverables, constraints, and submission requirements.

## Primary / official legal sources

- Uganda, **Data Protection and Privacy Act, 2019**, Act 9 of 2019. ULII legislation text: <https://ulii.org/akn/ug/act/2019/9/eng@2019-05-03>. The brief itself states PDPO registration obligations apply. The section references used in this draft are s.7 (consent/processing conditions), s.16 (correction/deletion), s.19 (cross-border transfers), s.23 (security-breach notification), and s.29 (registration). Verify the current consolidated Act, regulations, and PDPO guidance before final legal reliance.
- EU **General Data Protection Regulation (EU) 2016/679**, official text: <https://eur-lex.europa.eu/eli/reg/2016/679/oj>. Relevant provisions include Arts. 5-7, 12-22, 25, 28, 32-35, and 44-49. Art. 33 provides the 72-hour supervisory-authority notification rule where applicable; Art. 34 covers communication to data subjects in high-risk cases.
- California Consumer Privacy Act / CPRA, California Civil Code §1798.100 et seq.: <https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?division=3.&part=4.&lawCode=CIV>. Comparative reference only; applicability is not established by the case.

## Public incident examples used in the CFO memo

- U.S. Federal Trade Commission, Equifax settlement announcement (up to USD 575 million): <https://www.ftc.gov/news-events/news/press-releases/2019/07/equifax-pay-575-million-settle-ftc-cfpb-states-related-2017-data-breach>
- UK Information Commissioner's Office, British Airways penalty (GBP 20 million): <https://ico.org.uk/action-weve-taken/enforcement/british-airways/>
- UK Information Commissioner's Office, Marriott penalty (GBP 18.4 million): <https://ico.org.uk/action-weve-taken/enforcement/marriott-international-inc/>

These incidents differ in company size, facts, jurisdiction, and legal regime. They illustrate potential scale, not a forecast of SRG liability. The reporting-labor scenario in the CFO memo is an explicit assumption, not measured payroll evidence.

## Design frameworks

- DAMA International, *DAMA-DMBOK: Data Management Body of Knowledge*, 2nd edition, for the knowledge-area mapping.
- Stephen Few, *Information Dashboard Design*, and Edward Tufte, *The Visual Display of Quantitative Information*, for the dashboard critique: avoid misleading dual axes and distinguish measures with different units and meanings.

## Data provenance

Every generated source in `data/*_demo.*` is synthetic. Seed `20261004`; transaction period Jan-Jun 2025; fixed FX assumptions documented in generated JSON and scripts. No real customer or employee data is used.
