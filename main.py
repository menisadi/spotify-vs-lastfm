import argparse
from string import capwords
import pandas as pd
from compare import ListSimilarity
import plots


def standardize_title(title: str) -> str:
    """Convert a track title to standard title case format."""
    return capwords(title.strip())


def read_lists(first_path: str, second_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    sdf = pd.read_csv(first_path)
    ldf = pd.read_csv(second_path)

    sdf["track"] = sdf["track"].apply(standardize_title)
    ldf["track"] = ldf["track"].apply(standardize_title)

    sdf, ldf = fix_names(sdf, ldf)

    return sdf, ldf


def filter_alphanumeric(input_string):
    return "".join(char for char in input_string if char.isalnum())


def fix_names(first_df, second_df):
    first_df["stripped_track"] = first_df["track"].apply(filter_alphanumeric)
    second_df["stripped_track"] = second_df["track"].apply(filter_alphanumeric)

    convert_dict = (
        second_df[["track", "stripped_track"]]
        .merge(
            first_df[["track", "stripped_track"]],
            on="stripped_track",
            suffixes=("_second", "_first"),
        )
        .drop("stripped_track", axis=1)
        .set_index("track_second")
        .to_dict()["track_first"]
    )

    second_df["track"] = second_df["track"].replace(convert_dict)

    return first_df, second_df


def print_diffs(
    first_list,
    second_list,
    first_name: str = "First List",
    second_name: str = "Second List",
):
    first_only = set(first_list) - set(second_list)
    second_only = set(second_list) - set(first_list)

    first_only_list = [song for song in first_list if song in first_only]
    second_only_list = [song for song in second_list if song in second_only]

    max_length = max(len(first_only_list), len(second_only_list))

    # Extend shorter list with empty strings to align columns
    first_only_list += [""] * (max_length - len(first_only_list))
    second_only_list += [""] * (max_length - len(second_only_list))

    print(f"{first_name:<40} {second_name}")
    print("-" * 80)

    for first_song, second_song in zip(first_only_list, second_only_list):
        print(f"{first_song:<40} {second_song}")


def print_diffs_old(
    first_list,
    second_list,
    first_name: str = "First List",
    second_name: str = "Second List",
):
    first_only = set(first_list) - set(second_list)
    print(f"Songs only in {first_name}:")
    for song in first_list:
        if song in first_only:
            print(f"{song} (index: {first_list.index(song)})")

    print()

    second_only = set(second_list) - set(first_list)
    print(f"Songs only in {second_name}:")
    for song in second_list:
        if song in second_only:
            print(f"{song} (index: {second_list.index(song)})")


def main(
    first_path,
    second_path,
    first_title="First List",
    second_title="Second List",
    print_sim_score=True,
    print_diff=False,
    plot_top_chart=False,
    rbo_p=0.9,
):
    first_df, second_df = read_lists(first_path, second_path)

    first_list = first_df["track"].to_list()
    second_list = second_df["track"].to_list()

    if print_sim_score:
        similarity = ListSimilarity(
            first_list, second_list, rbo_p=rbo_p, lazy_compute=False
        )
        for metric, score in similarity.metrics.items():
            print(f"{metric}: {score:.3f}")

        composite = similarity.composite_score()
        print(f"\nComposite Score: {round(100 * composite)}%")

    if print_diff:
        print_diffs(
            first_list, second_list, first_name=first_title, second_name=second_title
        )

    if plot_top_chart:
        plots.connection_graph(
            first_list,
            second_list,
            top_k=20,
            list1_title=first_title,
            list2_title=second_title,
            main_title="Top Tracks According to\n\n",
            xkcd=False,  # should the plot be in XKCD style or not
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""""
        Comparing two lists (from csv source for now).
        Used for now to com to compare track from lists of top-tracks, from different sources."""
    )  # TODO: allow for txt input
    parser.add_argument(
        "-f",
        "--first",
        type=str,
        help="path to first CSV file",
    )
    parser.add_argument(
        "-s",
        "--second",
        type=str,
        help="path to second CSV file",
    )
    parser.add_argument(
        "-t",
        "--first-title",
        type=str,
        help="title for the first list",
    )
    parser.add_argument(
        "-y",
        "--second-title",
        type=str,
        help="title for the second list",
    )
    parser.add_argument(
        "--no-sim",
        action="store_false",
        dest="print_sim_score",
        help="disable similarity score output",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        dest="print_diff",
        help="show differences between playlists",
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        dest="plot_top_chart",
        help="generate connection graph visualization",
    )
    parser.add_argument(
        "--rbo-p",
        type=float,
        default=0.9,
        help="RBO similarity parameter p (default: 0.9)",
    )
    args = parser.parse_args()

    main(
        first_path=args.first,
        second_path=args.second,
        first_title=args.first_title,
        second_title=args.second_title,
        print_sim_score=args.print_sim_score,
        print_diff=args.print_diff,
        plot_top_chart=args.plot_top_chart,
        rbo_p=args.rbo_p,
    )
