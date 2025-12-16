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
            "bubblesort_distance": self.bubblesort_distance(),
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

    def _aligned_ranks(self) -> tuple[list[int], list[int]]:
        """
        Build aligned rank vectors over the union of items.

        Items appear in the order of list1 first, then any unseen items from list2.
        Missing items in each list get unique tail ranks so there are no ties.
        """

        def ranks(primary: list, secondary: list, universe: list) -> list[int]:
            base = {item: idx for idx, item in enumerate(primary)}
            tail_start = len(primary)
            for offset, item in enumerate(x for x in secondary if x not in base):
                base[item] = tail_start + offset
            return [base[item] for item in universe]

        universe = list(dict.fromkeys([*self.list1, *self.list2]))
        return (
            ranks(self.list1, self.list2, universe),
            ranks(self.list2, self.list1, universe),
        )

    def bubblesort_distance(self) -> float:
        """
        Calculate the normalized bubblesort distance between two lists.

        Uses Kendall Tau on aligned rank vectors; missing items are treated as
        appearing after known items in the list where they are absent.
        """
        ranks1, ranks2 = self._aligned_ranks()
        kt_corr, _ = kendalltau(ranks1, ranks2)
        if kt_corr is None:
            return 0.0
        return (1 - kt_corr) / 2

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
        ranks1, ranks2 = self._aligned_ranks()
        tau, _ = kendalltau(ranks1, ranks2)
        return 0.0 if tau is None else tau

    def spearman_correlation(self) -> float:
        """
        Compute Spearman rank correlation between two lists.
        """

        ranks1, ranks2 = self._aligned_ranks()
        spear_corr, _ = spearmanr(ranks1, ranks2)
        return 0.0 if spear_corr is None else spear_corr

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
