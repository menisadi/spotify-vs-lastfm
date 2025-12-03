# Spotify vs Last.fm Playlist Analyzer

This project allows you to compare top songs from two different sources, such as Spotify Wrapped and Last.fm scrobbling data. It calculates similarity metrics, highlights differences, and visualizes connections between the playlists.

## Features

- **Similarity Metrics**:
  - Edit Distance (absolute and normalized)
  - Jaccard Similarity
  - Rank-Biased Overlap (RBO)
  - Kendall Tau Distance
  - Spearman Correlation
  - Composite Similarity Score
- **Differences**: Identify songs unique to each playlist.
- **Visualization**: Generate connection graphs to show overlap and differences in ranked top tracks.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Required packages:
  - `scipy`
  - `editdistance`
  - `matplotlib`
  - `pandas`

Install dependencies with:
```bash
pip install -r requirements.txt
```

### Usage

#### CLI Usage
Run the script using the following command:
```bash
python main.py --first <path_to_first_csv> --second <path_to_second_csv>
```

Additional options:
- `--first-title`: Title for the first playlist.
- `--second-title`: Title for the second playlist.
- `--no-sim`: Disable similarity score output.
- `--diff`: Show differences between playlists.
- `--plot`: Generate a connection graph visualization.
- `--rbo-p`: Set the RBO similarity parameter (default: 0.9).

#### CSV Format
Input CSV files must have a `track` column containing the track names. Other columns will be ignored.

#### Example
To compare two playlists with visualization:
```bash
python main.py --first spotify_top.csv --second lastfm_top.csv --plot
```

#### Compare Against Multiple Playlists
Use `multi_compare.py` to compare one reference list against several targets (no plotting):
```bash
python multi_compare.py --first spotify_top.csv --seconds lastfm_top.csv apple_top.csv yt_music.csv
```
Flags:
- `--first`: Reference CSV with a `track` column.
- `--seconds`: One or more CSVs to compare against the reference.
- `--rbo-p`: Optional RBO similarity parameter (default: 0.9).

### Code Structure
- **`compare.py`**: Contains the `ListSimilarity` class for computing metrics and scores.
- **`main.py`**: CLI interface for data input, processing, and analysis.
- **`multi_compare.py`**: Compare one list to many and print a table of metrics.
- **`plots.py`**: Functions for creating visualizations, such as connection graphs.

### Outputs
1. **Similarity Scores**: Various metrics and a composite score.
2. **Differences**: A side-by-side list of unique tracks.
3. **Connection Graphs**: Visual depiction of similarities and differences.

## Future Enhancements
- Support for `.txt` inputs.
- Enhanced matching for tracks with minor discrepancies in titles.

## License
This project is open-source and available under the [MIT License](LICENSE).

---

Contributions and feedback are welcome!
