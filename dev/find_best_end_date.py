import argparse
from dataclasses import dataclass

import pandas as pd

from compare import ListSimilarity
from main import fix_names, standardize_title


@dataclass
class BestResult:
    date: pd.Timestamp
    score: float


def _normalize_spotify_list(spotify_path: str) -> pd.DataFrame:
    spotify_df = pd.read_csv(spotify_path)
    spotify_df["track"] = spotify_df["track"].apply(standardize_title)
    return spotify_df[["track"]].copy()


def _top_tracks_up_to(raw_df: pd.DataFrame, end_date) -> pd.DataFrame:
    filtered = raw_df[raw_df["date"] <= end_date]
    top_tracks = filtered["master_metadata_track_name"].value_counts().head(100)
    return pd.DataFrame({"track": [standardize_title(t) for t in top_tracks.index]})


def _score_for_metric(metric: str, list1: list[str], list2: list[str]) -> float:
    similarity = ListSimilarity(list1, list2, lazy_compute=False)
    match metric:
        case "spearman":
            return similarity.spearman_correlation()
        case "kendall":
            return similarity.kendall_tau_distance()
        case "rbo":
            return similarity.rbo()
        case "jaccard":
            return similarity.jaccard_similarity()
        case _:
            raise ValueError(f"Unsupported metric: {metric}")


def find_best_end_date(
    spotify_path: str,
    raw_path: str,
    metric: str,
) -> tuple[BestResult, list[tuple[pd.Timestamp, float]]]:
    spotify_df = _normalize_spotify_list(spotify_path)

    raw_df = pd.read_csv(raw_path)
    raw_df["ts"] = pd.to_datetime(raw_df["ts"])
    raw_df["date"] = raw_df["ts"].dt.date

    unique_dates = sorted(raw_df["date"].unique())

    best = BestResult(date=unique_dates[0], score=float("-inf"))
    scores: list[tuple[pd.Timestamp, float]] = []

    for current_date in unique_dates:
        top_df = _top_tracks_up_to(raw_df, current_date)
        sp_df, top_df = fix_names(spotify_df.copy(), top_df)
        score = _score_for_metric(
            metric, sp_df["track"].to_list(), top_df["track"].to_list()
        )
        scores.append((current_date, score))
        if score > best.score:
            best = BestResult(date=current_date, score=score)

    return best, scores


def main():
    parser = argparse.ArgumentParser(
        description="Find end date that maximizes a comparison metric."
    )
    parser.add_argument(
        "--spotify",
        default="data/spotify25.csv",
        help="path to Spotify top tracks CSV",
    )
    parser.add_argument(
        "--raw",
        default="data/spotify_from_extened_data_2025_raw.csv",
        help="path to raw extended history CSV",
    )
    parser.add_argument(
        "--metric",
        choices=["spearman", "kendall", "rbo", "jaccard"],
        default="spearman",
        help="comparison metric to maximize",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=5,
        help="show top N dates by score",
    )
    args = parser.parse_args()

    best, scores = find_best_end_date(args.spotify, args.raw, args.metric)
    print(f"Best {args.metric}: {best.score:.4f} on {best.date}")

    top_scores = sorted(scores, key=lambda x: x[1], reverse=True)[: args.top_n]
    print(f"Top {len(top_scores)}:")
    for date, score in top_scores:
        print(date, f"{score:.4f}")


if __name__ == "__main__":
    main()
