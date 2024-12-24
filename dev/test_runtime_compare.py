from os import close
import time
from string import capwords
import editdistance
import pandas as pd


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

    return sdf, ldf


# Approach 1: Two-Loops Approach
def two_loops_approach(list1, list2):
    closest_list1_to_list2 = {}
    closest_list2_to_list1 = {}

    # Find closest matches for list1 → list2
    for item1 in list1:
        closest_match = min(list2, key=lambda item2: editdistance.eval(item1, item2))
        distance = editdistance.eval(item1, closest_match)
        closest_list1_to_list2[item1] = (closest_match, distance)

    # Find closest matches for list2 → list1
    for item2 in list2:
        closest_match = min(list1, key=lambda item1: editdistance.eval(item2, item1))
        distance = editdistance.eval(item2, closest_match)
        closest_list2_to_list1[item2] = (closest_match, distance)

    return closest_list1_to_list2, closest_list2_to_list1


# Approach 2: Pairwise Distance Matrix with DataFrame
def pairwise_matrix_approach(list1, list2):
    distances = []
    for item1 in list1:
        for item2 in list2:
            distance = editdistance.eval(item1, item2)
            distances.append((item1, item2, distance))

    df = pd.DataFrame(distances, columns=["list1_item", "list2_item", "distance"])

    # Find closest matches for list1 → list2
    closest_list1_to_list2 = (
        df.loc[df.groupby("list1_item")["distance"].idxmin()]
        .set_index("list1_item")[["list2_item", "distance"]]
        .to_dict(orient="index")
    )

    # Find closest matches for list2 → list1
    closest_list2_to_list1 = (
        df.loc[df.groupby("list2_item")["distance"].idxmin()]
        .set_index("list2_item")[["list1_item", "distance"]]
        .to_dict(orient="index")
    )

    return closest_list1_to_list2, closest_list2_to_list1


# Approach 3: Optimized Single Pass
def single_pass_approach(list1, list2):
    closest_list1_to_list2 = {}
    closest_list2_to_list1 = {}

    for item1 in list1:
        for item2 in list2:
            distance = editdistance.eval(item1, item2)

            # Update closest match for list1 → list2
            if (
                item1 not in closest_list1_to_list2
                or distance < closest_list1_to_list2[item1][1]
            ):
                closest_list1_to_list2[item1] = (item2, distance)

            # Update closest match for list2 → list1
            if (
                item2 not in closest_list2_to_list1
                or distance < closest_list2_to_list1[item2][1]
            ):
                closest_list2_to_list1[item2] = (item1, distance)

    return closest_list1_to_list2, closest_list2_to_list1


def make_almost_identical(series1, series2):
    # Convert Series to list for processing
    list1 = series1.tolist()
    list2 = series2.tolist()

    # Get closest matches using the provided function
    closest_list1_to_list2, closest_list2_to_list1 = single_pass_approach(list1, list2)

    # Build a mapping for replacements (only for distances 1 or 2)
    replacements = {}
    for item1, (item2, distance) in closest_list1_to_list2.items():
        if 0 < distance <= 2:
            print(item1)
            replacements[item1] = item2

    # Apply replacements to both Series
    series1 = series1.replace(replacements)
    series2 = series2.replace(
        {v: k for k, v in replacements.items()}
    )  # Reverse replacements for series2

    return series1, series2


def filter_alphanumeric(input_string):
    return "".join(char for char in input_string if char.isalnum())


# Test the functions
if __name__ == "__main__":
    spotify_path = "./spotify.csv"
    lastfm_path = "./lastfm.csv"
    spotify_df, lastfm_df = read_lists(spotify_path, lastfm_path)
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

    closest_list1_to_list2, closest_list2_to_list1 = single_pass_approach(
        spotify_df["track"].to_list(), lastfm_df["track"].to_list()
    )

    for item1, (item2, d) in closest_list1_to_list2.items():
        if 0 < d <= 2:
            print(f"{item1} -> {item2}")

    print("Fixing!")
    lastfm_df["track"] = lastfm_df["track"].replace(convert_dict)
    # spotify_df["track"].replace(convert_dict)

    closest_list1_to_list2, closest_list2_to_list1 = single_pass_approach(
        spotify_df["track"].to_list(), lastfm_df["track"].to_list()
    )

    for item1, (item2, d) in closest_list1_to_list2.items():
        if 0 < d <= 2:
            print(f"{item1} -> {item2}")
