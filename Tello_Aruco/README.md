# Tello ArUco Marker Control

[![Python 3.10–3.12](https://img.shields.io/badge/Python-3.10–3.12-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.7+-blueviolet.svg)](https://opencv.org/)
[![DJITelloPy](https://img.shields.io/badge/DJITelloPy-library-informational.svg)](https://github.com/damiafuentes/DJITelloPy)

Hold up a printed ArUco marker in front of the Tello, and the drone performs a flip. Show marker `0` and it lands.

This is the simplest vision-based control project in the course: **camera → detect marker → read its ID → send a command**. Every other project in this repository follows the same pattern with a more advanced detector.

### Table of Contents
1. [What You Will Learn](#what-you-will-learn)
2. [What Is an ArUco Marker?](#what-is-an-aruco-marker)
3. [Files](#files)
4. [Setup](#setup)
5. [Run the No-Fly Test First](#run-the-no-fly-test-first)
6. [Before You Fly](#before-you-fly)
7. [Run the Program](#run-the-program)
8. [Marker IDs and Commands](#marker-ids-and-commands)
9. [How the Code Works](#how-the-code-works)
10. [Try This](#try-this)
11. [Troubleshooting](#troubleshooting)
12. [License](#license)

## What You Will Learn

* How to process live video from the Tello one frame at a time.
* How OpenCV detects ArUco markers and reports their IDs.
* How to turn what the camera sees into a drone command using `if` / `elif`.
* Why a **cooldown** is needed so one marker does not trigger the same command many times.
* Why the program uses **threads**, so the video keeps running while the drone flips.
* How to check that everything works with a **no-fly test** before the drone leaves the ground.

## What Is an ArUco Marker?

An ArUco marker is a black-and-white square pattern, similar to a simple QR code. Each pattern stands for a number (its **ID**). Markers come in families called **dictionaries**; this project uses `DICT_4X4_50`, which has 50 markers (IDs 0–49) built from a 4×4 grid. Because the patterns are simple and high-contrast, a computer can find them quickly and reliably, which makes them popular in robotics.

## Files

| File / Folder | Purpose |
| :--- | :--- |
| `test_Aruco_no_fly.py` | **Run this first.** Checks packages, detector, drone connection, battery, and video, then rehearses with live markers. The drone does not take off. |
| `test_Aruco.py` | Main program. Takes off, watches for markers, and flips or lands. |
| `requirements.txt` | Python packages needed by `test_Aruco.py`. |
| `Aruco_Generator/` | Script that creates printable, letter-sized marker PDFs. See its [README](Aruco_Generator/README.md). |
| `Aruco_Generator/Sample_Aruco/` | Ready-to-print markers for IDs 0–4 (PDF, PNG, JPG). |

## Setup

Use the same course virtual environment (`.venv`) you created in [`00_Getting_Started`](../00_Getting_Started). You do **not** need a new environment for each project.

From the repository root (or the PyCharm terminal), install the packages:

```sh
pip install -r Tello_Aruco/requirements.txt
```

Then print the markers in `Aruco_Generator/Sample_Aruco/` (the PDFs print one marker per letter page). Leave the white border around each marker; the detector needs it.

## Run the No-Fly Test First

`test_Aruco_no_fly.py` checks everything the flying program needs **without taking off**. Run it every time before you fly, especially on a new laptop or after installing packages.

```sh
python test_Aruco_no_fly.py
```

It works through five steps and stops at the first problem it cannot get past:

| Step | What it checks |
| :---: | :--- |
| 1 | The Python packages are installed. |
| 2 | The ArUco detector works (the computer draws a marker and detects it). |
| 3 | The computer can talk to the Tello, and the battery is charged enough. |
| 4 | The Tello video stream works. |
| 5 | **Live rehearsal.** The same threads and rules as `test_Aruco.py` run on the live video. Hold up each printed marker (0–4); the summary lists which ones were detected. The command the drone *would* receive is shown on screen and in the terminal, but nothing is sent. Press **Q** to finish. |

At the end, a summary marks every check `PASS`, `WARN`, or `FAIL`:

* **READY TO FLY** – everything passed.
* **READY WITH WARNINGS** – you can fly, but read the warnings (for example, a command you did not test in Step 5).
* **NOT READY** – fix each `FAIL` (the message says how), then run the test again.

> 💡 No drone nearby? Set `USE_WEBCAM = True` at the top of `test_Aruco_no_fly.py` to skip the drone connection and run the test with your laptop webcam instead.

## Before You Fly

* Battery above **50%**. The Tello refuses to flip when the battery is low; the program prints a warning if it is.
* Fly in an open area with at least 2 m of clear space on every side and above. Flips move the drone quickly.
* Keep everyone out of the flight area, and keep your hand near the **Q** key.
* The drone **takes off automatically** as soon as the program starts.

## Run the Program

1. Power on the Tello and wait for the status light to blink.
2. Connect your computer to the Tello's Wi‑Fi network (`TELLO-XXXXXX`).
3. In PyCharm, right-click `test_Aruco.py` → **Run**. Or, from this folder in a terminal:

   ```sh
   python test_Aruco.py
   ```

The program will:

* Connect to the Tello and print the battery level.
* Open a window showing the live video, then take off. Detected markers are outlined.
* Flip when it sees marker 1, 2, 3, or 4 (then wait 3 seconds before another flip is allowed).
* Land and exit when it sees marker 0 or when you press **Q**.

## Marker IDs and Commands

Dictionary: `DICT_4X4_50`

| Marker ID | Command |
| :---: | :--- |
| 0 | Land and end the program |
| 1 | Flip forward |
| 2 | Flip back |
| 3 | Flip left |
| 4 | Flip right |

If several markers are visible at once, the program uses the first one OpenCV reports.

## How the Code Works

`tello.flip_forward()` does not return until the flip is finished. If the program waited for it inside the video loop, the video would freeze during every flip. So the work is split between **three parts that run at the same time**:

```text
video_read_thread            main program                       command_thread
─────────────────            ────────────                       ──────────────
newest Tello frame     ──>   detect markers                     take off
convert RGB → BGR            draw them                          wait for a request:
save as latest_frame         marker ID → command    ──────>       LAND → land and stop
repeat                       (pending_command)                    flip → flip (if cooldown passed)
                             show video, check Q                  nothing for 5 s → keep-alive
                                                                land when the program ends
```

A few details worth noticing in `test_Aruco.py`:

* **`MARKER_COMMANDS`** is a dictionary that links each marker ID to a command name. To add a marker, add a line here and a branch in `run_command()`.
* **Locks.** `frame_lock` and `command_lock` make sure two threads never change the same variable at the same moment.
* **Color conversion.** `djitellopy` delivers frames in RGB order, but OpenCV expects BGR. Without `cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)`, reds and blues are swapped.
* **`ids` is a list of lists.** When two markers are visible, `ids` looks like `[[3], [1]]`. The code reads `ids[0][0]` to get the first ID as a plain number.
* **Cooldown.** A marker usually stays in view for many frames. `COMMAND_COOLDOWN` stops the drone from queuing flip after flip.
* **Keep-alive.** The Tello lands by itself if it hears nothing for 15 seconds. While waiting for a marker, the command thread sends a "stay still" message every 5 seconds.
* **Always land.** The command thread's `finally` block lands the drone, whether the program ends normally, you press **Q**, or something goes wrong.

## Try This

1. Change `FLIP_COOLDOWN` to `1.0` and then to `6.0`. How does the drone behave differently?
2. Add marker ID `5` that makes the drone move up 30 cm: add `5: "UP"` to `MARKER_COMMANDS` and a branch that calls `tello.move_up(30)` in `run_command()`. Generate the marker with the generator script, and check it with the no-fly test first.
3. Make the drone rotate 90° (`tello.rotate_clockwise(90)`) instead of flipping for one of the markers.
4. Print the marker's position on the screen. `corners[0][0]` holds the four corner points of the first marker. Can you tell whether the marker is on the left or right side of the image?
5. **Challenge:** Use the marker's position to make the drone turn toward it (turn left if the marker is on the left side of the image, right if it is on the right side).

## Troubleshooting

| Problem | Likely cause and fix |
| :--- | :--- |
| `AttributeError: module 'cv2' has no attribute 'aruco'` or no `ArucoDetector` | OpenCV is older than 4.7. Run `pip install --upgrade opencv-python`. |
| Colors look wrong (blue skin, orange sky) | The RGB → BGR conversion line was removed. Keep `cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)`. |
| Marker is not detected | Keep the white border around the marker, avoid glare on glossy paper, and hold the marker 0.5–2 m from the camera. Make sure the marker is from `DICT_4X4_50`. |
| Drone does not flip | Battery is at or below about 50%. Charge it. |
| Program cannot connect | Check that your computer is on the `TELLO-XXXXXX` Wi‑Fi and that no other program is connected to the drone. |

## License

This project is open-source and available under the [MIT License](LICENSE.md).
