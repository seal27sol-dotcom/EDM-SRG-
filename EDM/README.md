# Project Savanna: EDM Portfolio

This workspace contains the source portfolio, reproducible demo data, SQL and Python artifacts, editable Mermaid diagrams, and a portable static dashboard for the Enterprise Data Management capstone.

## Important data provenance

The PDF lists instructor-provided files, but only `ENTERPRISE DATA MANAGEMENT.pdf` was present in the workspace. Therefore every row currently in `data/*_demo.*` is synthetic and generated with a fixed seed. Synthetic metrics and dashboard findings are demonstrations, not statements about SRG's actual records. Replace or reconcile these inputs with the instructor files before submitting findings as empirical evidence. The referenced brief appendices A-E were also not included; the equivalent registers are supplied in `docs/registers.md`.

## Rebuild the artifacts

Requires Python 3.11+.

```powershell
python -m pip install -r requirements.txt
python scripts/generate_demo_data.py
python scripts/profile_clean.py
python scripts/mask_hr.py
python scripts/build_portfolio_html.py
python -m unittest discover -s tests
```

The generator creates 5,000 customers, 1,200 products, 60,000 transactions across six months, 14 suppliers, loyalty rows, an HR workbook, a synthetic ETL log, and footfall events. The profiling script emits cleaned CSVs, quality metrics, rejected rows, and the dashboard JSON.

## Run the dashboard locally

With XAMPP, place this workspace beneath `htdocs` and open:

`http://localhost/EDM/dashboard/`

Or run PHP's local server from the workspace root:

```powershell
C:\xampp\php\php.exe -S 127.0.0.1:8174 -t dashboard
```

Then open `http://127.0.0.1:8174/`.

## Publish the static dashboard

The dashboard has no build step, database, PHP dependency, or server-side secret. Upload the **contents** of `dashboard/` (including `data/srg-demo.json`) to the public document root of InfinityFree or another static host. Keep the relative `data/` directory beside `index.html`. Verify the live page over HTTPS, then capture a full-page screenshot and include the public URL in the submission. Do not publish raw HR or customer-level records: the dashboard JSON contains synthetic transaction identifiers only.

The assignment specifically names Power BI or Tableau Public. This static implementation is ready for the host requested, but confirm with the lecturer that it satisfies the platform requirement; otherwise recreate the same measures and views in Power BI/Tableau Public and submit that service's published link as well.

A BI-ready export is also included in `data/BI_dashboard_dataset.csv` with installation notes in `bi/README.md` so the same analysis can be imported directly into Power BI or Tableau Desktop.

## Evidence and assumptions

- `docs/portfolio.md`: A1-D2 consultancy narrative and interpretation.
- `docs/registers.md`: assumptions, governance RACI, policies, obligations, risks, DPIA, and decision log.
- `docs/data_dictionary.csv`: warehouse metadata for 30+ elements.
- `docs/validation_rules.csv`: entry-point data quality controls.
- `diagrams/`: Mermaid source for the lifecycle, model, MDM, ETL, lineage, fishbone, and roadmap diagrams.
- `sql/`: PostgreSQL warehouse, least-privilege access, test, and ETL scripts.
- `scripts/`: deterministic generator, profiler/cleanser, and HR masking implementation.
- `data/quality_before_after.csv`: computed evidence from the synthetic inputs.

Legal mapping is an academic design aid, not legal advice. Confirm the current consolidated Ugandan legislation, regulations, and PDPO guidance before relying on section interpretations.
