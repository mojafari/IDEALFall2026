# Getting Started: Python + Tello

Welcome to the introductory section of **IDEAL Fall 2026 – Taking the Plunge: Intro to Drones & AI**.

Before working with computer vision, gesture recognition, pose estimation, QR codes, ArUco markers, or YOLO, you will first learn how to write Python programs and use Python to communicate with a DJI Tello drone.

This section is designed to take you from:

**Python beginner → Python programmer → Tello programmer → Computer Vision beginner**

---

## Learning Objectives

By completing this section, you should be able to:

- Explain why programming is important for drones.
- Understand how a computer executes a program line by line.
- Write basic Python programs.
- Use variables, print statements, comments, and basic data types.
- Understand and fix common Python errors.
- Use `if` statements to make decisions.
- Use `for` loops to repeat instructions.
- Create simple Python functions to organize and reuse code.
- Install Python packages.
- Create and use a Python virtual environment.
- Use PyCharm to create, run, and debug Python programs.
- Connect a Python program to a Tello drone.
- Check the Tello battery level.
- Send basic flight commands to the Tello.
- Program a simple flight path.
- Use loops to make drone programs shorter and easier to modify.
- Access the Tello camera.
- Display the Tello video stream using OpenCV.
- Understand how programming concepts connect to drone control and computer vision.


---

## Course Progression

The introductory activities follow this progression:

```text
Python Basics
      ↓
Python Debugging
      ↓
How Code Executes
      ↓
Making Decisions with IF
      ↓
Repeating Code with FOR
      ↓
Reusable Code with Functions
      ↓
Tello Connection
      ↓
Takeoff & Landing
      ↓
Tello Movement
      ↓
Programming a Flight Path
      ↓
Using Loops for Flight Paths
      ↓
Tello Camera
      ↓
OpenCV
      ↓
Computer Vision Projects
      ↓
AI-powered Drone Applications
```

The goal is to learn programming concepts before using them to control a physical drone.

---

# 1. Python Setup

## Install Python

Download Python from:

https://www.python.org/

After installation, verify that Python is available from your terminal or command prompt.

### Windows
Open Command Prompt or PowerShell and run:

```bash
python --version
```

### macOS / Linux
Open Terminal and run:

```bash
python3 --version
```

You should see a Python version such as:

```text
Python 3.x.x
```

Important: For this course, we recommend using a current Python 3 version that is compatible with the course libraries. If your instructor provides a specific Python version, use that version.


---

# 2. Install an IDE (e.g., PyCharm)

We recommend **PyCharm Community Edition** since we will use PyCharm as the primary development environment for this course.

Download PyCharm from:

https://www.jetbrains.com/pycharm/download/

Install PyCharm and open it after installation.
PyCharm will be used throughout the course to:
* Write Python programs.
* Run Python programs.
* Install Python packages.
* Manage the project environment.
* Debug programs.
* View error messages.
* Organize project files.

Note: You may use the terminal when appropriate, but the examples in this course will primarily use PyCharm.

Note: You may use another Python-compatible editor if you prefer.

---


# 3. Open the Course Repository in PyCharm

After downloading or cloning this repository, open the project in PyCharm.
From the PyCharm welcome screen:
* Select Open.
* Locate the course repository folder.
* Select the repository folder.
* Click Open.
You should see the project files in the Project panel.
For example:

IDEALFall2026/
│
├── README.md
├── requirements.txt
│
├── 01_python_basics.py
├── 02_debugging.py
├── 03_how_code_executes.py
├── 04_if_statements.py
├── 05_for_loops.py
├── 06_functions.py
├── 07_tello_connection.py
├── 08_tello_takeoff_land.py
├── 09_tello_movement.py
├── 10_tello_flight_path.py
├── 11_tello_flight_path_loop.py
└── 12_tello_video.py

# 3. Create a Virtual Environment

A virtual environment keeps the packages for this course separate from other Python projects on your computer.

Open a terminal in the course project folder.

### Windows

```bash
python -m venv .venv
```

