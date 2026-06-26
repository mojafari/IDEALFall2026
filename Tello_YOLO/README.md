# Tello Drone with YOLO Object Tracking

[![Python 3.x](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-blueviolet.svg)](https://opencv.org/)
[![Ultralytics YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-brightgreen.svg)](https://docs.ultralytics.com/)
[![DJITelloPy](https://img.shields.io/badge/DJITelloPy-library-informational.svg)](https://github.com/damiafuentes/DJITelloPy)

### Table of Contents
1.  [Project Overview](#project-overview)
2.  [Features](#features)
3.  [Technologies Used](#technologies-used)
4.  [Installation](#installation)
5.  [Usage](#usage)
6.  [Program Logic](#program-logic)
7.  [Learnings and Challenges](#learnings-and-challenges)
8.  [License](#license)

## Project Overview

This project demonstrates the integration of a DJI Tello mini-drone with real-time object detection and tracking using the Ultralytics YOLOv8 model. The Python script controls the Tello, streams its video feed, and simultaneously performs object detection on the live video. A simple flight pattern is executed to show the drone's maneuverability while the object detection is active.

The project is an ideal showcase for applied computer vision and robotics, highlighting how real-time video feeds can be processed on the fly to inform a drone's actions or simply to provide annotated video.

## Features

*   **Real-time video streaming:** Connects to the Tello drone and displays its live video feed.
*   **YOLOv8 object detection and tracking:** Utilizes the pre-trained `yolov8n.pt` model to detect and track objects in real-time.
*   **Annotated video output:** Overlays bounding boxes and labels for detected objects onto the video stream.
*   **Multithreaded architecture:** Separates the video fetching and drone command processes into different threads to ensure smooth, non-blocking operation.
*   **Basic flight demonstration:** Executes a pre-defined square flight pattern to illustrate automated drone control.
*   **Safe program shutdown:** Ensures the drone lands and all resources are properly released upon program completion or user exit (`q` key press).

## Technologies Used

*   **Python 3.x:** The core programming language.
*   **djitellopy:** A powerful and user-friendly Python library for controlling the DJI Tello drone.
*   **Ultralytics YOLOv8:** The state-of-the-art model used for real-time object detection and tracking.
*   **OpenCV:** Used for video stream processing and displaying the annotated output.
*   **Threading:** Standard Python library for managing concurrent tasks, ensuring smooth video capture and command execution.

## Installation

### Prerequisites

*   A DJI Tello mini-drone with a charged battery.
*   Python 3.x installed on your computer.

### Setup Steps

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/mojafari/IDEALFall2025.git
    cd IDEALFall2025
    ```

2.  **Create a virtual environment (recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate      # On Windows
    ```

3.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
    (Note: You will need to create a `requirements.txt` file containing `opencv-python`, `djitellopy`, and `ultralytics` to make this step work.)

## Usage

1.  **Power on the Tello drone.** Wait for the lights to blink yellow, indicating it's ready.
2.  **Connect your computer to the Tello's Wi-Fi network.** The network name will be something like `TELLO-XXXXXX`.
3.  **Run the script from your terminal:**
    ```sh
    python test_sim_cam_sqv1_YOLO.py
    ```

The program will:
*   Connect to the Tello drone.
*   Display a video window showing the live feed with YOLO detections overlaid.
*   Automatically initiate a takeoff and perform a square flight path.
*   End the program safely by landing the drone and closing the video window when the flight is complete or you press `q` on the keyboard.

## Program Logic

The script uses two separate threads to handle the concurrent tasks of video streaming and drone control.

*   `video_read_thread`: This daemon thread continuously fetches frames from the Tello and stores the latest one in a shared variable (`latest_frame`) for the main thread to process.
*   `command_thread_function`: This thread handles the drone's flight logic. It initiates the takeoff, executes the predefined square pattern, and then lands the drone.

The main thread is responsible for:
*   Initializing the Tello object and establishing a connection.
*   Starting the video and command threads.
*   Displaying the video feed with YOLO object detection.
*   Handling user input to quit the program.

## Learnings and Challenges

*   **Concurrency management:** Successfully separating video capture and command execution into different threads was crucial for a non-blocking user experience. Using a `threading.Lock` was necessary to prevent race conditions when accessing the shared video frame variable.
*   **Hardware and software integration:** Integrating the `djitellopy` library with the video processing capabilities of `OpenCV` and the computer vision model `YOLO` required careful setup and synchronization.
*   **Real-time performance:** Running object detection on a live video stream is computationally intensive. Choosing a lightweight model like `yolov8n.pt` was key to achieving decent real-time performance on a typical laptop. Resizing the frame was also a necessary optimization.

## License

This project is open-source and available under the [MIT License](LICENSE.md).
