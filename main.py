import argparse
from string import capwords
from matplotlib.pyplot import plot_date
import pandas as pd
import compare
import plots


def standardize_title(title: str) -> str:
    """Convert a track title to standard title case format."""
    return capwords(title.strip())


def read_lists(
    spotify_path: str, lastfm_path: str
) -> tuple[pd.DataFrame, pd.DataFrame]:
    sdf = pd.read_csv(spotify_path)
    ldf = pd.read_csv(lastfm_path)

    sdf["track"] = sdf["track"].apply(standardize_title)
    ldf["track"] = ldf["track"].apply(standardize_title)

    sdf, ldf = fix_names(sdf, ldf)

    return sdf, ldf


def filter_alphanumeric(input_string):
    return "".join(char for char in input_string if char.isalnum())


def fix_names(spotify_df, lastfm_df):
    spotify_df["stripped_track"] = spotify_df["track"].apply(filter_alphanumeric)
    lastfm_df["stripped_track"] = lastfm_df["track"].apply(filter_alphanumeric)

    convert_dict = (
        lastfm_df[["track", "stripped_track"]]
        .merge(
            spotify_df[["track", "stripped_track"]],
            on="stripped_track",
            suffixes=("_last", "_spot"),
        )
        .drop("stripped_track", axis=1)
        .set_index("track_last")
        .to_dict()["track_spot"]
    )

    lastfm_df["track"] = lastfm_df["track"].replace(convert_dict)

    return spotify_df, lastfm_df


def print_diffs(spotify_list, lastfm_list):
    spotify_only = set(spotify_list) - set(lastfm_list)
    print("Songs only in Spotify:")
    for song in spotify_list:
        if song in spotify_only:
            print(f"{song} (index: {spotify_list.index(song)})")

    print()

    lastfm_only = set(lastfm_list) - set(spotify_list)
    print("Songs only in Last.FM:")
    for song in lastfm_list:
        if song in lastfm_only:
            print(f"{song} (index: {lastfm_list.index(song)})")


def main(print_sim_score=True, print_diff=False, plot_top_chart=False):
    spotify_path = "data/spotify.csv"
    lastfm_path = "data/lastfm.csv"
    spotify_df, lastfm_df = read_lists(spotify_path, lastfm_path)

    spotify_list = spotify_df["track"].to_list()
    lastfm_list = lastfm_df["track"].to_list()

    if print_sim_score:
        similarity = compare.rbo(spotify_list, lastfm_list, p=0.9)
        print(f"RBO Similarity: {similarity:.3f}\n")

    if print_diff:
        print_diffs(spotify_list, lastfm_list)

    if plot_top_chart:
        plots.connection_graph(
            spotify_list,
            lastfm_list,
            top_k=20,
            list1_title="Spotify",
            list2_title="Last.FM",
            xkcd=False,  # should the plot be in XKCD style or not
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare Spotify and Last.FM playlists"
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
    args = parser.parse_args()

    main(
        print_sim_score=args.print_sim_score,
        print_diff=args.print_diff,
        plot_top_chart=args.plot_top_chart,
    )