Activate the environment:

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
```

Activate the environment:

```bash
source .venv/bin/activate
```

After activation, your terminal should indicate that the virtual environment is active.

---

# 4. Install the Required Libraries

Install the packages used in this section:

```bash
pip install -r requirements.txt
```

Or install them individually:

```bash
pip install djitellopy
pip install opencv-python
```

---

# 5. Test Python

Before connecting to a drone, make sure Python is working correctly.

Run:

```bash
python 01_python_basics.py
```

You should see output similar to:

```text
Hello, Drone!
Drone: Tello
Speed: 30
Height: 50
Tello will fly at 30 cm/s.
```

Try changing the values in the program and run it again.

---

# 6. Practice Debugging

Open:

```text
02_debugging.py
```

This file contains several intentionally broken Python examples.

Your goal is to:

1. Read the error message.
2. Identify the problem.
3. Fix the code.
4. Run the program again.

Common beginner errors include:

- Missing quotation marks
- Missing parentheses
- Incorrect variable names
- Incorrect capitalization
- Incorrect indentation
- Mixing strings and numbers

Learning to read error messages is an important programming skill.

---

# 7. Connect to the Tello

## Before connecting

Make sure:

- The Tello is powered on.
- Your computer is connected to the Tello Wi-Fi network.
- The drone is sitting on a safe, level surface.
- The flight area is clear.
- The battery is sufficiently charged.

Run:

```bash
python 03_tello_connection.py
```

The program should connect to the drone and display the battery percentage.

Example:

```text
Connected to Tello!
Battery: 87 %
```

---

# 8. First Flight: Takeoff and Land

Open:

```text
04_tello_takeoff_land.py
```

This program will:

1. Connect to the Tello.
2. Check the battery.
3. Take off.
4. Wait three seconds.
5. Land.

Run:

```bash
python 04_tello_takeoff_land.py
```

## Important

Do not modify flight commands until you understand what they do.

Always test flight programs in a safe, open area.

---

# 9. Tello Movement

Open:

```text
05_tello_movement.py
```

You will learn commands such as:

```python
drone.move_forward(50)
drone.move_back(50)

drone.move_left(50)
drone.move_right(50)

drone.move_up(50)
drone.move_down(50)

drone.rotate_clockwise(90)
drone.rotate_counter_clockwise(90)
```

The numbers represent distances in centimeters or angles in degrees, depending on the command.

For example:

```python
drone.move_forward(50)
```

means:

> Move forward approximately 50 centimeters.

And:

```python
drone.rotate_clockwise(90)
```

means:

> Rotate clockwise approximately 90 degrees.

---

# 10. Flight Path Challenge

Modify `05_tello_movement.py` to create your own flight path.

For example:

```text
Takeoff
   ↓
Forward
   ↓
Turn
   ↓
Forward
   ↓
Turn
   ↓
Return
   ↓
Land
```

Try to create a square-shaped flight path.

### Challenge

Can you modify your program so that the drone:

1. Takes off.
2. Moves forward 50 cm.
3. Turns 90 degrees.
4. Moves forward 50 cm.
5. Turns 90 degrees.
6. Repeats the pattern.
7. Lands.

---

# 11. Tello Camera

The Tello is not only a flying robot. It can also provide a live video stream.

Open:

```text
06_tello_video.py
```

This program uses:

- `djitellopy` to communicate with the drone.
- `OpenCV` to display the camera image.

Run:

```bash
python 06_tello_video.py
```

A window should appear showing the Tello's camera feed.

Press:

```text
Q
```

to close the video window.

---

# 12. From Video to Computer Vision

The basic video program contains an important idea that will be used throughout this course:

```text
Tello Camera
     ↓
Video Frame
     ↓
OpenCV
     ↓
Image Processing
     ↓
Detection
     ↓
Decision
     ↓
Drone Action
```

For example, later in the course we may build systems that:

```text
Tello Camera
     ↓
Detect a QR Code
     ↓
Determine its location
     ↓
Move the drone
```

or:

```text
Tello Camera
     ↓
Detect a person
     ↓
Recognize a pose
     ↓
Determine an action
     ↓
Control the drone
```

This is the foundation for the AI and computer-vision projects later in the course.

---

# 13. DJITelloPy API Reference

DJITelloPy provides a Python interface for communicating with the Tello.

Documentation:

https://djitellopy.readthedocs.io/en/latest/

Tello API:

https://djitellopy.readthedocs.io/en/latest/tello/

Use the documentation to investigate additional commands and capabilities.

Some useful commands include:

```python
drone.takeoff()
drone.land()

