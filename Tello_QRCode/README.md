# Tello QR Code Control

[![Python 3.10–3.12](https://img.shields.io/badge/Python-3.10–3.12-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.7+-blueviolet.svg)](https://opencv.org/)
[![DJITelloPy](https://img.shields.io/badge/DJITelloPy-library-informational.svg)](https://github.com/damiafuentes/DJITelloPy)

Show the Tello a printed QR code, and it reads the text inside and performs that command: `flip_left` makes it flip left, `stop` makes it land.

This project works just like [`Tello_Aruco`](../Tello_Aruco), but instead of a number, each code carries **text**. That means you can invent new commands just by printing a new QR code with new words.

### Table of Contents
1. [What You Will Learn](#what-you-will-learn)
2. [QR Codes vs. ArUco Markers](#qr-codes-vs-aruco-markers)
3. [Files](#files)
4. [Setup](#setup)
5. [Run the No-Fly Test First](#run-the-no-fly-test-first)
6. [Before You Fly](#before-you-fly)
7. [Run the Program](#run-the-program)
8. [QR Codes and Commands](#qr-codes-and-commands)
9. [How the Code Works](#how-the-code-works)
10. [Student Projects from Fall 2025](#student-projects-from-fall-2025)
11. [Try This](#try-this)
12. [Troubleshooting](#troubleshooting)
13. [License](#license)

## What You Will Learn

* How to detect and decode QR codes in live video with OpenCV's `QRCodeDetector`.
* How to compare text (strings) with `if` / `elif` to choose a drone command.
* Why a **cooldown** is needed so one QR code does not trigger the same command many times.
* Why the program uses **threads**, so the video keeps running while the drone flips.
* How to check that everything works with a **no-fly test** before the drone leaves the ground.

## QR Codes vs. ArUco Markers

| | ArUco marker | QR code |
| :--- | :--- | :--- |
| Stores | A number (ID) | Text (words, links, numbers) |
| Detection distance | Longer (simpler pattern) | Shorter (more detail to read) |
| Speed | Very fast | A little slower |
| Good for | Robot navigation, tracking | Labels, instructions, "missions" |

Because a QR code stores more information in the same space, the camera needs to be closer and the image sharper to read it.

## Files

| File / Folder | Purpose |
| :--- | :--- |
| `test_QRCode_no_fly.py` | **Run this first.** Checks packages, QR reader, drone connection, battery, and video, then rehearses with your printed codes. The drone does not take off. |
| `test_QRCode.py` | Main program. Takes off, reads QR codes, and flips or lands. |
| `requirements.txt` | Python packages needed by `test_QRCode.py`. |
| `QRCode_Generator/` | Script that creates printable, letter-sized QR code PDFs. See its [README](QRCode_Generator/README.md). |
| `Group1/`, `Group2/` | Projects built by student groups in Fall 2025. See [below](#student-projects-from-fall-2025). |

## Setup

Use the same course virtual environment (`.venv`) you created in [`00_Getting_Started`](../00_Getting_Started). From the repository root (or the PyCharm terminal):

```sh
pip install -r Tello_QRCode/requirements.txt
pip install -r Tello_QRCode/QRCode_Generator/requirements.txt
```

Then generate and print the QR codes (see the [generator README](QRCode_Generator/README.md)). The text inside each code must **exactly** match the text in `test_QRCode.py`, including lowercase letters and underscores.

## Run the No-Fly Test First

`test_QRCode_no_fly.py` checks everything the flying program needs **without taking off**. Run it every time before you fly, especially on a new laptop or after installing packages.

```sh
python test_QRCode_no_fly.py
```

It works through five steps and stops at the first problem it cannot get past:

| Step | What it checks |
| :---: | :--- |
| 1 | The Python packages are installed. |
| 2 | The QR code reader works (the computer draws a QR code and reads it). |
| 3 | The computer can talk to the Tello, and the battery is charged enough. |
| 4 | The Tello video stream works. |
| 5 | **Live rehearsal.** The same threads and rules as `test_QRCode.py` run on the live video. Hold up each printed QR code; the summary lists which ones were read, and warns about codes with misspelled text. The command the drone *would* receive is shown on screen and in the terminal, but nothing is sent. Press **Q** to finish. |

At the end, a summary marks every check `PASS`, `WARN`, or `FAIL`:

* **READY TO FLY** – everything passed.
* **READY WITH WARNINGS** – you can fly, but read the warnings (for example, a command you did not test in Step 5).
* **NOT READY** – fix each `FAIL` (the message says how), then run the test again.

> 💡 No drone nearby? Set `USE_WEBCAM = True` at the top of `test_QRCode_no_fly.py` to skip the drone connection and run the test with your laptop webcam instead.

## Before You Fly

* Battery above **50%**. The Tello refuses to flip when the battery is low; the program prints a warning if it is.
* Fly in an open area with at least 2 m of clear space on every side and above. Flips move the drone quickly.
* Keep everyone out of the flight area, and keep your hand near the **Q** key.
* The drone **takes off automatically** as soon as the program starts.

## Run the Program

1. Power on the Tello and wait for the status light to blink.
2. Connect your computer to the Tello's Wi‑Fi network (`TELLO-XXXXXX`).
3. In PyCharm, right-click `test_QRCode.py` → **Run**. Or, from this folder in a terminal:

   ```sh
   python test_QRCode.py
   ```

The program will:

* Connect to the Tello and print the battery level.
* Open a window showing the live video, then take off. A green box surrounds any QR code, with its text above it.
* Perform a flip when it reads a flip command (then wait 3 seconds before another command is allowed).
* Land and exit when it reads `stop` or when you press **Q**.

## QR Codes and Commands

| QR code text | Command |
| :---: | :--- |
| `stop` | Land and end the program |
| `flip_forward` | Flip forward |
| `flip_back` | Flip back |
| `flip_left` | Flip left |
| `flip_right` | Flip right |

Any other text is printed in the terminal as an unknown QR code and ignored.

## How the Code Works

`tello.flip_forward()` does not return until the flip is finished. If the program waited for it inside the video loop, the video would freeze during every flip. So the work is split between **three parts that run at the same time**:

```text
video_read_thread            main program                       command_thread
─────────────────            ────────────                       ──────────────
newest Tello frame     ──>   read QR code                       take off
convert RGB → BGR            draw box and text                  wait for a request:
save as latest_frame         text → command         ──────>       LAND → land and stop
repeat                       (pending_command)                    flip → flip (if cooldown passed)
                             show video, check Q                  nothing for 5 s → keep-alive
                                                                land when the program ends
```

A few details worth noticing in `test_QRCode.py`:

* **`QR_COMMANDS`** is a dictionary that links each QR code text to a command name. To add a command, add a line here and a branch in `run_command()`.
* **Two results.** `detectAndDecode()` can *find* a QR code (so `points` is not `None`) but still fail to *read* it (so `text` is empty). This happens when the code is far away, blurry, or tilted. The green box shows that it was found; the text appears only when it was read.
* **Locks.** `frame_lock` and `command_lock` make sure two threads never change the same variable at the same moment.
* **Color conversion.** `djitellopy` delivers frames in RGB order, but OpenCV expects BGR. The code converts every frame so colors look right.
* **Cooldown.** `COMMAND_COOLDOWN` stops the drone from queuing flip after flip while a code stays in view.
* **Keep-alive.** The Tello lands by itself if it hears nothing for 15 seconds. While waiting for a code, the command thread sends a "stay still" message every 5 seconds.
* **Always land.** The command thread's `finally` block lands the drone, whether the program ends normally, you press **Q**, or something goes wrong.

## Student Projects from Fall 2025

These folders keep the work of two student groups from last year as examples. Read them to see how others extended the basic program; each has its own README.

* [`Group1/`](Group1) – Runs QR detection in its own thread so the video stays smooth while the drone is busy. This year's `test_QRCode.py` builds on the same idea.
* [`Group2/`](Group2) – A "find the right door" mission: the drone turns until it reads the QR code on the correct door.

## Try This

1. Add a new command, `up`, that calls `tello.move_up(30)`: add `"up": "UP"` to `QR_COMMANDS` and a branch in `run_command()`. Generate a QR code with the text `up`, and check it with the no-fly test first.
2. Replace the flips with movements (`move_left(50)`, `move_right(50)`) so the program works even when the battery is below 50%.
3. Put a sentence in a QR code, such as `rotate 90`. Use `text.split()` to separate the command from the number, then call `tello.rotate_clockwise(int(number))`.
4. **Challenge:** Build a "treasure hunt". Tape QR codes around the room, where each code tells the drone which way to turn to find the next code.

## Troubleshooting

| Problem | Likely cause and fix |
| :--- | :--- |
| Green box appears but no text | The code was found but not read. Move it closer (0.5–1 m), hold it still, and avoid glare. |
| Nothing happens when the code is visible | The text in the QR code does not exactly match the program (check capitals, spaces, and underscores). The terminal prints `Unknown QR code: ...` in that case. |
| Drone does not flip | Battery is at or below about 50%. Charge it. |
| Colors look wrong | The RGB → BGR conversion line was removed. Keep `cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)`. |
| Program cannot connect | Check that your computer is on the `TELLO-XXXXXX` Wi‑Fi and that no other program is connected to the drone. |

## License

This project is open-source and available under the [MIT License](LICENSE.md).
