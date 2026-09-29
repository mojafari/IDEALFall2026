# Taking the Plunge: Intro to Drones & AI

Welcome to the official course repository for **IDEAL Fall 2026 – Taking the Plunge: Intro to Drones & AI**.

This course provides an engaging introduction to drone technology, foundational programming, and how artificial intelligence enables drones to interact intelligently with their environment. Through hands-on projects and guided modules, students will explore how drones can be programmed to navigate, recognize objects, and perform simple autonomous tasks using AI techniques.

## Course Goals

- Understand the basic principles of drone flight and operation.
- Learn fundamental programming concepts using Python.
- Explore how AI enables drones to detect and respond to their surroundings.
- Apply computer vision techniques for gesture control, object detection, marker tracking, and other applications.

## Repository Structure

The folders are numbered and listed in the order we will use them in class.

### Foundations

| Folder | What you will do |
| :--- | :--- |
| [`00_Getting_Started`](./00_Getting_Started) | Learn how to write Python programs and use Python to communicate with a DJI Tello drone. |
| [`01_Getting_Started_AI`](./01_Getting_Started_AI) | Learn to use an AI assistant to explain, modify, debug, and review your drone programs. |

### Computer Vision Projects

Every project follows the same idea: **the drone's camera sees something → the program recognizes it → the drone reacts.** Each one uses a smarter way of recognizing.

| Folder | What the drone recognizes | How it recognizes it |
| :--- | :--- | :--- |
| [`Tello_Aruco`](./Tello_Aruco) | Printed ArUco markers (flip or land) | Pattern matching with OpenCV |
| [`Tello_QRCode`](./Tello_QRCode) | Printed QR codes with text commands | QR decoding with OpenCV |
| [`Tello_YOLO`](./Tello_YOLO) | Everyday objects (people, chairs, bottles...) while flying a square | YOLO neural network (AI) |
| [`Tello_GestureCTRL`](./Tello_GestureCTRL) | Your hand gestures, to fly the drone | MediaPipe hand tracking (AI) |
| [`Tello_PoseCTRL`](./Tello_PoseCTRL) | Your arm poses, to fly the drone | MediaPipe body tracking (AI) |

Each folder has its own README with setup steps, the commands it understands, an explanation of the code, "Try This" exercises, and troubleshooting tips.

Every project also has a **no-fly test** (`test_..._no_fly.py`). It checks the packages, the AI model or detector, the drone connection, the battery, and the video, then runs a live rehearsal with the same threads as the flying program while printing the commands it *would* send. The drone never takes off. Run it before every flight; it ends with **READY TO FLY** or tells you exactly what to fix.

| Project | No-fly test | Flying program |
| :--- | :--- | :--- |
| `Tello_Aruco` | `test_Aruco_no_fly.py` | `test_Aruco.py` |
| `Tello_QRCode` | `test_QRCode_no_fly.py` | `test_QRCode.py` |
| `Tello_YOLO` | `test_YOLO_no_fly.py` | `test_sim_cam_sqv1_YOLO.py` |
| `Tello_GestureCTRL` | `test_gesture_no_fly.py` | `tello_gesture_control.py` |
| `Tello_PoseCTRL` | `test_pose_no_fly.py` | `tello_pose_control.py` |

All flying programs use the same structure: one **thread** reads the camera, one **thread** sends drone commands, and the main program runs the detector and shows the video. Drone commands such as `flip_forward()` or `move_forward(100)` take a few seconds to finish, so keeping them in their own thread means the video never freezes while the drone moves.

The file [`test_camera.py`](./test_camera.py) is a quick check that your computer can connect to the Tello and show its video. Run it whenever you are not sure the connection works.

## Development Environment (Recommended Setup)

- **Python 3.12** (Python 3.10 and 3.11 also work). Very new Python versions may not be supported yet by MediaPipe, which the gesture and pose projects need.
- **One virtual environment (`.venv`) for the whole course**, created in the repository folder. [`00_Getting_Started`](./00_Getting_Started) walks you through creating it in PyCharm.
- **PyCharm Community Edition** (optional but recommended for easier debugging and project management).

