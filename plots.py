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


def rank_alignment_matrix(
    reference: list[str],
    comparisons: list[tuple[str, list[str]]],
    top_k: int = 50,
    missing_color: str = "#d9d9d9",
):
    """
    Visualize how multiple ranked lists align against a reference list using colors.

    Each comparison list is shown as a column, ordered by its own ranking. Cells are
    colored by how far the item's position deviates from the reference list: green
    means it appears in the same position, red means it is far away, and gray means
    the item is not present in the reference at all.
    """
    if not comparisons:
        return

    columns = [("Reference", reference), *comparisons]
    max_rows = min(top_k, max(len(lst) for _, lst in columns))
    if max_rows == 0:
        return

    cmap = plt.get_cmap("RdYlGn_r")  # green at 0, red at 1
    reference_positions = {name: idx for idx, name in enumerate(reference)}

    cell_text: list[list[str]] = []
    cell_colors: list[list[str | tuple[float, float, float, float]]] = []

    for row_idx in range(max_rows):
        text_row: list[str] = []
        color_row: list[str | tuple[float, float, float, float]] = []
        for col_idx, (label, items) in enumerate(columns):
            if row_idx < len(items):
                track = items[row_idx]
                prefix = f"{row_idx + 1}. " if col_idx == 0 else ""
                text_row.append(f"{prefix}{track}")
            else:
                track = ""
                text_row.append("")

            if col_idx == 0:
                color_row.append("white")
                continue

            if not track:
                color_row.append("white")
                continue

            ref_pos = reference_positions.get(track)
            if ref_pos is None:
                color_row.append(missing_color)
                continue

            diff = abs(ref_pos - row_idx)
            denominator = max(len(reference) - 1, 1)
            normalized = min(diff / denominator, 1.0)
            color_row.append(cmap(normalized))
        cell_text.append(text_row)
        cell_colors.append(color_row)

    fig_width = 3 + 2 * len(comparisons)
    fig_height = 0.35 * max_rows + 2
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis("off")

    table = ax.table(
        cellText=cell_text,
        cellColours=cell_colors,
        colLabels=[label for label, _ in columns],
        loc="center",
        cellLoc="left",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.1, 1.2)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=1))
    sm.set_array([])
    cbar = plt.colorbar(
        sm,
        ax=ax,
        fraction=0.046,
        pad=0.12,
        orientation="horizontal",
        location="top",
    )
    cbar.set_label("Rank difference vs reference (lower is closer)")

    ax.text(
        0.0,
        -0.08,
        "Gray cells: not present in reference list",
        transform=ax.transAxes,
        fontsize=8,
        va="top",
    )

    fig.tight_layout()
    plt.show()
