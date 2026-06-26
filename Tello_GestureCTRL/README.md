# Tello Drone Gesture Control

[![Python 3.x](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/downloads/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.12-brightgreen.svg)](https://google.github.io/mediapipe/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-blueviolet.svg)](https://opencv.org/)
[![DJITelloPy](https://img.shields.io/badge/DJITelloPy-library-informational.svg)](https://github.com/damiafuentes/DJITelloPy)

### Table of Contents
1.  [Project Overview](#project-overview)
2.  [Files](#files)
3.  [Features](#features)
4.  [Technologies Used](#technologies-used)
5.  [Installation](#installation)
6.  [Usage](#usage)
7.  [Gestures and Commands](#gestures-and-commands)
8.  [Learnings and Challenges](#learnings-and-challenges)
9.  [License](#license)

## Project Overview

This project provides a system for controlling a DJI Tello mini-drone using hand gestures. It uses the `gesture_controller.py` module, which leverages the MediaPipe library to detect hand landmarks and recognize specific gestures. The main script, `tello_gesture_control.py`, integrates this gesture detection with the drone's control interface via `djitellopy`, allowing for intuitive, real-time command execution.

## Files

*   `gesture_controller.py`: A modular script containing the `GestureController` class. This class is responsible for all hand detection and gesture interpretation logic. It processes video frames to identify gestures like "TAKE_OFF", "LAND", and directional movements.
*   `tello_gesture_control.py`: The main program that orchestrates the entire process. It connects to the Tello drone, starts a video stream, and uses multithreading to handle video processing and gesture-based command sending without blocking the main loop.

## Features

*   **Hand Gesture Recognition:** Uses MediaPipe to accurately and efficiently detect and track hands, translating specific hand shapes into drone commands.
*   **Real-time Video Streaming and Processing:** Displays the Tello's live camera feed, with hand landmarks and the recognized gesture overlaid for visual feedback.
*   **Multithreaded Architecture:** Uses separate threads for video capture and command execution to ensure smooth, non-blocking operation.
*   **Safe Execution:** Includes a cooldown period between commands to prevent rapid, erratic movements and a `try...finally` block to ensure the drone lands and resources are released upon program termination.
*   **Specific Drone Commands:** Recognizes gestures for takeoff, landing, hovering, moving forward, and rotating left.

## Technologies Used

*   **Python 3.x:** The core programming language.
*   **MediaPipe:** A powerful library for computer vision, used for real-time hand landmark detection and tracking.
*   **OpenCV:** Used for video stream processing and displaying the annotated output.
*   **djitellopy:** The library for sending commands and receiving video data from the DJI Tello drone.
*   **Threading:** The standard Python library for concurrent task management.

## Installation

### Prerequisites

*   A DJI Tello mini-drone with a charged battery.
*   Python 3.x installed on your computer.

### Setup Steps

1.  **Navigate to the project directory:**
    ```sh
    cd IDEALFall2025/tello_gesture_control
    ```

2.  **Create a virtual environment (recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate      # On Windows
    ```

3.  **Install dependencies:**
    ```sh
    pip install mediapipe opencv-python djitellopy
    ```

## Usage

1.  **Power on the Tello drone.** Wait for the lights to blink green, indicating it's ready.
2.  **Connect your computer to the Tello's Wi-Fi network.** The network name will be something like `TELLO-XXXXXX`.
3.  **Run the script from your terminal:**
    ```sh
    python tello_gesture_control.py
    ```

The program will:
*   Connect to the Tello and report its battery life.
*   Display a video window showing the live feed with gesture information.
*   Wait for the "TAKE_OFF" gesture to begin.
*   Follow subsequent gesture commands for flight.
*   End the program safely by landing the drone and closing the video window when the "LAND" gesture is made or you press `q`.

## Gestures and Commands

| Gesture | Command | Description |
| :------ | :---------- | :----- |
| All fingers up | TAKE_OFF | Lifts the drone off the ground. |
| All fingers down | LAND | Lands the drone safely. |
| Index finger up | FORWARD | Moves the drone forward. |
| Index and Middle fingers up | ROTATE_LEFT | Rotates the drone counter-clockwise. |
| Other gestures | HOVER | Keeps the drone stationary. |


## Learnings and Challenges

*   **Robust State Management:** Implemented shared variables (`is_running`, `in_flight`, `latest_gesture`) and threading locks to manage the drone's state and inter-thread communication reliably.
*   **Command Rate Limiting:** Added a cooldown mechanism (`command_cooldown`) to prevent the drone from receiving too many commands in quick succession, improving flight stability.
*   **Integration of External Libraries:** Successfully combined MediaPipe's computer vision capabilities with `djitellopy`'s drone control functionality within a multithreaded Python application.


## License

This project is open-source and available under the [MIT License](LICENSE.md).
		
		
		
		
		
