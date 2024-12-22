import matplotlib.pyplot as plt


def connection_graph(list1, list2):
    """
    Draw a connection graph between two lists.

    Parameters:
        list1, list2: The two ordered lists to compare.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create mappings for positions in each list
    positions1 = {item: i for i, item in enumerate(list1)}
    positions2 = {item: i for i, item in enumerate(list2)}

    # Combine all unique items
    all_items = set(list1).union(set(list2))

    # Plot source and target lists
    for i, item in enumerate(list1):
        ax.text(0, i, item, ha="right", va="center", fontsize=10, color="blue")
    for i, item in enumerate(list2):
        ax.text(1, i, item, ha="left", va="center", fontsize=10, color="green")

    # Draw connections
    for item in all_items:
        if item in positions1 and item in positions2:
            ax.plot(
                [0, 1], [positions1[item], positions2[item]], "k-", alpha=0.7
            )
        elif item in positions1:  # Item only in list1
            ax.plot([0, 1], [positions1[item], len(list2)], "r--", alpha=0.7)
        elif item in positions2:  # Item only in list2
            ax.plot([0, 1], [len(list1), positions2[item]], "r--", alpha=0.7)

    # Set axis limits and labels
    ax.set_xlim(-0.2, 1.2)
    ax.set_ylim(-1, max(len(list1), len(list2)))
    ax.axis("off")
    ax.set_title("Connection Graph Between Two Lists", fontsize=14)

    plt.show()
