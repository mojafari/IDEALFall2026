# Tello + YOLO Object Detection

[![Python 3.10–3.12](https://img.shields.io/badge/Python-3.10–3.12-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.7+-blueviolet.svg)](https://opencv.org/)
[![Ultralytics YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-brightgreen.svg)](https://docs.ultralytics.com/)
[![DJITelloPy](https://img.shields.io/badge/DJITelloPy-library-informational.svg)](https://github.com/damiafuentes/DJITelloPy)

The Tello flies a square while an AI model called **YOLO** watches its video and labels everything it recognizes: people, chairs, backpacks, bottles, laptops, and about 80 kinds of everyday objects.

In the ArUco and QR code projects, the drone looked for special printed patterns. Here, the drone recognizes ordinary objects, using a neural network that learned from hundreds of thousands of labeled photos.

### Table of Contents
1. [What You Will Learn](#what-you-will-learn)
2. [What Is YOLO?](#what-is-yolo)
3. [Files](#files)
4. [Setup](#setup)
5. [Run the No-Fly Test First](#run-the-no-fly-test-first)
6. [Before You Fly](#before-you-fly)
7. [Run the Program](#run-the-program)
8. [How the Code Works](#how-the-code-works)
9. [Try This](#try-this)
10. [Troubleshooting](#troubleshooting)
11. [License](#license)

## What You Will Learn

* How to run a pre-trained AI model on live drone video.
* What **object detection** (finding objects) and **tracking** (following the same object across frames) mean.
* How **threads** let the drone fly and the video update at the same time.
* How a `for` loop turns a square flight path into a few lines of code (as in `00_Getting_Started/11_tello_flight_path_loop.py`).

## What Is YOLO?

**YOLO** stands for **"You Only Look Once."** It looks at a whole image in a single pass and returns a list of boxes, each with a label (such as `person`) and a confidence score (such as `0.87`, meaning 87% sure). Doing everything in one pass is what makes it fast enough for live video.

The model used here, `yolov8n.pt`, is the **nano** version of YOLOv8: the smallest and fastest one, which runs well on a normal laptop without a graphics card. It was trained on the [COCO dataset](https://cocodataset.org/), so it knows 80 common object types.

## Files

| File | Purpose |
| :--- | :--- |
| `test_YOLO_no_fly.py` | **Run this first.** Checks packages, the model, tracking, drone connection, battery, and video, then rehearses the flight while YOLO labels the live video. The drone does not take off. |
| `test_sim_cam_sqv1_YOLO.py` | Main program. Flies a square and shows YOLO detections on the live video. |
| `requirements.txt` | Python packages needed by the program. |
| `yolov8n.pt` | The YOLO model file. It is downloaded automatically on the first run (see below). |

## Setup

Use the same course virtual environment (`.venv`) you created in [`00_Getting_Started`](../00_Getting_Started). From the repository root (or the PyCharm terminal):

```sh
pip install -r Tello_YOLO/requirements.txt
```

`ultralytics` is a large package (it installs PyTorch), so this can take several minutes.

### Download the model before class

When your computer is connected to the Tello's Wi‑Fi, it has **no internet**. So download the model first, while you are on normal internet. From this folder, run:

```sh
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

This saves `yolov8n.pt` in this folder. If the file is already there, nothing is downloaded.

## Run the No-Fly Test First

`test_YOLO_no_fly.py` checks everything the flying program needs **without taking off**. Run it every time before you fly, especially on a new laptop or after installing packages.

```sh
python test_YOLO_no_fly.py
```

It works through five steps and stops at the first problem it cannot get past:

| Step | What it checks |
| :---: | :--- |
| 1 | The Python packages are installed. |
| 2 | The YOLO model file loads, finds objects in a sample photo, and tracking works (this needs the `lap` package). |
| 3 | The computer can talk to the Tello, and the battery is charged enough. |
| 4 | The Tello video stream works. |
| 5 | **Live rehearsal.** The same threads and rules as `test_sim_cam_sqv1_YOLO.py` run on the live video. YOLO labels the live video while a pretend command thread prints each step of the square (about 25 seconds). Check that the video keeps moving while the steps run: that is what the threads are for. The command the drone *would* receive is shown on screen and in the terminal, but nothing is sent. Press **Q** to finish. |

At the end, a summary marks every check `PASS`, `WARN`, or `FAIL`:

* **READY TO FLY** – everything passed.
* **READY WITH WARNINGS** – you can fly, but read the warnings (for example, a command you did not test in Step 5).
* **NOT READY** – fix each `FAIL` (the message says how), then run the test again.

> 💡 No drone nearby? Set `USE_WEBCAM = True` at the top of `test_YOLO_no_fly.py` to skip the drone connection and run the test with your laptop webcam instead.

## Before You Fly

* The drone **takes off automatically** and flies a **1 m × 1 m square**. Clear at least 2 m × 2 m of floor, plus space above.
* Put the drone down facing an open direction; its first move is 1 m forward.
* Keep everyone out of the flight area, and keep your hand near the **Q** key.
* Battery above 30%.

## Run the Program

1. Power on the Tello and wait for the status light to blink.
2. Connect your computer to the Tello's Wi‑Fi network (`TELLO-XXXXXX`).
3. In PyCharm, right-click `test_sim_cam_sqv1_YOLO.py` → **Run**. Or, from this folder in a terminal:

   ```sh
   python test_sim_cam_sqv1_YOLO.py
   ```

The program will:

* Load the YOLO model, connect to the Tello, and print the battery level.
* Open a video window with a box and label around every object YOLO recognizes.
* Take off, fly four sides of a square (forward 100 cm, turn 90°), and land.
* End by itself after landing. Pressing **Q** stops the flight early: the drone finishes its current move and then lands.

## How the Code Works

The program does two jobs at the same time, so it uses two threads plus the main program:

```text
video_read_thread            command_thread_function         main program
─────────────────            ───────────────────────         ────────────
get newest frame             takeoff                          take newest frame
convert RGB → BGR            repeat 4 times:                  run YOLO on it
save as latest_frame  ──┐      move forward 100 cm      ┌──>  draw boxes and labels
repeat                  │      rotate 90°               │     show the video
                        │    land                       │     check for Q key
                        └──────── latest_frame ─────────┘
```

* **Why threads?** `tello.move_forward(100)` does not return until the move is finished, which takes a few seconds. If the video were in the same loop, it would freeze during every move.
* **Why a lock?** `frame_lock` makes sure the main program never reads `latest_frame` while the video thread is in the middle of replacing it.
* **`model.track()`** detects objects and gives each one an ID number that stays the same while it remains in view (look for `id:1`, `id:2` in the labels).
* **Color conversion.** `djitellopy` delivers frames in RGB order, but YOLO and OpenCV expect BGR. Without the conversion, colors look wrong and detection gets less accurate.

## Try This

1. Change `SIDE_LENGTH_CM` to `50` and `NUMBER_OF_SIDES` to `3`. What shape does the drone fly now?
2. Print what YOLO finds. After `results = model.track(...)`, add:

   ```python
   for box in results[0].boxes:
       name = model.names[int(box.cls)]
       confidence = float(box.conf)
       print(name, round(confidence, 2))
   ```

3. Show only people: change the tracking line to `model.track(frame, persist=True, verbose=False, classes=[0])` (class 0 is `person`).
4. Try a newer or larger model by changing `MODEL_NAME` (for example `yolov8s.pt`, the "small" model). Is it more accurate? Is the video slower?
5. **Challenge:** Make the drone land as soon as YOLO sees a `stop sign` or a `cell phone`. (Hint: the main program can set `is_running = False`.)

## Troubleshooting

| Problem | Likely cause and fix |
| :--- | :--- |
| Error while loading `yolov8n.pt` (download failed, or "file is not a zip / corrupt") | You were on the Tello Wi‑Fi, or an earlier download stopped halfway. Delete `yolov8n.pt`, connect to normal internet, and run the download command in [Setup](#download-the-model-before-class). |
| `ModuleNotFoundError: No module named 'lap'`, or Ultralytics tries to install `lap` | Run `pip install lap` while on normal internet. `model.track()` needs it. |
| Video is slow or choppy | YOLO is running on your laptop's CPU. Close other programs, or try `model.track(frame, persist=True, verbose=False, imgsz=320)` for a smaller, faster input. |
| Colors look wrong | The RGB → BGR conversion line in `video_read_thread` was removed. |
| Program cannot connect | Check that your computer is on the `TELLO-XXXXXX` Wi‑Fi and that no other program is connected to the drone. |

## License

This project is open-source and available under the [MIT License](LICENSE.md).
