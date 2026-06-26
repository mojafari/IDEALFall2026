# Tello Drone ArUco Marker Control

[![Python 3.x](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-blueviolet.svg)](https://opencv.org/)
[![DJITelloPy](https://img.shields.io/badge/DJITelloPy-library-informational.svg)](https://github.com/damiafuentes/DJITelloPy)

### Table of Contents
1.  [Project Overview](#project-overview)
2.  [Features](#features)
3.  [Technologies Used](#technologies-used)
4.  [Installation](#installation)
5.  [Usage](#usage)
6.  [ArUco Markers](#aruco-markers)
7.  [Learnings and Challenges](#learnings-and-challenges)
8.  [License](#license)

## Project Overview

This project demonstrates how to control a DJI Tello mini-drone using ArUco markers. The Python script connects to the Tello, streams its video feed, and uses OpenCV to detect specific ArUco markers. Depending on the ID of the detected marker, the drone will execute a different pre-programmed flip maneuver. This is an example of a simple vision-based control system for a robotic platform.

## Features

*   **Real-time video streaming:** Displays the Tello's live camera feed using OpenCV.
*   **ArUco marker detection:** Uses the `cv2.aruco` library to detect markers from the live video.
*   **Marker-based control:** Triggers a specific drone flip command based on the ID of the detected marker.
*   **Safe landing:** The drone lands when a marker with ID `0` is detected or when the user presses `q`.

## Technologies Used

*   **Python 3.x:** The core programming language.
*   **djitellopy:** A library for controlling the DJI Tello drone.
*   **OpenCV:** The powerful computer vision library used for image processing and ArUco marker detection.
*   **NumPy:** Used by OpenCV for handling image data.

## Installation

### Prerequisites

*   A DJI Tello mini-drone with a charged battery.
*   Python 3.x installed on your computer.

### Setup Steps

1.  **Navigate to the project directory:**
    ```sh
    cd IDEALFall2025/test_Aruco
    ```

2.  **Create a virtual environment (recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate      # On Windows
    ```

3.  **Install dependencies:**
    ```sh
    pip install opencv-python djitellopy
    ```

## Usage

1.  **Print and display the required ArUco markers:**
    *   ID `0` for landing.
    *   ID `1` for a forward flip.
    *   ID `2` for a backward flip.
    *   ID `3` for a left flip.
    *   ID `4` for a right flip.
    
    The script is configured to use the `DICT_4X4_50` dictionary. You will need to generate and print these markers.

2.  **Power on the Tello drone.** Wait for the lights to blink yellow, indicating it's ready.
3.  **Connect your computer to the Tello's Wi-Fi network.** The network name will be something like `TELLO-XXXXXX`.
4.  **Run the script from your terminal:**
    ```sh
    python test_Aruco.py
    ```

The program will:
*   Connect to the Tello and print its battery life.
*   Take off automatically.
*   Open a window showing the live video feed.
*   Perform the corresponding flip maneuver when a marker with ID 1, 2, 3, or 4 is detected.
*   Land when a marker with ID 0 is detected or you press `q`.

## ArUco Markers

This project uses the `DICT_4X4_50` dictionary. To use the drone's features, you must generate and use physical markers with the following IDs:

| Marker ID | Command |
|:---:|:---|
| 0 | Land |
| 1 | Flip Forward |
| 2 | Flip Backward |
| 3 | Flip Left |
| 4 | Flip Right |


## Learnings and Challenges

*   **Real-time video processing:** Successfully processing a live video stream from the drone's camera with minimal latency.
*   **Computer vision integration:** Using the `cv2.aruco` library to accurately detect markers and their IDs.
*   **Robotics control:** Implementing simple autonomous control based on visual input. A key learning is the importance of robust code to handle cases where markers are not visible.

## License

This project is open-source and available under the [MIT License](LICENSE.md).
