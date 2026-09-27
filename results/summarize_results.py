#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""汇总评估 JSON，生成论文结果表。"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TABLES_DIR = PROJECT_ROOT / "results" / "tables"


MAIN_COLUMNS = [
    ("model", "Model"),
    ("recall_at_1", "Recall@1"),
    ("recall_at_5", "Recall@5"),
    ("mrr", "MRR@10"),
    ("fdr", "FDR"),
    ("avg_margin", "Avg Margin"),
]


def load_result(spec: str) -> dict:
    if "=" in spec:
        label, path = spec.split("=", 1)
    else:
        path = spec
        label = Path(path).stem
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    metrics = payload.get("metrics", payload)
    return {"label": label, "path": path, "metrics": metrics}


def fmt(value) -> str:
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([name for _, name in MAIN_COLUMNS])
        for row in rows:
            metrics = row["metrics"]
            writer.writerow(
                [
                    row["label"],
                    fmt(metrics["recall_at_1"]),
                    fmt(metrics["recall_at_5"]),
                    fmt(metrics["mrr"]),
                    fmt(metrics["fdr"]),
                    fmt(metrics["avg_margin"]),
                ]
            )


def markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] + ["---:"] * (len(headers) - 1)) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return lines


def write_markdown(path: Path, rows: list[dict]) -> None:
    main_rows = []
    for row in rows:
        metrics = row["metrics"]
        main_rows.append(
            [
                row["label"],
                fmt(metrics["recall_at_1"]),
                fmt(metrics["recall_at_5"]),
                fmt(metrics["mrr"]),
                fmt(metrics["fdr"]),
                fmt(metrics["avg_margin"]),
            ]
        )

    lines = ["# Reported evaluation results", ""]
    lines += markdown_table([name for _, name in MAIN_COLUMNS], main_rows)

    lines += ["", "## Results by observed difficulty", ""]
    for row in rows:
        lines += [f"### {row['label']}", ""]
        difficulty_rows = []
        for difficulty, metrics in row["metrics"].get("by_difficulty", {}).items():
            difficulty_rows.append(
                [
                    difficulty,
                    str(metrics["num_cases"]),
                    fmt(metrics["recall_at_1"]),
                    fmt(metrics["recall_at_5"]),
                    fmt(metrics["mrr"]),
                    fmt(metrics["fdr"]),
                    fmt(metrics["avg_margin"]),
                ]
            )
        lines += markdown_table(
            ["Difficulty", "Records", "Recall@1", "Recall@5", "MRR@10", "FDR", "Avg Margin"],
            difficulty_rows,
        )
        lines.append("")

    lines += ["## FDR by recorded task category", ""]
    for row in rows:
        axis_rows = []
        for axis, metrics in row["metrics"].get("axis_fdr", {}).items():
            num_cases = metrics.get("num_cases", metrics.get("num_pairs", ""))
            axis_rows.append([axis, str(num_cases), fmt(metrics["fdr"])])
        lines += [f"### {row['label']}", ""]
        lines += markdown_table(["Recorded task category", "Records", "FDR"], axis_rows)
        lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="生成论文结果表")
    parser.add_argument("--input", action="append", required=True, help="LABEL=eval.json，可重复")
    parser.add_argument("--csv", default=str(TABLES_DIR / "results_table.csv"), help="主结果 CSV")
    parser.add_argument("--md", default=str(TABLES_DIR / "results_table.md"), help="Markdown 结果表")
    args = parser.parse_args()

    rows = [load_result(spec) for spec in args.input]
    write_csv(Path(args.csv), rows)
    write_markdown(Path(args.md), rows)
    print(f"wrote {args.csv}")
    print(f"wrote {args.md}")


if __name__ == "__main__":
    main()
