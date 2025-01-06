import pandas as pd

from compare import ListSimilarity
from main import read_lists


def main():
    spotify_raw_path = "/users/meni/code/personal/lastVSspot/data/Spotify Extended Streaming History/audio_2024.csv"
    spotify_path = "./data/spotify.csv"
    lastfm_path = "./data/lastfm.csv"
    spotify_df, lastfm_df = read_lists(spotify_path, lastfm_path)
    spotify_list = spotify_df["track"].to_list()
    lastfm_list = lastfm_df["track"].to_list()

    spotify_raw_df = pd.read_csv(spotify_raw_path)

    spotify_raw_df["timestamp"] = pd.to_datetime(spotify_raw_df["timestamp"]).dt.date
    start_date = pd.to_datetime("2024-09-01").date()
    end_date = pd.to_datetime(("2024-12-05")).date()
    current_date = start_date

    scores = []
    dates = []
    while current_date <= end_date:
        filtered_df = spotify_raw_df[spotify_raw_df["timestamp"] <= current_date]
        top_tracks = filtered_df["track"].value_counts().head(100)
        top_tracks_list = top_tracks.reset_index()["track"].to_list()

        similarity = ListSimilarity(top_tracks_list, lastfm_list, lazy_compute=False)
        current_score = (
            similarity.bubblesort_distance()
        )  # TODO: which method should we use here?
        scores.append(current_score)
        dates.append(current_date)

        current_date += pd.to_timedelta("1d")

    min_score = min(scores)
    min_date = dates[scores.index(min_score)]
    print(f"Min: {min_score:.2f} on {min_date}")
    print(f"Mean: {sum(scores) / len(scores):.2f}")
    print(f"Max: {max(scores):.2f}")

    final_filtered_df = spotify_raw_df[spotify_raw_df["timestamp"] <= min_date]
    final_top_tracks = final_filtered_df["track"].value_counts().head(100)

    return final_top_tracks


if __name__ == "__main__":
    result_df = main()
    result_df.reset_index().to_csv("min_distance_spority.csv")
