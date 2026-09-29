# QR Code Generator

`generate_single_qr_page.py` creates printable QR codes, one large code per letter-sized PDF page. Big, sharp QR codes are much easier for the Tello's camera to read.

## Files

| File | Purpose |
| :--- | :--- |
| `generate_single_qr_page.py` | Generates one PDF per QR code. |
| `requirements.txt` | Python packages needed by the script. |

## Setup

Use the course virtual environment (`.venv`). From the repository root:

```sh
pip install -r Tello_QRCode/QRCode_Generator/requirements.txt
```

## Usage

1. Open `generate_single_qr_page.py`.
2. In the `if __name__ == "__main__":` block, edit the `commands` dictionary. Each line is **text to put in the QR code** → **PDF file name**:

   ```python
   commands = {
       "flip_forward": "qr_flip_forward.pdf",
       "flip_back": "qr_flip_back.pdf",
       "flip_left": "qr_flip_left.pdf",
       "flip_right": "qr_flip_right.pdf",
       "stop": "qr_stop.pdf",
   }
   ```

3. Run the script. In PyCharm, right-click the file → **Run**. Or, from this folder:

   ```sh
   python generate_single_qr_page.py
   ```

## Output

One PDF per entry in `commands` (for example `qr_stop.pdf`), saved in the folder the script is run from, which is this folder when you run it from PyCharm. Each QR code fills most of a letter page, with its text printed underneath so you can tell the pages apart.

## Things to Keep in Mind

* The text must **exactly** match what `test_QRCode.py` checks for. `Stop`, `stop `, and `stop` are three different texts to a computer.
* Short text makes a simpler QR code, which the drone can read from farther away.
* Print at 100% scale and keep the white margin (the "quiet zone") around the code.
* The codes use the highest error-correction level (`ERROR_CORRECT_H`), so they can still be read if a small part is covered or smudged.

## License

This project is open-source and available under the [MIT License](../LICENSE.md).
