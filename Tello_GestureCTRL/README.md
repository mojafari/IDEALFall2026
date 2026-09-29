# Tello Gesture Control

[![Python 3.10–3.12](https://img.shields.io/badge/Python-3.10–3.12-blue.svg)](https://www.python.org/downloads/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Tasks%20API-brightgreen.svg)](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-blueviolet.svg)](https://opencv.org/)
[![DJITelloPy](https://img.shields.io/badge/DJITelloPy-library-informational.svg)](https://github.com/damiafuentes/DJITelloPy)

Fly the Tello with your hand. Open your hand and the drone takes off; make a fist and it lands. The drone's own camera watches your hand, and Google's **MediaPipe** AI finds the 21 joints of your fingers in every frame.

### Table of Contents
1. [What You Will Learn](#what-you-will-learn)
2. [How Hand Tracking Works](#how-hand-tracking-works)
3. [Files](#files)
4. [Setup](#setup)
5. [Practice With Your Webcam First](#practice-with-your-webcam-first)
6. [Run the No-Fly Test](#run-the-no-fly-test)
7. [Before You Fly](#before-you-fly)
8. [Run the Program](#run-the-program)
9. [Gestures and Commands](#gestures-and-commands)
10. [How the Code Works](#how-the-code-works)
11. [Try This](#try-this)
12. [Troubleshooting](#troubleshooting)
13. [License](#license)

## What You Will Learn

* How an AI model finds **landmarks** (key points) on a hand.
* How simple rules on those points ("is the fingertip above the knuckle?") turn into gestures.
* How to make a controller safer: hold-time filtering, one command per gesture, and automatic landing.
* How **threads** let the drone move while the video keeps updating.

## How Hand Tracking Works

MediaPipe's **Hand Landmarker** model looks at an image and returns 21 points on the hand. Each point has an `x` and `y` position between 0 and 1 (0 = left/top edge of the image, 1 = right/bottom edge).

| Points | Part of the hand |
| :--- | :--- |
| 0 | Wrist |
| 1, 2, 3, 4 | Thumb (4 is the tip) |
| 5, 6, 7, 8 | Index finger (5 knuckle, 6 middle joint, 8 tip) |
| 9, 10, 11, 12 | Middle finger (12 is the tip) |
| 13, 14, 15, 16 | Ring finger (16 is the tip) |
| 17, 18, 19, 20 | Pinky (20 is the tip) |

Our code does not use AI to decide the gesture. It uses simple rules on the points:

* A finger is **up** if its tip is higher in the image than its middle joint (for the index finger: point 8 above point 6). Remember that in images, `y` grows **downward**, so "higher" means a **smaller** `y`.
* The thumb sticks out sideways, so it is **up** if its tip (4) is farther out to the side than its base (2).

## Files

| File | Purpose |
| :--- | :--- |
| `gesture_controller.py` | Finds the hand and decides the gesture. Run it by itself to practice with your webcam. |
| `test_gesture_no_fly.py` | **Run this before flying.** Checks packages, the hand model, drone connection, battery, and video, then rehearses every gesture on the drone's camera. The drone does not take off. |
| `tello_gesture_control.py` | Main program. Connects to the Tello and turns gestures into flight commands. |
| `requirements.txt` | Python packages needed by this project. |
| `hand_landmarker.task` | The MediaPipe hand model (about 8 MB). Downloaded automatically on the first run. |

## Setup

Use the same course virtual environment (`.venv`) you created in [`00_Getting_Started`](../00_Getting_Started). From the repository root (or the PyCharm terminal):

```sh
pip install -r Tello_GestureCTRL/requirements.txt
```

> **Python version:** MediaPipe does not support every new Python release right away. If `pip` says it cannot find a version of `mediapipe`, your Python is probably too new. Python 3.12 works well for this course.

## Practice With Your Webcam First

While you are still on **normal internet** (not the Tello Wi‑Fi), run the controller by itself:

```sh
python gesture_controller.py
```

The first time, this downloads the hand model into this folder. Then it opens your laptop webcam and shows the gesture it sees. Practice each gesture until the label is steady. No drone is involved, so this is a safe place to experiment.

## Run the No-Fly Test

`test_gesture_no_fly.py` checks everything the flying program needs **without taking off**. The webcam practice above tests your gestures; this test also checks the drone, its video, and the same threads the flying program uses. Run it every time before you fly.

```sh
python test_gesture_no_fly.py
```

It works through five steps and stops at the first problem it cannot get past:

| Step | What it checks |
| :---: | :--- |
| 1 | The Python packages are installed. |
| 2 | The hand model file is present and MediaPipe can run it. |
| 3 | The computer can talk to the Tello, and the battery is charged enough. |
| 4 | The Tello video stream works. |
| 5 | **Live rehearsal.** The same threads and rules as `tello_gesture_control.py` run on the live video. Show every gesture; the rehearsal pretends to take off and land, so you can try the full sequence. The summary lists which gestures were recognized. The command the drone *would* receive is shown on screen and in the terminal, but nothing is sent. Press **Q** to finish. |

At the end, a summary marks every check `PASS`, `WARN`, or `FAIL`:

* **READY TO FLY** – everything passed.
* **READY WITH WARNINGS** – you can fly, but read the warnings (for example, a command you did not test in Step 5).
* **NOT READY** – fix each `FAIL` (the message says how), then run the test again.

> 💡 No drone nearby? Set `USE_WEBCAM = True` at the top of `test_gesture_no_fly.py` to skip the drone connection and run the test with your laptop webcam instead.

## Before You Fly

* The no-fly test above ended with **READY TO FLY** (or you have read its warnings).
* Clear at least 2 m of space around and in front of the drone.
* **FORWARD moves the drone toward you**, because its camera is looking at you. Stand at least 1.5–2 m away, and step back if it gets close.
* Keep your hand near the **Q** key. Pressing **Q** lands the drone.
* Good lighting on your hand makes detection much more reliable.

## Run the Program

1. Power on the Tello and wait for the status light to blink.
2. Connect your computer to the Tello's Wi‑Fi network (`TELLO-XXXXXX`).
3. In PyCharm, right-click `tello_gesture_control.py` → **Run**. Or, from this folder in a terminal:

   ```sh
   python tello_gesture_control.py
   ```

4. Crouch down so your hand is in front of the drone's camera, and show an **open hand** to take off.

The video window shows two lines:

* **Seen:** what the camera sees right now.
* **Active:** the gesture the drone is obeying. A gesture becomes active only after you hold it steady for 0.3 s.

## Gestures and Commands

| Gesture | Command | What the drone does |
| :--- | :--- | :--- |
| Open hand (all five fingers up) | `TAKE_OFF` | Takes off (only when on the ground). |
| Fist (all fingers down) | `LAND` | Lands and ends the program. |
| Only the index finger up | `FORWARD` | Moves 30 cm forward, **toward you**. |
| Index and middle fingers up ("peace sign") | `ROTATE_LEFT` | Rotates 45° counter-clockwise. |
| Any other hand shape | `HOVER` | Stays in place. |
| No hand visible | `NO_HAND` | Stays in place. |

**One move per gesture.** Holding up your index finger moves the drone forward **once**. To move again, relax your hand (or take it out of view) for a moment, then show the gesture again. This stops the drone from flying into you if you forget to lower your hand.

## How the Code Works

```text
video_read_thread          main program                         gesture_command_thread
─────────────────          ────────────                         ──────────────────────
newest Tello frame   ──>   MediaPipe finds 21 hand points
convert RGB → BGR          rules decide the gesture ("Seen")
                           held for 0.3 s? → "Active"   ──>     TAKE_OFF / LAND / move
                           draw skeleton and labels             or keep the drone hovering
                           check for Q key
```

Safety features built into `tello_gesture_control.py`:

| Feature | Setting | Why |
| :--- | :--- | :--- |
| Hold time | `HOLD_TIME = 0.3` | While your hand changes shape, it briefly passes through other gestures. Waiting for a steady gesture ignores those. |
| One move per gesture | `ready_for_move` | A held gesture does not repeat the move over and over. |
| Cooldown | `COMMAND_COOLDOWN = 0.5` | A short pause after each command. |
| Keep-alive | `KEEPALIVE_INTERVAL = 5.0` | The Tello lands by itself if it hears nothing for 15 seconds. While you hover, the program sends a "stay still" message every 5 seconds. |
| Safe exit | `try` / `finally` | Pressing **Q**, closing the program, or an error always lands the drone. |

## Try This

1. In `gesture_controller.py`, add a new gesture: pinky only up → `"UP"`. Then, in `tello_gesture_control.py`, make `"UP"` call `tello.move_up(30)`.
2. Change `ROTATE_DEGREES` to `20`. After turning 45°, your hand is often out of the camera's view. Does a smaller angle help?
3. Change `HOLD_TIME` to `0.0` and practice with the webcam. Watch the **Seen** label while you switch gestures. What problem does the hold time solve?
4. In `gesture_controller.py`, lower the three confidence values from `0.75` to `0.5` and test with the webcam. Does the hand get detected more often? Do you see more mistakes?
5. **Challenge:** Make the drone follow your hand. Landmark 9 (middle of the palm) has an `x` value; if `x < 0.4` rotate left a little, if `x > 0.6` rotate right a little.

## Troubleshooting

| Problem | Likely cause and fix |
| :--- | :--- |
| `AttributeError: module 'mediapipe' has no attribute 'solutions'` | You are running last year's code. This year's code uses the newer MediaPipe **Tasks** API; pull the latest version of this repository. |
| `Could not download the hand model` | You are on the Tello Wi‑Fi, or offline. Connect to normal internet and run `python gesture_controller.py` once. |
| `CERTIFICATE_VERIFY_FAILED` while downloading (macOS) | Your Python install needs its security certificates. Run **Install Certificates.command** in your `Applications/Python 3.x` folder, then try again. |
| `pip` cannot find `mediapipe` | Your Python version is too new for MediaPipe. Use Python 3.12. |
| Gesture flickers between two labels | Improve the lighting, hold your hand 0.5–1 m from the camera, and face your palm toward it. |
| Drone lands by itself after a while | The battery may be low. Check the battery printed at the start. |
| Colors look wrong in the video | The RGB → BGR conversion line in `video_read_thread` was removed. |

## License

This project is open-source and available under the [MIT License](LICENSE.md).
