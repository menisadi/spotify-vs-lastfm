import matplotlib.pyplot as plt
from contextlib import contextmanager


@contextmanager
def optional_xkcd(enabled: bool):
    if enabled:
        with plt.xkcd():
            yield
    else:
        yield


def connection_graph(
    list1: list,
    list2: list,
    top_k: int = 20,
    list1_title: str = "",
    list2_title: str = "",
    main_title: str = "",
    xkcd: bool = False,
):
    """
    Draw a connection graph between two lists in XKCD style.

    Parameters:
        list1, list2: The two ordered lists to compare.
    """
    with optional_xkcd(xkcd):
        fig, ax = plt.subplots(figsize=(10, 6))

        list1_top_k = list1[:top_k]
        list2_top_k = list2[:top_k]
        positions1 = {item: len(list1_top_k) - i for i, item in enumerate(list1_top_k)}
        positions2 = {item: len(list2_top_k) - i for i, item in enumerate(list2_top_k)}

        all_items = set(list1_top_k).union(set(list2_top_k))
        in_both = set(list1).intersection(set(list2))
        disagree_tpp = set(list1_top_k).symmetric_difference(set(list2_top_k))
        disagree = set(list1).symmetric_difference(set(list2))
        colors_dict = {item: "black" for item in in_both}
        colors_dict.update({item: "blue" for item in disagree_tpp})
        colors_dict.update({item: "red" for item in disagree})

        if list1_title != "":
            ax.text(
                0,
                len(list1_top_k) + 2,
                list1_title,
                fontsize=15,
                ha="right",
                va="center",
            )
        for i, item in enumerate(list1_top_k):
            ax.text(
                0,
                len(list1_top_k) - i,
                item + " (" + str(i + 1) + ")",
                ha="right",
                va="center",
                fontsize=10,
                color=colors_dict[item],
            )
        if list2_title != "":
            ax.text(
                1,
                len(list2_top_k) + 2,
                list2_title,
                fontsize=15,
                ha="left",
                va="center",
            )
        for i, item in enumerate(list2_top_k):
            ax.text(
                1,
                len(list1_top_k) - i,
                "(" + str(i + 1) + ") " + item,
                ha="left",
                va="center",
                fontsize=10,
                color=colors_dict[item],
            )

        for item in all_items:
            if item in positions1 and item in positions2:
                ax.plot(
                    [0.03, 0.97],
                    [positions1[item], positions2[item]],
                    "k-",
                    alpha=0.7,
                )

        ax.set_xlim(-0.2, 1.2)
        ax.set_ylim(-1, max(len(list1_top_k), len(list2_top_k)))
        ax.axis("off")
        if main_title != "":
            ax.set_title(main_title, fontsize=14)

        plt.show()
