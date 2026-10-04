#!/usr/bin/env python3
"""Build a print-ready HTML portfolio from Markdown and embedded Mermaid sources."""

import html
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "portfolio.md"
OUTPUT = ROOT / "docs" / "portfolio.html"
DIAGRAM_DIR = ROOT / "diagrams"


def embed_diagrams(text: str) -> str:
    for path in sorted(DIAGRAM_DIR.glob("*.mmd")):
        marker = f"<!-- EMBED:{path.stem} -->"
        if marker in text:
            diagram = html.escape(path.read_text(encoding="utf-8"))
            text = text.replace(marker, f'<figure class="diagram"><pre class="mermaid">{diagram}</pre><figcaption>{path.stem.replace("-", " ").title()}</figcaption></figure>')
    return text


def main() -> None:
    source = embed_diagrams(SOURCE.read_text(encoding="utf-8"))
    body = markdown.markdown(source, extensions=["tables", "fenced_code", "toc"])
    document = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Project Savanna | EDM Portfolio</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Source+Serif+4:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--ink:#182722;--muted:#607168;--forest:#183b32;--teal:#26786e;--coral:#cb6e52;--line:#d9e1da;--paper:#f4f6f1;--surface:#fff}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:11pt/1.58 "Source Serif 4",Georgia,serif}}
.cover{{padding:22mm 18mm 12mm;background:var(--forest);color:#f4f7ee;min-height:72mm;border-bottom:5px solid #c4e36a}}
.cover .overline{{font:9pt "Manrope",sans-serif;letter-spacing:0;color:#c6d6c9;text-transform:uppercase}}
.cover h1{{margin:12mm 0 3mm;font:700 32pt/1.12 "Manrope",sans-serif;color:#fff}}
.cover p{{max-width:145mm;color:#d9e5db;font:12pt/1.5 "Manrope",sans-serif}}
.cover .meta{{margin-top:14mm;font:9pt "Manrope",sans-serif;color:#b8cdc0}}
article{{max-width:190mm;margin:12mm auto;padding:0 10mm 20mm;background:#fff}}
h1,h2,h3,h4{{font-family:"Manrope",Arial,sans-serif;line-height:1.25;color:var(--forest);break-after:avoid}}
article h1{{margin-top:15mm;font-size:22pt}}article h2{{margin-top:11mm;padding-bottom:2mm;border-bottom:1px solid var(--line);font-size:16pt}}article h3{{margin-top:7mm;font-size:12pt}}p,li{{orphans:3;widows:3}}a{{color:var(--teal);overflow-wrap:anywhere}}
blockquote{{margin:5mm 0;padding:2mm 5mm;border-left:3px solid var(--coral);color:#46584e;background:#f6f8f4}}
table{{width:100%;border-collapse:collapse;margin:4mm 0 7mm;font:8.5pt/1.4 "Manrope",Arial,sans-serif;break-inside:auto}}
th{{background:#eaf1e8;color:var(--forest);text-align:left}}th,td{{padding:2.3mm;border:1px solid var(--line);vertical-align:top}}tr{{break-inside:avoid}}
code,pre{{font-family:"DM Mono",Consolas,monospace;font-size:8pt}}.diagram{{margin:7mm 0;padding:4mm;border:1px solid var(--line);background:#fbfcf9;break-inside:avoid;overflow:visible}}.diagram pre{{white-space:pre-wrap}}.diagram svg{{max-width:100%;height:auto}}figcaption{{margin-top:2mm;color:var(--muted);font:8pt "Manrope",sans-serif;text-align:right;text-transform:uppercase}}
#toc{{padding:4mm 6mm;background:#f1f5ef;border:1px solid var(--line)}}
@page{{size:A4;margin:15mm 16mm 17mm;@bottom-right{{content:"Project Savanna | " counter(page);font:8pt "Manrope",sans-serif;color:#718078}}}}
@media print{{body{{background:#fff;font-size:10pt}}.cover{{break-after:page;min-height:0;padding:18mm}}article{{max-width:none;margin:0;padding:0}}a{{color:inherit;text-decoration:none}}.diagram{{break-inside:avoid}}}}
</style>
</head>
<body>
<header class="cover"><div class="overline">Savanna Retail Group · Enterprise Data Management</div><h1>Project Savanna</h1><p>Data management turnaround · Consultancy portfolio draft</p><div class="meta">A1-D2 integrated capstone · Individual submission · October 2026</div></header>
<article>{body}</article>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>if(window.mermaid)mermaid.initialize({{startOnLoad:true,theme:'base',securityLevel:'strict',themeVariables:{{primaryColor:'#edf4e9',primaryTextColor:'#182722',primaryBorderColor:'#26786e',lineColor:'#607168',secondaryColor:'#fff0e8',tertiaryColor:'#f6f8f4',fontFamily:'Manrope, sans-serif'}}}});</script>
</body>
</html>'''
    OUTPUT.write_text(document, encoding="utf-8")
    print(f"Built print-ready portfolio: {OUTPUT.relative_to(ROOT)} ({len(body):,} HTML characters)")


if __name__ == "__main__":
    main()
