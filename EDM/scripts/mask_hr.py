#!/usr/bin/env python3
"""Create a least-privilege analytics copy of the synthetic HR workbook."""

import csv
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "SRG_HR_demo.xlsx"
TARGET = ROOT / "data" / "cleaned" / "SRG_HR_analytics_masked.csv"


def mask(value: object, visible: int = 2) -> str:
    digits = "".join(character for character in str(value or "") if character.isdigit())
    return "*" * max(0, len(digits) - visible) + digits[-visible:] if digits else ""


def salary_band(value: object) -> str:
    salary = int(value or 0)
    return "< UGX 2M" if salary < 2_000_000 else ("UGX 2M-5M" if salary < 5_000_000 else "> UGX 5M")


def main() -> None:
    worksheet = load_workbook(SOURCE, read_only=True, data_only=True).active
    iterator = worksheet.iter_rows(values_only=True)
    headers = next(iterator)
    indexes = {name: index for index, name in enumerate(headers)}
    output = []
    for row in iterator:
        output.append({
            "EmployeeID": row[indexes["EmployeeID"]],
            "JobTitle": row[indexes["JobTitle"]],
            "NationalIDMasked": mask(row[indexes["NationalID"]], 4),
            "PhoneMasked": mask(row[indexes["Phone"]], 2),
            "SalaryBand": salary_band(row[indexes["SalaryUGX"]]),
        })
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    with TARGET.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)
    print(f"Masked {len(output)} synthetic HR rows; direct identifiers and exact salary are excluded.")


if __name__ == "__main__":
    main()
