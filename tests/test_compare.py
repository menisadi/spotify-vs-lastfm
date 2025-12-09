from pytest import approx
from compare import ListSimilarity


def test_identical_lists_scores_are_high():
    items = ["One", "Two", "Three", "Four", "Five"]
    similarity = ListSimilarity(items, items.copy(), rbo_p=0.9, lazy_compute=False)
    metrics = similarity.metrics

    assert metrics is not None
    assert metrics["edit_distance"] == 0
    assert metrics["edit_distance_normalized"] == approx(0.0, abs=1e-12)
    assert metrics["jaccard_similarity"] == approx(1.0)
    assert metrics["spearman_correlation"] == approx(1.0)
    assert metrics["kendall_tau"] == approx(1.0)
    assert similarity.composite_score() > 0.75


def test_composite_penalizes_reordering():
    base = ["a", "b", "c", "d", "e"]
    reversed_list = list(reversed(base))

    aligned = ListSimilarity(base, base.copy(), rbo_p=0.9, lazy_compute=False)
    reversed_similarity = ListSimilarity(
        base, reversed_list, rbo_p=0.9, lazy_compute=False
    )

    assert reversed_similarity.metrics is not None
    assert reversed_similarity.metrics["jaccard_similarity"] == 1.0
    assert reversed_similarity.metrics["kendall_tau"] < 1.0
    assert reversed_similarity.metrics["edit_distance_normalized"] > 0
    assert reversed_similarity.composite_score() < aligned.composite_score()
