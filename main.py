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

    # Standardize track titles
    sdf["track"] = sdf["track"].apply(standardize_title)
    ldf["track"] = ldf["track"].apply(standardize_title)

    return sdf, ldf

    return sdf, ldf


def main():
    spotify_path = "./spotify.csv"
    lastfm_path = "./lastfm.csv"
    spotify_df, lastfm_df = read_lists(spotify_path, lastfm_path)

    spotify_list = spotify_df["track"].to_list()
    lastfm_list = lastfm_df["track"].to_list()

    similarity = compare.rbo(spotify_list, lastfm_list, p=0.9)
    print(f"RBO Similarity: {similarity:.3f}")

    top_k_to_plot = 20
    plots.connection_graph(
        spotify_list[:top_k_to_plot],
        lastfm_list[:top_k_to_plot],
        list1_title="Spotify",
        list2_title="Last.FM",
    )


if __name__ == "__main__":
    main()
