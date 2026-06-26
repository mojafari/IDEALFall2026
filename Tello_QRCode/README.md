# Tello Drone QR Code Control

### Table of Contents
1.  [Project Overview](#project-overview)
2.  [Features](#features)
3.  [Technologies Used](#technologies-used)
4.  [Installation](#installation)
5.  [Usage](#usage)
6.  [QR Codes](#qr-codes)
7.  [Learnings and Challenges](#learnings-and-challenges)
8.  [License](#license)

## Project Overview

This project demonstrates how to control a DJI Tello mini-drone using QR codes. The Python script connects to the Tello, streams its video feed, and uses OpenCV to detect specific QR codes. Depending on the data encoded in the detected QR code, the drone will execute a different pre-programmed maneuver. This is an example of a simple vision-based control system for a robotic platform.

## Features

*   **Real-time video streaming:** Displays the Tello's live camera feed using OpenCV.
*   **QR code detection:** Uses the `cv2.QRCodeDetector` to detect and decode QR codes from the live video.
*   **QR code-based control:** Triggers a specific drone command based on the data encoded in the detected QR code.
*   **Safe landing:** The drone lands when a QR code containing the text `stop` is detected or when the user presses `q`.

## Technologies Used

*   **Python 3.x:** The core programming language.
*   **djitellopy:** A library for controlling the DJI Tello drone.
*   **OpenCV:** The powerful computer vision library used for image processing and QR code detection.
*   **NumPy:** Used by OpenCV for handling image data.

## Installation

### Prerequisites

*   A DJI Tello mini-drone with a charged battery.
*   Python 3.x installed on your computer.

### Setup Steps

1.  **Navigate to the project directory:**
    ```sh
    cd IDEALFall2025/Tello_QRCode
    ```

2.  **Create a virtual environment (recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate      # On Windows
    ```

3.  **Install dependencies:**
    ```sh
    pip install opencv-contrib-python djitellopy
    ```

## Usage

1.  **Print and display the required QR codes:**
    *   `stop` for landing.
    *   `flip_forward` for a forward flip.
    *   `flip_back` for a backward flip.
    *   `flip_left` for a left flip.
    *   `flip_right` for a right flip.
    
    You will need to generate and print these markers, ensuring the encoded data exactly matches the commands used in the `test_QRCode.py` script.

2.  **Power on the Tello drone.** Wait for the lights to blink yellow, indicating it's ready.
3.  **Connect your computer to the Tello's Wi-Fi network.** The network name will be something like `TELLO-XXXXXX`.
4.  **Run the script from your terminal:**
    ```sh
    python test_QRCode.py
    ```

The program will:
*   Connect to the Tello and print its battery life.
*   Take off automatically.
*   Open a window showing the live video feed.
*   Perform the corresponding maneuver when a QR code with the specific command is detected.
*   Land when a QR code with the data `stop` is detected or you press `q`.

## QR Codes

This project uses QR codes with specific text data. To use the drone's features, you must generate and use physical QR codes with the following data:


| QR Code Data | Command |
|:---:|:---|
| `stop` | Land |
| `flip_forward` | Flip Forward |
| `flip_back` | Flip Backward |
| `flip_left` | Flip Left |
| `flip_right` | Flip Right |


## Learnings and Challenges

*   **Real-time video processing:** Successfully processing a live video stream from the drone's camera with minimal latency.
*   **Computer vision integration:** Using the `cv2.QRCodeDetector` to accurately detect and decode QR codes.
*   **Robotics control:** Implementing simple autonomous control based on visual input. A key learning is the importance of robust code to handle cases where markers are not visible.

## License

This project is open-source and available under the [MIT License](LICENSE.md).

