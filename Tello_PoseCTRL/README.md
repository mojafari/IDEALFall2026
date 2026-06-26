# Tello Drone Pose Control

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
7.  [Poses and Commands](#poses-and-commands)
8.  [Learnings and Challenges](#learnings-and-challenges)
9.  [License](#license)

## Project Overview

This project extends the control capabilities of a DJI Tello mini-drone by using full-body pose estimation. It replaces hand gesture recognition with a system that leverages the MediaPipe Pose solution to detect and interpret full-body poses. The `pose_controller.py` module handles the computer vision, while the `tello_pose_control.py` script manages real-time video streaming, pose-based command sending via `djitellopy`, and ensures safe, non-blocking operation using multithreading.

## Files

*   `pose_controller.py`: A modular script containing the `PoseController` class. This class uses MediaPipe Pose to detect body landmarks and interprets arm positions and movements to generate drone commands.
*   `tello_pose_control.py`: The main program that orchestrates the entire process. It connects to the Tello drone, starts a video stream, and uses multithreading to handle video processing and pose-based command sending.

## Features

*   **Full-Body Pose Recognition:** Uses MediaPipe Pose to accurately and efficiently detect body landmarks, translating specific arm positions into drone commands.
*   **Real-time Video Streaming and Processing:** Displays the Tello's live camera feed, with detected pose landmarks and the recognized command overlaid for visual feedback.
*   **Multithreaded Architecture:** Employs separate threads for video capture and command execution to ensure smooth, non-blocking operation, which is crucial for responsive control.
*   **Safe Execution:** Implements a command cooldown period to prevent erratic movements and includes a `try...finally` block to ensure the drone lands and resources are released upon program termination.
*   **Specific Drone Commands:** Recognizes poses for takeoff, landing, hovering, moving forward, turning left, and turning right.

## Technologies Used

*   **Python 3.x:** The core programming language.
*   **MediaPipe:** A powerful library for computer vision, used here for real-time full-body pose landmark detection and tracking.
*   **OpenCV:** Used for video stream processing, including frame capture, annotation, and display.
*   **djitellopy:** The library for sending commands and receiving video data from the DJI Tello drone.
*   **Threading:** The standard Python library for concurrent task management.

## Installation

### Prerequisites

*   A DJI Tello mini-drone with a charged battery.
*   Python 3.x installed on your computer.

### Setup Steps

1.  **Clone the repository (or navigate to the project directory):**
    ```sh
    # Assuming the code is part of a larger project, navigate to the specific folder
    cd IDEALFall2025/Tello_PoseCTRL
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
    python tello_pose_control.py
    ```

The program will:
*   Connect to the Tello and report its battery life.
*   Display a video window showing the live feed with pose information.
*   Wait for the "TAKE_OFF" pose to begin.
*   Follow subsequent pose commands for flight.
*   End the program safely by landing the drone and closing the video window when the "LAND" pose is made or you press `q`.

## Poses and Commands

| Pose | Command | Description |
| :------ | :---------- | :----- |
| Both arms up | TAKE_OFF | Lifts the drone off the ground. |
| Both arms down | LAND | Lands the drone safely. |
| Both arms forward | FORWARD | Moves the drone forward. |
| Left arm up | ROTATE_LEFT | Rotates the drone counter-clockwise. |
| Right arm up | ROTATE_RIGHT | Rotates the drone clockwise. |
| Other gestures | HOVER | Keeps the drone stationary. |


## Learnings and Challenges

*   **Pose-based Command Interpretation:** Interpreting complex body poses robustly from a single camera angle can be challenging. The logic must be simple yet effective to avoid misinterpreting minor body movements.
*   **Response Latency:** Full-body pose detection can be more computationally intensive than hand detection. Fine-tuning the command cooldown (`command_cooldown`) is critical to ensure a balance between responsiveness and stability.
*   **Thread Synchronization:** Managing shared state and ensuring threads communicate without data corruption is a key learning point from implementing this project.


## License

This project is open-source and available under the [MIT License](LICENSE.md).