drone.move_forward(50)
drone.move_back(50)

drone.move_left(50)
drone.move_right(50)

drone.move_up(50)
drone.move_down(50)

drone.rotate_clockwise(90)
drone.rotate_counter_clockwise(90)
```

---

# 14. Mini-Project: "Hello, Drone!"

Create a new Python file called:

```text
hello_drone.py
```

Start with:

```python
from djitellopy import Tello
import time

drone = Tello()

drone.connect()

print("Battery:", drone.get_battery(), "%")

drone.takeoff()

time.sleep(3)

drone.land()
```

Modify the program to:

- Print a custom message before takeoff.
- Change the amount of time the drone remains in the air.
- Print the battery level.
- Add one safe movement command.
- Print a message when the flight is complete.

For example:

```text
Launching mission...
Battery: 92 %
Taking off...
Mission complete!
```

---

# 15. Pair Programming Challenge

Work with a partner.

One student is the **Driver** and one student is the **Navigator**.

### Driver

The Driver:

- Types the code.
- Runs the program.
- Makes the requested changes.

### Navigator

The Navigator:

- Reads the code.
- Checks for errors.
- Looks up API commands.
- Helps plan the flight path.

Switch roles halfway through the activity.

---

# 16. Safety Checklist

Before every flight:

- [ ] The Tello battery is sufficiently charged.
- [ ] The drone is on a stable surface.
- [ ] The flight area is clear.
- [ ] People are a safe distance away.
- [ ] There are no obstacles in the planned flight path.
- [ ] The computer is connected to the correct Tello Wi-Fi network.
- [ ] The program has been reviewed before running.
- [ ] You understand every flight command in the program.
- [ ] You know how to stop the flight if something goes wrong.

Never fly a drone indoors or outdoors where flight is prohibited or unsafe.

Follow your instructor's classroom flight rules and applicable local regulations.

---

# 17. Troubleshooting

## Python command not found

Try:

```bash
python --version
```

or:

```bash
python3 --version
```

If neither works, check that Python was installed correctly.

---

## DJITelloPy cannot be imported

If you see:

```text
ModuleNotFoundError: No module named 'djitellopy'
```

install the package:

```bash
pip install djitellopy
```

If you are using a virtual environment, make sure it is activated.

---

## Tello will not connect

Check:

1. Is the Tello powered on?
2. Is your computer connected to the Tello Wi-Fi?
3. Is another program already connected to the drone?
4. Is the Tello battery charged?
5. Are you running the correct Python environment?

---

## Video does not appear

Check:

- The Tello is connected.
- `streamon()` is being called.
- OpenCV is installed.
- No other application is using the Tello video stream.
- The program is being run from the correct Python environment.

---

# 18. What You Should Know Before Moving On

Before starting the computer-vision projects, you should be comfortable with:

- Basic Python syntax
- Variables
- Functions
- Imports
- Debugging
- Python packages
- Virtual environments
- Tello connection
- Battery checking
- Basic flight commands
- Tello video streaming
- Basic OpenCV concepts

Once you are comfortable with these concepts, move on to the computer-vision projects in the main course repository.

---

## Next Steps

After completing this section, continue with the project folders:

- [`Tello_Aruco`](../Tello_Aruco) – ArUco marker tracking
- [`Tello_QRCode`](../Tello_QRCode) – QR code tracking
- [`Tello_GestureCTRL`](../Tello_GestureCTRL) – Gesture-based control
- [`Tello_PoseCTRL`](../Tello_PoseCTRL) – Pose-based control
- [`Tello_YOLO`](../Tello_YOLO) – Object detection with YOLO

The goal is to move from **programming the drone directly** to **programming the drone to perceive and respond to its environment**.

---

## Resources

- Python: https://www.python.org/
- PyCharm: https://www.jetbrains.com/pycharm/download/
- DJITelloPy Documentation: https://djitellopy.readthedocs.io/en/latest/
- DJITelloPy Tello API: https://djitellopy.readthedocs.io/en/latest/tello/
- OpenCV Documentation: https://docs.opencv.org/

---

**IDEAL Fall 2026 – Taking the Plunge: Intro to Drones & AI**
