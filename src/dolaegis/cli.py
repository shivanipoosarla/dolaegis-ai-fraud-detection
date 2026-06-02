from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import List

from .models import Transaction
from .risk_engine import FraudRiskEngine, RiskResult
from .dashboard import write_dashboard_html
from .reporting import write_json_report, write_markdown_report
from .governance import build_audit_record, write_audit_log


def load_transactions(path: Path) -> List[Transaction]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [Transaction.from_row(row) for row in reader]


def analyze_file(input_path: Path, outdir: Path) -> List[RiskResult]:
    engine = FraudRiskEngine()
    transactions = load_transactions(input_path)
    results = [engine.score(tx) for tx in transactions]
    write_json_report(results, outdir / "fraud_risk_report.json")
    write_markdown_report(results, outdir / "fraud_risk_report.md")
    write_dashboard_html(results, outdir / "fraud_dashboard.html")
    audit_records = [build_audit_record(tx, result) for tx, result in zip(transactions, results)]
    write_audit_log(audit_records, outdir / "audit_log.jsonl")
    return results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="DolAegis fraud-risk scoring demo")
    parser.add_argument("--input", required=True, help="Path to transaction CSV file")
    parser.add_argument("--outdir", default="reports", help="Directory for generated reports")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    input_path = Path(args.input)
    outdir = Path(args.outdir)

    if not input_path.exists():
        parser.error(f"Input file not found: {input_path}")

    results = analyze_file(input_path, outdir)
    high = sum(1 for r in results if r.level == "high")
    review = sum(1 for r in results if r.decision == "manual_review")
    approved = sum(1 for r in results if r.decision == "approve")
    print(f"Analyzed {len(results)} transactions. High risk: {high}. Manual review: {review}. Approved: {approved}.")
    print(f"Reports, dashboard, and audit log written to: {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
