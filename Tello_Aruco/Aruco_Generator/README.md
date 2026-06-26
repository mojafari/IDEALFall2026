# ArUco Marker Generator

This README provides instructions for the `generate_single_aruco_page.py` script, which generates and saves letter-sized ArUco markers, with one marker per PDF file. This is ideal for printing large, highly visible markers to be used with your Tello drone.

### Table of Contents
1.  [Project Overview](#project-overview)
2.  [Features](#features)
3.  [Technologies Used](#technologies-used)
4.  [Installation](#installation)
5.  [Usage](#usage)
6.  [Output](#output)

## Project Overview

This is a utility script designed to generate high-resolution ArUco markers for use with the Tello drone control program. The script creates individual letter-sized PDF files, with each file containing a single, large ArUco marker. This ensures maximum clarity for your drone's camera.

## Features

*   **Customizable Markers:** Easily change the ArUco dictionary and marker IDs.
*   **High-Resolution Output:** Generates large markers for optimal visibility during flight.
*   **Letter-Sized PDFs:** Creates print-ready PDF files formatted for standard letter paper.
*   **One Marker Per Page:** Ensures each marker is isolated and easy to cut out.

## Technologies Used

*   **Python 3.x:** The core programming language.
*   **OpenCV:** Used for generating the ArUco marker images.
*   **Pillow (PIL):** Used for image manipulation to prepare the marker for PDF output.
*   **ReportLab:** A library for creating PDF documents.

## Installation

### Prerequisites

*   Python 3.x installed on your computer.

### Setup Steps

1.  Navigate to the project directory:
    ```sh
    cd IDEALFall2025/Tello_Aruco/Aruco_Generator
    ```

2.  Create a virtual environment (recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate      # On Windows
    ```

3.  Install dependencies:
    ```sh
    pip install opencv-contrib-python reportlab
    ```

## Usage

1.  Open the `generate_single_aruco_page.py` file in a text editor.
2.  Edit the `ids` variable in the `if __name__ == "__main__":` block to include the specific ArUco IDs you want to generate.
    ```python
    ids = [0, 1, 2, 3, 4] # Example IDs for your Tello control
    ```
3.  Run the script from your terminal:
    ```sh
    python generate_single_aruco_page.py
    ```

## Output

After running the script, a separate PDF file will be created for each ID in the `ids` list. The files will be saved in the same directory and named `aruco_marker_#.pdf` (e.g., `aruco_marker_0.pdf`, `aruco_marker_1.pdf`). You can then print these PDFs on letter-sized paper and use them with your Tello drone.

