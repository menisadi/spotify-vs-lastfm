import argparse
from pathlib import Path
import pandas as pd

from compare import ListSimilarity
from main import read_lists


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
    column_order = [
        "second",
        "edit_distance",
        "edit_distance_normalized",
        "bubblesort_distance",
        "kendall_tau",
        "spearman_correlation",
        "jaccard_similarity",
        "rbo",
        "composite_score",
        "composite_percent",
    ]

    frame = pd.DataFrame(results)
    frame = frame[column_order]

    def fmt_float(value: float) -> str:
        return "-" if pd.isna(value) else f"{value:.3f}"

    formatters = {
        "edit_distance": lambda v: "-" if pd.isna(v) else f"{int(v)}",
        "edit_distance_normalized": fmt_float,
        "bubblesort_distance": fmt_float,
        "kendall_tau": fmt_float,
        "spearman_correlation": fmt_float,
        "jaccard_similarity": fmt_float,
        "rbo": fmt_float,
        "composite_score": fmt_float,
        "composite_percent": lambda v: "-" if pd.isna(v) else f"{v:.0f}%",
    }

    return frame.to_string(index=False, formatters=formatters)


def main(first: str, seconds: list[str], rbo_p: float) -> None:
    results = []
    for second_path in seconds:
        comparison = compare_pair(first, second_path, rbo_p=rbo_p)
        comparison["second"] = Path(second_path).name
        results.append(comparison)

    print(format_table(results))


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
    args = parser.parse_args()

    main(first=args.first, seconds=args.seconds, rbo_p=args.rbo_p)
