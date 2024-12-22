import matplotlib.pyplot as plt


def connection_graph(
    list1: list, list2: list, list1_title: str = "", list2_title: str = ""
):
    """
    Draw a connection graph between two lists.

    Parameters:
        list1, list2: The two ordered lists to compare.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    positions1 = {item: len(list1) - i for i, item in enumerate(list1)}
    positions2 = {item: len(list2) - i for i, item in enumerate(list2)}

    all_items = set(list1).union(set(list2))
    in_both = set(list1).intersection(set(list2))
    disagree = set(list1).symmetric_difference(set(list2))
    colors_dict = {item: "black" for item in in_both}
    colors_dict.update({item: "red" for item in disagree})

    if list1_title != "":
        ax.text(
            0,
            len(list1) + 2,
            list1_title,
            fontsize=15,
            ha="right",
            va="center",
        )
    for i, item in enumerate(list1):
        ax.text(
            0,
            len(list1) - i,
            item + " (" + str(i + 1) + ")",
            ha="right",
            va="center",
            fontsize=10,
            color=colors_dict[item],
        )
    if list2_title != "":
        ax.text(
            1,
            len(list2) + 2,
            list2_title,
            fontsize=15,
            ha="left",
            va="center",
        )
    for i, item in enumerate(list2):
        ax.text(
            1,
            len(list1) - i,
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
    ax.set_ylim(-1, max(len(list1), len(list2)))
    ax.axis("off")
    # ax.set_title("Connection Graph Between Two Lists", fontsize=14)

    plt.show()
