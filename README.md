# Playlist Similarity Tool

This tool compares two playlists from different sources (e.g., Spotify and Last.fm) and calculates their similarity. Currently, it uses the Rank-Biased Overlap (RBO) method for comparison, with plans to incorporate additional comparison methods in the future.

## Features
- **Compare playlists:** Reads playlist data from CSV files and calculates similarity between two lists of tracks.
- **Current similarity metric:** Rank-Biased Overlap (RBO) with customizable parameters.
- **Extensible design:** Plans to add more comparison methods in future updates.

## Requirements
- Python 3.10 or higher
- `pandas` library
- A `compare` module with an `rbo` function (used for RBO similarity calculation)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/playlist-similarity-tool.git
   cd playlist-similarity-tool
   ```
2. Install the required libraries:
   ```bash
   pip install pandas
   ```

## Usage
1. Prepare your data:
   - Save your playlists as CSV files with a column named `track` containing track names.
   - Example file structure:
     ```csv
     track
     Song A
     Song B
     Song C
     ```

2. Run the script:
   ```bash
   python main.py
   ```

   By default, it reads playlists from `spotify.csv` and `lastfm.csv` in the same directory.

3. View the output:
   The script calculates and displays the RBO similarity between the two playlists:
   ```
   RBO Similarity: 0.845
   ```

## Planned Features
- Add more similarity metrics, such as:
  - Jaccard similarity
  - Cosine similarity
  - Edit distance for track names
- Include data visualization for similarity analysis (e.g., charts and plots).

## Contributing
Feel free to contribute by submitting issues or pull requests. Future improvements and ideas are welcome!

## License
This project is licensed under the [MIT License](LICENSE).
