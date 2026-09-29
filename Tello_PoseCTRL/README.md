# Tello Pose Control

[![Python 3.10–3.12](https://img.shields.io/badge/Python-3.10–3.12-blue.svg)](https://www.python.org/downloads/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Tasks%20API-brightgreen.svg)](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-blueviolet.svg)](https://opencv.org/)
[![DJITelloPy](https://img.shields.io/badge/DJITelloPy-library-informational.svg)](https://github.com/damiafuentes/DJITelloPy)

Fly the Tello with your whole body. Raise both arms and the drone takes off; raise one arm and it turns; cross your arms in an "X" and it lands. Google's **MediaPipe** AI finds 33 points on your body in every frame of the drone's video.

This project follows the same design as [`Tello_GestureCTRL`](../Tello_GestureCTRL). The difference is the model: instead of finger joints up close, it tracks your shoulders, elbows, and wrists from a few meters away.

### Table of Contents
1. [What You Will Learn](#what-you-will-learn)
2. [How Pose Tracking Works](#how-pose-tracking-works)
3. [Files](#files)
4. [Setup](#setup)
5. [Practice With Your Webcam First](#practice-with-your-webcam-first)
6. [Run the No-Fly Test](#run-the-no-fly-test)
7. [Before You Fly](#before-you-fly)
8. [Run the Program](#run-the-program)
9. [Poses and Commands](#poses-and-commands)
10. [How the Code Works](#how-the-code-works)
11. [Try This](#try-this)
12. [Troubleshooting](#troubleshooting)
13. [License](#license)

## What You Will Learn

* How an AI model estimates a person's **pose** (body position) from a single camera.
* How to write rules that compare body points ("is the wrist above the shoulder?").
* Why a controller should ignore points the model is not sure about (**visibility**).
* How the same program structure (threads, hold time, one move per pose) works for a different AI model.

## How Pose Tracking Works

MediaPipe's **Pose Landmarker** model returns 33 points on the body. This project uses these:

| Point | Body part |
| :---: | :--- |
| 11 / 12 | Left / right shoulder |
| 13 / 14 | Left / right elbow |
| 15 / 16 | Left / right wrist |
| 23 / 24 | Left / right hip |

Each point has:

* `x`, `y` – position in the image, from 0 to 1. Remember that `y` grows **downward**, so a wrist **above** a shoulder has a **smaller** `y`.
* `z` – rough depth. More negative means closer to the camera.
* `visibility` – how sure the model is that the point is actually visible (0 to 1).

**"Left" and "right" always mean *your* left and right**, not the left and right of the image. Because the drone is facing you, your left arm appears on the right side of its video.

## Files

| File | Purpose |
| :--- | :--- |
| `pose_controller.py` | Finds the body and decides the command. Run it by itself to practice with your webcam. |
| `test_pose_no_fly.py` | **Run this before flying.** Checks packages, the pose model, drone connection, battery, and video, then rehearses every pose on the drone's camera. The drone does not take off. |
| `tello_pose_control.py` | Main program. Connects to the Tello and turns poses into flight commands. |
| `requirements.txt` | Python packages needed by this project. |
| `pose_landmarker_lite.task` | The MediaPipe pose model (about 6 MB). Downloaded automatically on the first run. |

## Setup

Use the same course virtual environment (`.venv`) you created in [`00_Getting_Started`](../00_Getting_Started). From the repository root (or the PyCharm terminal):

```sh
pip install -r Tello_PoseCTRL/requirements.txt
```

> **Python version:** MediaPipe does not support every new Python release right away. If `pip` says it cannot find a version of `mediapipe`, your Python is probably too new. Python 3.12 works well for this course.

## Practice With Your Webcam First

While you are still on **normal internet** (not the Tello Wi‑Fi), run the controller by itself:

```sh
python pose_controller.py
```

The first time, this downloads the pose model into this folder. Then it opens your laptop webcam and shows the command it sees. Step back until your head, shoulders, arms, and hips are all in view, and practice each pose. No drone is involved.

## Run the No-Fly Test

`test_pose_no_fly.py` checks everything the flying program needs **without taking off**. The webcam practice above tests your poses; this test also checks the drone, its video, and the same threads the flying program uses. Run it every time before you fly.

```sh
python test_pose_no_fly.py
```

It works through five steps and stops at the first problem it cannot get past:

| Step | What it checks |
| :---: | :--- |
| 1 | The Python packages are installed. |
| 2 | The pose model file is present and MediaPipe can run it. |
| 3 | The computer can talk to the Tello, and the battery is charged enough. |
| 4 | The Tello video stream works. |
| 5 | **Live rehearsal.** The same threads and rules as `tello_pose_control.py` run on the live video. Stand 2–3 m away and show every pose; the rehearsal pretends to take off and land, so you can try the full sequence. The summary lists which poses were recognized. The command the drone *would* receive is shown on screen and in the terminal, but nothing is sent. Press **Q** to finish. |

At the end, a summary marks every check `PASS`, `WARN`, or `FAIL`:

* **READY TO FLY** – everything passed.
* **READY WITH WARNINGS** – you can fly, but read the warnings (for example, a command you did not test in Step 5).
* **NOT READY** – fix each `FAIL` (the message says how), then run the test again.

> 💡 No drone nearby? Set `USE_WEBCAM = True` at the top of `test_pose_no_fly.py` to skip the drone connection and run the test with your laptop webcam instead.

## Before You Fly

* The no-fly test above ended with **READY TO FLY** (or you have read its warnings).
* Stand **2–3 m in front of the drone** so your whole upper body is in view.
* **FORWARD moves the drone toward you**, 50 cm at a time. Leave room to step back.
* Only one person should be in view. Other people walking behind you can confuse the model.
* Keep someone at the laptop with a hand near the **Q** key. Pressing **Q** lands the drone.

## Run the Program

1. Power on the Tello and wait for the status light to blink.
2. Connect your computer to the Tello's Wi‑Fi network (`TELLO-XXXXXX`).
3. In PyCharm, right-click `tello_pose_control.py` → **Run**. Or, from this folder in a terminal:

   ```sh
   python tello_pose_control.py
   ```

4. Stand in front of the drone and raise **both arms** to take off.

The video window shows two lines:

* **Seen:** what the camera sees right now.
* **Active:** the command the drone is obeying. A pose becomes active only after you hold it steady for 0.5 s.

## Poses and Commands

| Pose | Command | What the drone does |
| :--- | :--- | :--- |
| Both wrists above your shoulders | `TAKE_OFF` | Takes off (only when on the ground). |
| Only **your left** wrist above your shoulder | `TURN_LEFT` | Rotates 45° counter-clockwise. |
| Only **your right** wrist above your shoulder | `TURN_RIGHT` | Rotates 45° clockwise. |
| Forearms crossed in an "X" in front of your chest | `LAND` | Lands and ends the program. |
| Both arms stretched straight toward the drone | `FORWARD` | Moves 50 cm forward, **toward you**. |
| Arms relaxed at your sides (or anything else) | `HOVER` | Stays in place. |
| No person visible, or arms hidden | `NO_PERSON` / `HOVER` | Stays in place. |

**One move per pose.** Raising one arm turns the drone **once**. To turn again, lower your arm for about half a second, then raise it again.

**After a turn, you may be out of view.** A 45° turn often moves you to the edge of the camera's view or out of it. When the drone cannot see you, it simply hovers. Walk back in front of it to continue.

## How the Code Works

```text
video_read_thread          main program                         pose_command_thread
─────────────────          ────────────                         ───────────────────
newest Tello frame   ──>   MediaPipe finds 33 body points
convert RGB → BGR          rules decide the command ("Seen")
                           held for 0.5 s? → "Active"   ──>     TAKE_OFF / LAND / move
                           draw skeleton and labels             or keep the drone hovering
                           check for Q key
```

The rules in `get_pose_command()` are checked in order, and the first match wins:

1. If a shoulder or wrist has `visibility` below 0.5 → `HOVER` (never fly based on a guess).
2. Both wrists above shoulders → `TAKE_OFF`.
3. Only the left wrist up → `TURN_LEFT`; only the right wrist up → `TURN_RIGHT`.
4. Your wrists have swapped sides, so your left wrist appears to the left of your right wrist in the image (arms crossed) → `LAND`.
5. Both wrists much closer to the camera than the shoulders → `FORWARD`.
6. Otherwise → `HOVER`.

Safety features built into `tello_pose_control.py`:

| Feature | Setting | Why |
| :--- | :--- | :--- |
| Relaxed arms = hover | (pose rules) | Standing normally never sends a command. |
| Hold time | `HOLD_TIME = 0.5` | While your arms move, they briefly pass through other poses. Waiting for a steady pose ignores those. |
| One move per pose | `ready_for_move` | A held pose does not repeat the move over and over. |
| Cooldown | `COMMAND_COOLDOWN = 1.0` | A short pause after each command. |
| Keep-alive | `KEEPALIVE_INTERVAL = 5.0` | The Tello lands by itself if it hears nothing for 15 seconds. While you hover, the program sends a "stay still" message every 5 seconds. |
| Safe exit | `try` / `finally` | Pressing **Q**, closing the program, or an error always lands the drone. |

## Try This

1. Change `ROTATE_DEGREES` to `20`. Do you stay in the camera's view after a turn?
2. Add a `BACK` command: for example, both hands on top of your head (both wrists above the shoulders **and** close together in `x`). Make it call `tello.move_back(50)`. Remember that the order of the rules matters, since `TAKE_OFF` is checked first.
3. Print the `z` values of your wrists and shoulders while practicing with the webcam. Is `-0.2` a good threshold for `FORWARD` for you?
4. In the webcam practice mode, hide one arm behind your back. What does the visibility check do?
5. **Challenge:** Make the drone keep you centered. Use the middle of your shoulders, `(landmarks[11].x + landmarks[12].x) / 2`, and rotate a little left or right when it drifts away from 0.5.

## Troubleshooting

| Problem | Likely cause and fix |
| :--- | :--- |
| `AttributeError: module 'mediapipe' has no attribute 'solutions'` | You are running last year's code. This year's code uses the newer MediaPipe **Tasks** API; pull the latest version of this repository. |
| `Could not download the pose model` | You are on the Tello Wi‑Fi, or offline. Connect to normal internet and run `python pose_controller.py` once. |
| `CERTIFICATE_VERIFY_FAILED` while downloading (macOS) | Your Python install needs its security certificates. Run **Install Certificates.command** in your `Applications/Python 3.x` folder, then try again. |
| `pip` cannot find `mediapipe` | Your Python version is too new for MediaPipe. Use Python 3.12. |
| Always `HOVER`, even with arms up | Your wrists or shoulders are out of view, so their visibility is low. Step back so your whole upper body is in the picture. |
| `TURN_LEFT` and `TURN_RIGHT` seem swapped | They follow **your** left and right, not the image's. Your left arm appears on the right side of the video. |
| `LAND` is hard to trigger | Cross your forearms clearly, with your wrists on opposite sides, and hold still for half a second. |

## License

This project is open-source and available under the [MIT License](LICENSE.md).
