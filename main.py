from string import capwords
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


def main():
    spotify_path = "./spotify.csv"
    lastfm_path = "./lastfm.csv"
    spotify_df, lastfm_df = read_lists(spotify_path, lastfm_path)

    spotify_list = spotify_df["track"].to_list()
    lastfm_list = lastfm_df["track"].to_list()

    similarity = compare.rbo(spotify_list, lastfm_list, p=0.9)
    print(f"RBO Similarity: {similarity:.3f}")

    plots.connection_graph(
        spotify_list,
        lastfm_list,
        top_k=20,
        list1_title="Spotify",
        list2_title="Last.FM",
    )


if __name__ == "__main__":
    main()
