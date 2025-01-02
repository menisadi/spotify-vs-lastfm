class ListSimilarity:
    def __init__(self, list1, list2, rbo_p=0.9, lazy_compute=False):
        self.list1 = list1
        self.list2 = list2

    def rank_based_edit_distance(self, base_weights=None):
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
        penalty_rank = max(n, m) + 1  # Default rank for missing items

        # Initialize base cases
        for i in range(1, n + 1):
            dp[i][0] = dp[i - 1][0] + base_weights["deletion"] * penalty_rank
        for j in range(1, m + 1):
            dp[0][j] = dp[0][j - 1] + base_weights["insertion"] * penalty_rank

        # Fill the DP table
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                rank_a = rank1.get(self.list1[i - 1], penalty_rank)
                rank_b = rank2.get(self.list2[j - 1], penalty_rank)

                if self.list1[i - 1] == self.list2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = dp[i - 1][j - 1] + base_weights["substitution"] * abs(
                        rank_a - rank_b
                    )

                dp[i][j] = min(
                    dp[i][j], dp[i][j - 1] + base_weights["insertion"] * penalty_rank
                )
                dp[i][j] = min(
                    dp[i][j], dp[i - 1][j] + base_weights["deletion"] * penalty_rank
                )

                if (
                    i > 1
                    and j > 1
                    and self.list1[i - 1] == self.list2[j - 2]
                    and self.list1[i - 2] == self.list2[j - 1]
                ):
                    dp[i][j] = min(
                        dp[i][j], dp[i - 2][j - 2] + base_weights["transposition"]
                    )

        return dp[n][m]
