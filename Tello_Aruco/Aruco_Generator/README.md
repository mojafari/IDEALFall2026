# ArUco Marker Generator

`generate_single_aruco_page.py` creates printable ArUco markers, one large marker per letter-sized PDF page. Big, high-contrast markers are much easier for the Tello's camera to detect from a distance.

> Ready-made markers for IDs 0–4 are already in [`Sample_Aruco/`](Sample_Aruco). You only need this script if you want different IDs, a different dictionary, or a different marker size.

## Files

| File | Purpose |
| :--- | :--- |
| `generate_single_aruco_page.py` | Generates one PDF per marker ID. |
| `requirements.txt` | Python packages needed by the script. |
| `Sample_Aruco/` | Pre-generated markers for IDs 0–4. |

## Setup

Use the course virtual environment (`.venv`). From the repository root:

```sh
pip install -r Tello_Aruco/Aruco_Generator/requirements.txt
```

## Usage

1. Open `generate_single_aruco_page.py`.
2. In the `if __name__ == "__main__":` block, set the IDs you want:

   ```python
   dictionary_name = "DICT_4X4_50"
   ids = [0, 1, 2, 3, 4, 5]   # add 5 for a new command
   ```

3. Run the script. In PyCharm, right-click the file → **Run**. Or, from this folder:

   ```sh
   python generate_single_aruco_page.py
   ```

## Output

One PDF per ID, named `aruco_marker_<ID>.pdf` (for example `aruco_marker_5.pdf`). Files are saved in the folder the script is run from, which is this folder when you run it from PyCharm.

Each marker is printed 6 inches wide and centered on the page, with its ID written underneath. To make the markers bigger or smaller, change `marker_size_in` in the script.

## Things to Keep in Mind

* The dictionary here **must match** the dictionary in `test_Aruco.py` (`DICT_4X4_50`). A marker from a different dictionary will not be recognized.
* Print at 100% scale ("Actual size"), not "Fit to page", and keep the white margin around the marker.
* Matte paper works better than glossy paper, which reflects light.

## License

This project is open-source and available under the [MIT License](../LICENSE.md).
