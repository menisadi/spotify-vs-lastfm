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

    # Standardize track titles
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
            replacements[item1] = item2

    # Apply replacements to both Series
    series1 = series1.replace(replacements)
    series2 = series2.replace(
        {v: k for k, v in replacements.items()}
    )  # Reverse replacements for series2

    return series1, series2


# Test the functions
if __name__ == "__main__":
    spotify_path = "./spotify.csv"
    lastfm_path = "./lastfm.csv"
    spotify_df, lastfm_df = read_lists(spotify_path, lastfm_path)

    # make_almost_identical(spotify_df["track"], lastfm_df["track"])

    spotify_list = spotify_df["track"].to_list()
    lastfm_list = lastfm_df["track"].to_list()

    def measure_runtime(func, list1, list2, name):
        start_time = time.time()
        func(list1, list2)
        end_time = time.time()
        runtime = end_time - start_time
        print(f"{name:<25} Runtime: {runtime:.4f} seconds")
        return runtime

    print("\nRuntime Comparison Test")
    print("-" * 50)
    print(
        f"Testing with {len(spotify_list)} Spotify tracks and {len(lastfm_list)} LastFM tracks\n"
    )

    # Test all three approaches
    runtime1 = measure_runtime(
        two_loops_approach, spotify_list, lastfm_list, "Two Loops Approach"
    )
    runtime2 = measure_runtime(
        pairwise_matrix_approach,
        spotify_list,
        lastfm_list,
        "Pairwise Matrix Approach",
    )
    runtime3 = measure_runtime(
        single_pass_approach, spotify_list, lastfm_list, "Single Pass Approach"
    )

    # Find the fastest approach
    runtimes = {
        "Two Loops": runtime1,
        "Pairwise Matrix": runtime2,
        "Single Pass": runtime3,
    }
    fastest = min(runtimes.items(), key=lambda x: x[1])

    print("\nResults Summary:")
    print("-" * 50)
    print(f"Fastest approach: {fastest[0]} ({fastest[1]:.4f} seconds)")
    print(f"Speed comparison (relative to fastest):")
    for approach, runtime in runtimes.items():
        ratio = runtime / fastest[1]
        print(f"{approach:<15} : {ratio:.2f}x slower")
