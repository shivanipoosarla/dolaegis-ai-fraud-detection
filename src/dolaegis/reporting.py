from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

from .risk_engine import RiskResult


def write_json_report(results: Iterable[RiskResult], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    serializable = [result.to_dict() for result in results]
    out_path.write_text(json.dumps(serializable, indent=2), encoding="utf-8")


def write_markdown_report(results: List[RiskResult], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# DolAegis Fraud Risk Report", ""]
    lines.append(f"Transactions analyzed: {len(results)}")
    lines.append(f"High risk: {sum(1 for r in results if r.level == 'high')}")
    lines.append(f"Manual review: {sum(1 for r in results if r.decision == 'manual_review')}")
    lines.append(f"Approved: {sum(1 for r in results if r.decision == 'approve')}")
    lines.append("")

    for result in results:
        lines.append(f"## Transaction {result.transaction_id}")
        lines.append(f"- User: `{result.user_id}`")
        lines.append(f"- Score: **{result.score}/100**")
        lines.append(f"- Risk level: **{result.level}**")
        lines.append(f"- Decision: **{result.decision}**")
        if result.factors:
            lines.append("- Factors:")
            for factor in result.factors:
                lines.append(f"  - `{factor.name}` +{factor.points}: {factor.explanation}")
        else:
            lines.append("- Factors: none")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
