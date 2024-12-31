from scipy.stats import kendalltau, spearmanr
import editdistance
from difflib import SequenceMatcher


class ListSimilarity:
    @staticmethod
    def edit_distance(list1, list2):
        """
        Compute the edit distance between two lists.
        """
        return editdistance.eval(list1, list2)

    @staticmethod
    def edit_distance_normalized(list1, list2):
        """
        Compute the normalized edit distance between two lists.
        """
        distance = ListSimilarity.edit_distance(list1, list2)
        max_length = max(len(list1), len(list2))
        return distance / max_length if max_length > 0 else 0

    @staticmethod
    def kendall_tau_distance(list1, list2):
        """
        Compute Kendall Tau distance between two lists.
        """
        rank1 = {item: i for i, item in enumerate(list1)}
        rank2 = {item: i for i, item in enumerate(list2)}
        common_items = set(list1) | set(list2)
        ranks1 = [rank1.get(item, -1) for item in common_items]
        ranks2 = [rank2.get(item, -1) for item in common_items]
        return kendalltau(ranks1, ranks2).correlation

    @staticmethod
    def spearman_correlation(list1, list2):
        """
        Compute Spearman rank correlation between two lists.
        """
        rank1 = {item: i for i, item in enumerate(list1)}
        rank2 = {item: i for i, item in enumerate(list2)}
        common_items = set(list1) | set(list2)
        ranks1 = [rank1.get(item, -1) for item in common_items]
        ranks2 = [rank2.get(item, -1) for item in common_items]
        return spearmanr(ranks1, ranks2).correlation

    @staticmethod
    def jaccard_similarity(list1, list2):
        """
        Compute Jaccard similarity between two lists.
        """
        set1, set2 = set(list1), set(list2)
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union != 0 else 0

    @staticmethod
    def rbo(list1, list2, p=0.9):
        """
        Compute Rank-Biased Overlap (RBO) between two lists.
        """

        def overlap_at_depth(list1, list2, depth):
            return len(set(list1[:depth]) & set(list2[:depth])) / depth

        k = min(len(list1), len(list2))
        score = 0
        for d in range(1, k + 1):
            overlap = overlap_at_depth(list1, list2, d)
            score += (1 - p) * (p ** (d - 1)) * overlap
        return score

    @staticmethod
    def compute_all(list1, list2, rbo_p=0.9):
        """
        Compute all similarity metrics and return them as a dictionary.
        """
        return {
            "edit_distance_normalized": ListSimilarity.edit_distance_normalized(
                list1, list2
            ),
            "kendall_tau": ListSimilarity.kendall_tau_distance(list1, list2),
            "spearman_correlation": ListSimilarity.spearman_correlation(list1, list2),
            "jaccard_similarity": ListSimilarity.jaccard_similarity(list1, list2),
            "rbo": ListSimilarity.rbo(list1, list2, p=rbo_p),
        }

    @staticmethod
    def composite_score(list1, list2, weights=None, rbo_p=0.9):
        """
        Compute a composite similarity score for two lists.

        Parameters:
            list1, list2: The lists to compare.
            weights: A dictionary of weights for the metrics.
            rbo_p: The weight decay parameter for RBO.

        Returns:
            A composite similarity score between 0 and 1.
        """
        if weights is None:
            weights = {
                "jaccard": 0.3,
                "rbo": 0.3,
                "spearman": 0.2,
                "kendall": 0.1,
                "edit_distance": 0.1,
            }

        jaccard = ListSimilarity.jaccard_similarity(list1, list2)
        rbo = ListSimilarity.rbo(list1, list2, p=rbo_p)
        spearman = max(
            0, ListSimilarity.spearman_correlation(list1, list2)
        )  # Ensure non-negative
        kendall = max(
            0, ListSimilarity.kendall_tau_distance(list1, list2)
        )  # Ensure non-negative
        edit_distance_norm = 1 - ListSimilarity.edit_distance_normalized(list1, list2)

        score = (
            weights["jaccard"] * jaccard
            + weights["rbo"] * rbo
            + weights["spearman"] * spearman
            + weights["kendall"] * kendall
            + weights["edit_distance"] * edit_distance_norm
        )
        return score
