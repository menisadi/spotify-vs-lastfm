def rbo(list1, list2, p=0.9):
    """
    Compute Rank-Biased Overlap (RBO) between two lists.

    Parameters:
        list1, list2: The ranked lists to compare (order matters).
        p: Weight decay parameter (default: 0.9).

    Returns:
        A similarity score between 0 and 1.
    """

    def overlap_at_depth(list1, list2, depth):
        return len(set(list1[:depth]) & set(list2[:depth])) / depth

    # Length of the shorter list
    k = min(len(list1), len(list2))
    score = 0

    for d in range(1, k + 1):
        overlap = overlap_at_depth(list1, list2, d)
        score += (1 - p) * (p ** (d - 1)) * overlap

    return score


def almost_same(string1, string2):
    """
    Check if two strings are almost the same by matching every character
    up to one symbolic character.

    Parameters:
        string1 (str): The first string.
        string2 (str): The second string.

    Returns:
        bool: True if the strings match ignoring one symbolic character, otherwise False.
    """
    SYMBOLS = {"-", "'", '"', "_", ".", ",", "!", "?", " "}

    def normalize(s):
        return "".join(c for c in s if c not in SYMBOLS)

    normalized1 = normalize(string1)
    normalized2 = normalize(string2)

    return normalized1 == normalized2
