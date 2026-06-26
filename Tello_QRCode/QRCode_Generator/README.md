# QR Code Generator

This README provides instructions for the `generate_single_qr_page.py` script, which generates and saves letter-sized QR codes, with one code per PDF file. This is ideal for printing large, highly visible codes to be used with your Tello drone.

### Table of Contents
1.  [Project Overview](#project-overview)
2.  [Features](#features)
3.  [Technologies Used](#technologies-used)
4.  [Installation](#installation)
5.  [Usage](#usage)
6.  [Output](#output)

## Project Overview

This is a utility script designed to generate high-resolution QR codes for use with the Tello drone control program. The script creates individual letter-sized PDF files, with each file containing a single, large QR code. This ensures maximum clarity for your drone's camera.

## Features

*   **Customizable QR Codes:** Easily change the QR code data to encode different commands.
*   **High-Resolution Output:** Generates large QR code images for optimal visibility during flight.
*   **Letter-Sized PDFs:** Creates print-ready PDF files formatted for standard letter paper.
*   **One Code Per Page:** Ensures each QR code is isolated and easy to cut out.

## Technologies Used

*   **Python 3.x:** The core programming language.
*   **qrcode:** The library used for generating the QR code images.
*   **Pillow (PIL):** Used for image manipulation to prepare the QR code for PDF output.
*   **ReportLab:** A library for creating PDF documents.

## Installation

### Prerequisites

*   Python 3.x installed on your computer.

### Setup Steps

1.  Navigate to the project directory:
    ```sh
    cd IDEALFall2025/Tello_QR_Code/QRCode_Generator
    ```

2.  Create a virtual environment (recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate      # On Windows
    ```

3.  Install dependencies:
    ```sh
    pip install qrcode[pil] reportlab
    ```

## Usage

1.  Open the `generate_single_qr_page.py` file in a text editor.
2.  Edit the `commands` dictionary in the `if __name__ == "__main__":` block to include the specific QR code data you want to encode.
    ```python
    commands = {
        "flip_forward": "qr_flip_forward.pdf",
        "flip_back": "qr_flip_back.pdf",
        "flip_left": "qr_flip_left.pdf",
        "flip_right": "qr_flip_right.pdf",
        "stop": "qr_stop.pdf",
    }
    ```
3.  Run the script from your terminal:
    ```sh
    python generate_single_qr_page.py
    ```

## Output

After running the script, a separate PDF file will be created for each item in the `commands` dictionary. The files will be saved in the same directory and named according to the dictionary values (e.g., `qr_stop.pdf`). You can then print these PDFs on letter-sized paper and use them with your Tello drone.
