import argparse
from pathlib import Path
import pandas as pd

from compare import ListSimilarity
from main import read_lists


COLUMNS = [
    ("second", "Target"),
    ("edit_distance", "Edit"),
    ("edit_distance_normalized", "Edit (norm)"),
    ("bubblesort_distance", "Bubblesort"),
    ("kendall_tau", "Kendall"),
    ("spearman_correlation", "Spearman"),
    ("jaccard_similarity", "Jaccard"),
    ("rbo", "RBO"),
    ("composite_score", "Composite"),
    ("composite_percent", "Composite %"),
]


def compare_pair(first_path: str, second_path: str, rbo_p: float) -> dict:
    first_df, second_df = read_lists(first_path, second_path)

    first_list = first_df["track"].to_list()
    second_list = second_df["track"].to_list()

    similarity = ListSimilarity(first_list, second_list, rbo_p=rbo_p, lazy_compute=False)
    metrics = dict(similarity.metrics)
    composite = similarity.composite_score()

    metrics["composite_score"] = composite
    metrics["composite_percent"] = composite * 100
    metrics["second"] = str(second_path)
    return metrics


def format_table(results: list[dict]) -> str:
    def format_value(key: str, value: float | str) -> str:
        if pd.isna(value):
            return "-"
        if key == "second":
            return str(value)
        if key == "edit_distance":
            return f"{int(value)}"
        if key == "composite_percent":
            return f"{value:.0f}%"
        return f"{value:.3f}"

    rows: list[list[str]] = []
    for entry in results:
        rows.append([format_value(key, entry.get(key)) for key, _ in COLUMNS])

    col_widths = []
    for idx, (_, header) in enumerate(COLUMNS):
        max_row_width = max((len(row[idx]) for row in rows), default=0)
        col_widths.append(max(len(header), max_row_width))

    header_line = " | ".join(
        (header.ljust(col_widths[idx]) if idx == 0 else header.rjust(col_widths[idx]))
        for idx, (_, header) in enumerate(COLUMNS)
    )
    separator = "-+-".join("-" * width for width in col_widths)

    body_lines = []
    for row in rows:
        body_lines.append(
            " | ".join(
                row[idx].ljust(col_widths[idx])
                if idx == 0
                else row[idx].rjust(col_widths[idx])
                for idx in range(len(COLUMNS))
            )
        )

    return "\n".join([header_line, separator, *body_lines])


def main(first: str, seconds: list[str], rbo_p: float, csv_path: str | None) -> None:
    results = []
    for second_path in seconds:
        comparison = compare_pair(first, second_path, rbo_p=rbo_p)
        comparison["second"] = Path(second_path).name
        results.append(comparison)

    print(format_table(results))

    if csv_path:
        frame = pd.DataFrame(results)
        frame = frame[[key for key, _ in COLUMNS]]
        frame.to_csv(csv_path, index=False)
        print(f"\nSaved CSV to {csv_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare one source list against multiple target lists."
    )
    parser.add_argument(
        "-f",
        "--first",
        required=True,
        help="path to the reference CSV file",
    )
    parser.add_argument(
        "-s",
        "--seconds",
        nargs="+",
        required=True,
        help="one or more CSV files to compare against the reference",
    )
    parser.add_argument(
        "--rbo-p",
        type=float,
        default=0.9,
        help="RBO similarity parameter p (default: 0.9)",
    )
    parser.add_argument(
        "--out-csv",
        dest="out_csv",
        help="Optional path to save the comparison table as CSV",
    )
    args = parser.parse_args()

    main(first=args.first, seconds=args.seconds, rbo_p=args.rbo_p, csv_path=args.out_csv)
