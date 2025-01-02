from scipy.stats import kendalltau, spearmanr
from editdistance import (
    eval as edit_distance_eval,
)


class ListSimilarity:
    def __init__(self, list1, list2, rbo_p=0.9, lazy_compute=False):
        """
        Initialize the ListSimilarity instance.

        Parameters:
            list1, list2: The lists to compare.
            rbo_p: The weight decay parameter for RBO.
            lazy_compute: If True, metrics are computed on demand instead of during initialization.
        """
        self.list1 = list1
        self.list2 = list2
        self.rbo_p = rbo_p
        self.lazy_compute = lazy_compute
        self.metrics = None if lazy_compute else self._compute_all()

    def _compute_all(self):
        """
        Compute all similarity metrics and store them in a dictionary.

        Returns:
            A dictionary of precomputed metrics.
        """
        return {
            "edit_distance": self.edit_distance(),
            "edit_distance_normalized": self.edit_distance_normalized(),
            # "rank_based_edit_distance": self.rank_based_edit_distance(),
            "kendall_tau": self.kendall_tau_distance(),
            "spearman_correlation": self.spearman_correlation(),
            "jaccard_similarity": self.jaccard_similarity(),
            "rbo": self.rbo(),
        }

    def _ensure_metrics(self):
        """
        Ensure metrics are computed if lazy_compute is enabled.
        """
        if self.metrics is None:
            self.metrics = self._compute_all()

    # FIX: this one isn't working properly. There are libraries which can be used instead of implementing by myself.
    def rank_based_edit_distance(self, base_weights=None):
        """
        Compute a rank-based weighted edit distance between two lists.
        Missing items are treated as if they are at the bottom of the other list.

        Parameters:
            base_weights: Base weights for operations:
                          {'insertion': float, 'deletion': float,
                           'substitution': float, 'transposition': float}
        Returns:
            Rank-based weighted edit distance.
        """
        if base_weights is None:
            base_weight = 1
            base_weights = {
                "insertion": base_weight * len(self.list1),
                "deletion": base_weight * len(self.list1),
                "substitution": 2 * base_weight * len(self.list1),
                "transposition": base_weight,
            }

        n, m = len(self.list1), len(self.list2)
        dp = [[float("inf")] * (m + 1) for _ in range(n + 1)]
        dp[0][0] = 0

        # Map items to ranks
        rank1 = {item: i for i, item in enumerate(self.list1)}
        rank2 = {item: i for i, item in enumerate(self.list2)}
        max_rank1, max_rank2 = n, m

        # Initialize base cases
        for i in range(1, n + 1):
            dp[i][0] = dp[i - 1][0] + base_weights["deletion"] * (max_rank2)
        for j in range(1, m + 1):
            dp[0][j] = dp[0][j - 1] + base_weights["insertion"] * (max_rank1)

        # Fill the DP table
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                rank_a = rank1.get(
                    self.list1[i - 1], max_rank2
                )  # Rank in list2 if missing
                rank_b = rank2.get(
                    self.list2[j - 1], max_rank1
                )  # Rank in list1 if missing

                if (
                    self.list1[i - 1] == self.list2[j - 1]
                ):  # No cost if items are the same
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    # Substitution
                    dp[i][j] = dp[i - 1][j - 1] + base_weights["substitution"] * abs(
                        rank_a - rank_b
                    )

                # Insertion
                dp[i][j] = min(
                    dp[i][j], dp[i][j - 1] + base_weights["insertion"] * rank_b
                )
                # Deletion
                dp[i][j] = min(
                    dp[i][j], dp[i - 1][j] + base_weights["deletion"] * rank_a
                )

                # Transposition (swap adjacent elements)
                if (
                    i > 1
                    and j > 1
                    and self.list1[i - 1] == self.list2[j - 2]
                    and self.list1[i - 2] == self.list2[j - 1]
                ):
                    dp[i][j] = min(
                        dp[i][j],
                        dp[i - 2][j - 2]
                        + base_weights["transposition"] * abs(rank_a - rank_b),
                    )

        return dp[n][m]

    def edit_distance(self):
        """
        Compute the edit distance between two lists.
        """
        return edit_distance_eval(self.list1, self.list2)

    def edit_distance_normalized(self):
        """
        Compute the normalized edit distance between two lists.
        """
        distance = self.edit_distance()
        max_length = max(len(self.list1), len(self.list2))
        return distance / max_length if max_length > 0 else 0

    def kendall_tau_distance(self) -> float:
        """
        Compute Kendall Tau distance between two lists.
        """
        rank1 = {item: i for i, item in enumerate(self.list1)}
        rank2 = {item: i for i, item in enumerate(self.list2)}
        common_items = set(self.list1) | set(self.list2)
        ranks1 = [rank1.get(item, -1) for item in common_items]
        ranks2 = [rank2.get(item, -1) for item in common_items]
        tau, _ = kendalltau(ranks1, ranks2)
        return tau

    def spearman_correlation(self) -> float:
        """
        Compute Spearman rank correlation between two lists.
        """

        rank1 = {item: i for i, item in enumerate(self.list1)}
        rank2 = {item: i for i, item in enumerate(self.list2)}
        common_items = set(self.list1) | set(self.list2)
        ranks1 = [rank1.get(item, -1) for item in common_items]
        ranks2 = [rank2.get(item, -1) for item in common_items]
        spear_corr, _ = spearmanr(ranks1, ranks2)
        return spear_corr

    def jaccard_similarity(self):
        """
        Compute Jaccard similarity between two lists.
        """
        set1, set2 = set(self.list1), set(self.list2)
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union != 0 else 0

    def rbo(self):
        """
        Compute Rank-Biased Overlap (RBO) between two lists.
        """

        def overlap_at_depth(depth):
            return len(set(self.list1[:depth]) & set(self.list2[:depth])) / depth

        k = min(len(self.list1), len(self.list2))
        score = 0
        for d in range(1, k + 1):
            overlap = overlap_at_depth(d)
            score += (1 - self.rbo_p) * (self.rbo_p ** (d - 1)) * overlap
        return score

    def composite_score(self, weights=None):
        """
        Compute a composite similarity score for two lists.

        Parameters:
            weights: A dictionary of weights for the metrics.

        Returns:
            A composite similarity score between 0 and 1.
        """
        self._ensure_metrics()
        if weights is None:
            weights = {
                "jaccard": 0.3,
                "rbo": 0.3,
                "spearman": 0.2,
                "kendall": 0.1,
                "edit_distance": 0.1,
            }

        metrics = self.metrics
        assert metrics is not None, "Metrics have not been computed yet"

        return (
            weights["jaccard"] * metrics["jaccard_similarity"]
            + weights["rbo"] * metrics["rbo"]
            + weights["spearman"] * max(0, metrics["spearman_correlation"])
            + weights["kendall"] * max(0, metrics["kendall_tau"])
            + weights["edit_distance"] * (1 - metrics["edit_distance_normalized"])
        )