> 💡 Students can use any code editor, but PyCharm Community Edition provides built-in support for virtual environments and is recommended for this course.
> Download here: [https://www.jetbrains.com/pycharm/download](https://www.jetbrains.com/pycharm/download)

## Hardware Requirements

- **DJI Tello (Combo)** – This is the primary drone platform used throughout the course.
- **Optional:** Webcam – The gesture and pose projects can use your laptop webcam for practice without flying. Other modules do not need it.

## Getting Started

To participate in the projects, you will need:

- A laptop with **Python 3.12** installed
- **PyCharm Community Edition** IDE
- A DJI **Tello** drone
- **Optional:** Webcam (for practicing gestures and poses)

Each project folder has a `requirements.txt` listing the packages it needs. With your course `.venv` active, you can install the packages for **all** projects at once from the repository root:

```sh
pip install -r 00_Getting_Started/requirements.txt -r Tello_Aruco/requirements.txt -r Tello_QRCode/requirements.txt -r Tello_YOLO/requirements.txt -r Tello_GestureCTRL/requirements.txt -r Tello_PoseCTRL/requirements.txt
```

This is a large download (mostly PyTorch, which YOLO uses), so do it at home or on a fast connection, before class.

### Important: The Tello Wi‑Fi Has No Internet

When your laptop is connected to the drone's Wi‑Fi (`TELLO-XXXXXX`), it cannot reach the internet. Anything that needs to be downloaded must be downloaded **before** you connect to the drone:

| Project | Download before class | How |
| :--- | :--- | :--- |
| All | Python packages | The `pip install` command above |
| `Tello_YOLO` | `yolov8n.pt` model | See [Tello_YOLO → Setup](./Tello_YOLO/README.md#download-the-model-before-class) |
| `Tello_GestureCTRL` | `hand_landmarker.task` model | Run `python gesture_controller.py` once in that folder |
| `Tello_PoseCTRL` | `pose_landmarker_lite.task` model | Run `python pose_controller.py` once in that folder |

## Flight Safety Rules

1. Run the project's **no-fly test** first, and fly only after it says **READY TO FLY**.
2. Fly only in the area your instructor has cleared. Keep at least 2 m of empty space around the drone.
3. Many programs **take off automatically** when they start. Look at the drone, not the screen, when you press Run.
4. Keep one hand near the **Q** key. In every project, **Q** lands the drone.
5. Never try to catch a flying drone.
6. Check the battery before flying. Flips need more than 50%.
7. If something goes wrong and **Q** does not work, press the power button on the drone.

## Troubleshooting (All Projects)

| Problem | Likely cause and fix |
| :--- | :--- |
| `ModuleNotFoundError: No module named ...` | The package is not installed in the environment PyCharm is using. Check that the interpreter is your `.venv` (see `00_Getting_Started`), then `pip install -r <project>/requirements.txt`. |
| Program cannot connect to the Tello | Make sure your laptop is on the `TELLO-XXXXXX` Wi‑Fi, the drone is on, and no other program (or the Tello phone app) is connected to it. |
| Video colors look wrong (blue and red swapped) | The Tello library delivers frames in RGB order, while OpenCV expects BGR. The project code converts each frame with `cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)`. |
| `import cv2` fails after installing MediaPipe or YOLO | Two OpenCV packages are fighting. Run `pip uninstall -y opencv-python opencv-contrib-python`, then `pip install opencv-contrib-python`. |
| The drone lands by itself | The battery is low, or the drone received no command for 15 seconds (a built-in Tello safety feature). |

## License

This project is intended for educational use and classroom exploration.
Feel free to fork and adapt under the terms of the [MIT License](LICENSE.md).

---

Stay tuned for updates and new modules throughout the semester!
