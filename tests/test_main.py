from main import read_lists, standardize_title


def test_standardize_title_capwords():
    assert standardize_title("  sOmE song  ") == "Some Song"


def test_read_lists_aligns_names(tmp_path):
    first_csv = tmp_path / "first.csv"
    second_csv = tmp_path / "second.csv"

    first_csv.write_text("track\nhello world\nAnother Song\n")
    second_csv.write_text("track\nHello World!!!\nAnother Song\n")

    first_df, second_df = read_lists(str(first_csv), str(second_csv))

    assert list(first_df["track"]) == ["Hello World", "Another Song"]
    assert list(second_df["track"]) == ["Hello World", "Another Song"]
