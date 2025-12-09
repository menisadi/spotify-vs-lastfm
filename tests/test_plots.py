import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import plots  # noqa: E402


def test_rank_alignment_matrix_runs(monkeypatch):
    monkeypatch.setattr(plt, "show", lambda *_, **__: None)

    reference = ["Alpha", "Beta", "Gamma", "Delta"]
    comparisons = [
        ("List B", ["Alpha", "Gamma", "Beta", "Epsilon"]),
        ("List C", ["Delta", "Beta", "Alpha", "Zeta"]),
    ]

    assert plots.rank_alignment_matrix(reference, comparisons, top_k=4) is None
