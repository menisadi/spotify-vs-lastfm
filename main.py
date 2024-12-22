import pandas as pd
import compare

# import plots


def read_lists(
    spotify_path: str, lastfm_path: str
) -> tuple[pd.DataFrame, pd.DataFrame]:
    sdf = pd.read_csv(spotify_path)
    ldf = pd.read_csv(lastfm_path)

    return sdf, ldf


def main():
    spotify_path = "./spotify.csv"
    lastfm_path = "./lastfm.csv"
    spotify_df, lastfm_df = read_lists(spotify_path, lastfm_path)

    spotify_list = spotify_df["track"].to_list()
    lastfm_list = lastfm_df["track"].to_list()

    similarity = compare.rbo(spotify_list, lastfm_list, p=0.9)
    print(f"RBO Similarity: {similarity:.3f}")


if __name__ == "__main__":
    main()
