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

```text
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
```

The exact repository structure may change as the course is updated.

---

# 4. Create a Python Virtual Environment in PyCharm

A virtual environment keeps the packages for this course separate from other Python projects on your computer.

We recommend creating a virtual environment named:

```text
.venv
```

## Option A: Create the Environment When Creating the Project
If you are creating the project from scratch in PyCharm:
* Open PyCharm.
* Select New Project.
* Select Python.
* Choose your project location.
* Under Python Interpreter, select New Virtualenv Environment.
* Name the environment .venv.
* Select the appropriate Python version.
* Click Create.
---
## Option B: Create the Environment for an Existing Project
If you already opened the repository:
* Open Settings in PyCharm.

On Windows/Linux:

```text
File → Settings
```

On macOS:
```text
PyCharm → Settings
```
* Go to:
```text
Project → Python Interpreter
```
* Select Add Interpreter.
* Select Add Local Interpreter.
* Choose Virtualenv Environment.
* Select New.
* Use:
```text
.venv
```
as the environment location.
* Select the appropriate Python version.
* Click OK or Apply.

PyCharm should now use the .venv environment for this project.

---

# 5. Verify the Python Interpreter in PyCharm

Before installing packages, make sure PyCharm is using the correct interpreter.

Look for the Python interpreter selector in PyCharm.

It should show something similar to:
```text
Python 3.x (.venv)
```
You can also check:
```text
Settings → Project → Python Interpreter
```
The interpreter should point to your project's .venv.

For example, on Windows it may look similar to:
```text
...\IDEALFall2026\.venv\Scripts\python.exe
```
On macOS/Linux:
```text
.../IDEALFall2026/.venv/bin/python
```
Important: Installing a package into one Python environment does not automatically install it into every Python environment. Make sure you are installing packages into the same .venv environment that PyCharm uses to run your programs.

---

# 6. Install the Required Libraries

This course uses several Python libraries.

The most important libraries for this introductory section are:
* DJITelloPy – communicates with the Tello drone.
* OpenCV – works with images and video.

There are two recommended ways to install packages.

---

## Option A: Install Packages Through PyCharm

This is the recommended method for beginners.

### Using the Python Interpreter window
* Open:

```text
Settings → Project → Python Interpreter
```

* Make sure the selected interpreter is your .venv.
* Click the + button to add a package.
* Search for:

```text
djitellopy
```

* Select the package.
* Click Install Package.

Repeat the process for:

```text
opencv-python
```

After installation, the packages should appear in the list of installed packages.


---

## Option B: Install Packages Through the PyCharm Terminal

PyCharm includes a built-in terminal.

Open:

```text
View → Tool Windows → Terminal
```

If your virtual environment is configured correctly, the terminal should use the project's .venv.

Install DJITelloPy:

```bash
pip install djitellopy
```

Install OpenCV:

```bash
pip install opencv-python
```

You can also install all project dependencies at once:

```bash
pip install -r requirements.txt
```


---

## Option C: Install Packages Using the System Terminal

You can also use your computer's normal terminal.

If your virtual environment is activated, run:

```bash
pip install -r requirements.txt
```

Or install the packages individually:

```bash
pip install djitellopy
pip install opencv-python
```


### Windows
Activate the virtual environment first:

```bash
.venv\Scripts\activate
```

Then:

```bash
pip install -r requirements.txt
```

### macOS / Linux
Activate the virtual environment first:

```bash
source .venv/bin/activate
```

Then:

```bash
pip install -r requirements.txt
```

---

# 7. Test Your Python Environment

Before connecting to a drone, make sure Python is working correctly.

Open:

```text
01_python_basics.py
```

In PyCharm, right-click the file and select:

```text
Run '01_python_basics'
```

You can also use the green Run ▶ button in PyCharm.

Alternatively, from the terminal:

```bash
python 01_python_basics.py
```

On some macOS/Linux systems you may use:

```bash
python3 01_python_basics.py
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

# 8. Python Basics

Open:

```text
01_python_basics.py
```

In this activity, you will learn some of the basic building blocks of Python.

You will practice:
* print()
* Variables
* Strings
* Numbers
* Comments

For example:

```python
drone_name = "Tello"
speed = 30
height = 50

print("Drone:", drone_name)
print("Speed:", speed)
print("Height:", height)

```

### Think About It
What happens if you change:

```python
speed = 30
```
to:

```python
speed = 50
```

How does the output change?


---

# 9. Practice Debugging

Open:

```text
02_debugging.py
```

This file contains several intentionally broken Python examples.

Your goal is to:

1. Run the program.
2. Read the error message.
3. Identify the problem.
4. Fix the code.
5. Run the program again.

Common beginner errors include:

- Missing quotation marks
- Missing parentheses
- Incorrect variable names
- Incorrect capitalization
- Incorrect indentation
- Mixing strings and numbers

For example:

```python
print("Welcome to drone class)
```
contains a missing quotation mark.

A corrected version is:

```python
print("Welcome to drone class")
```

## Debugging in PyCharm

PyCharm will display errors in the editor and in the Run window.

When you see an error:
* Read the error message.
* Look at the line number.
* Find the problem in the code.
* Make a correction.
* Run the program again.

Learning to read error messages is an important programming skill.

When your drone programs become more complicated, errors are normal.

The goal is not to avoid every error.

The goal is to learn how to find and fix errors.

---

# 10. How Does Python Execute Code?

Open:

```text
03_how_code_executes.py
```

A computer program is a sequence of instructions.

Python normally executes statements from top to bottom.

For example:

```python
print("Step 1")
print("Step 2")
print("Step 3")
```

Python executes the program like this:

```text
print("Step 1")
      ↓
print("Step 2")
      ↓
print("Step 3")
```

The output is:

```text
Step 1
Step 2
Step 3
```

Understanding this idea is important because programming structures such as if statements and loops can change how the program flows.

## Predict Before You Run

Look at this program:

```python
print("Taking off")

height = 50

print("Height:", height)

print("Moving forward")

print("Landing")
```

Before running the program, write down what you think the output will be.

Then run the program and compare your prediction with the actual result.
### Key Idea
A program is not magic.

The computer follows instructions one step at a time.

---

# 11. Making Decisions with if

Open:

```text
04_if_statements.py
```

Programs often need to make decisions.

For example:

If the battery is low, do not fly.

An if statement allows Python to check a condition.

```python
battery = 15

if battery < 20:
    print("Battery is too low for flight.")
```

Python asks:

```text
Is battery less than 20?
        ↓
      YES
        ↓
Print the warning
```

If the condition is false, the indented code is skipped.

---

## if and else
We can provide two possible outcomes:

```python
battery = 80

if battery < 20:
    print("Battery is too low for flight.")
else:
    print("Battery level is OK.")
```

The program now behaves like this:

```text
             Battery
                ↓
         Is battery < 20?
            ↙       ↘
          YES        NO
           ↓          ↓
      Do not fly   Ready to fly
```

This is an important programming concept:

Get information → Make a decision → Take an action

Later, the Tello will provide the information.

For example:

```python
battery = tello.get_battery()

if battery < 20:
    print("Do not fly!")
else:
    print("Ready for flight!")

```

---

## Your Turn
Create a variable called speed.

If the speed is greater than 50, print:

```text
The drone is moving fast.
```

Otherwise, print:

```text
The drone is moving slowly.
```

Try several different speed values.


---

# 12. Repeating Code with for

Open:

```text
05_for_loops.py
```

Computers are very good at repeating instructions.

Consider this code:

```python
print("Hello")
print("Hello")
print("Hello")
print("Hello")
print("Hello")
```

This works, but it is repetitive.

What if we wanted to print the message 100 times?

We would not want to write 100 print() statements.

Instead, we can use a for loop:


```python
for i in range(5):
    print("Hello")
```

The loop tells Python:

Repeat the indented instructions five times.

```python
for i in range(5):
    print("Hello")
```

---

## Understanding range()
Consider:

```python
for i in range(5):
    print("Loop number:", i)
```

The output is:

```text
Loop number: 0
Loop number: 1
Loop number: 2
Loop number: 3
Loop number: 4
```

Notice that Python starts counting at 0.

range(5) produces five repetitions:

```text
0
1
2
3
4
```

---

Why Are Loops Useful?
Without a loop:

```python
print("Checking sensor...")
print("Checking sensor...")
print("Checking sensor...")
print("Checking sensor...")
```

With a loop:

```python
for i in range(4):
    print("Checking sensor...")
```

The second version is shorter and easier to modify.

If we want 20 repetitions, we only need to change:

```python
range(4)
```

to:


```python
range(20)
```
---

Your Turn
Write a loop that prints:

```text
Drone is ready!
```

five times.

Then change your program to print the message ten times.

---


# 13. Creating Reusable Code with Functions

Open:

```text
06_functions.py
```

As programs become larger, we often want to group related instructions together.

A function is a reusable group of instructions.

For example:

```python
def say_hello():
    print("Hello, Drone!")
```

Defining the function does not run it.

We need to call it:

```python
say_hello()
```

We can call it multiple times:

```python
say_hello()
say_hello()
say_hello()
```

---


## Functions with Parameters
Functions can also receive information.

```python
def greet_drone(drone_name):
    print("Hello,", drone_name)

greet_drone("Tello")
greet_drone("Drone 1")
```

The value provided to the function is called an argument.

Functions are especially useful for drone programming because they allow us to organize complicated flight instructions.

For example:

```python
def fly_forward():
    tello.move_forward(100)
```

We can then use:

```python
fly_forward()
```

instead of repeatedly writing the entire command.

---

## Your Turn
Create a function called:

```text
show_mission_complete()
```

The function should print:

```text
Mission complete!
```

Then call the function.

---


# 14. Programming Concepts So Far

Before moving to the Tello, review the four important ideas we have learned.
## Sequence
Instructions normally execute from top to bottom.

```python
print("Takeoff")
print("Move")
print("Land")
```
## Selection
An if statement allows the program to make a decision.
```python
if battery < 20:
    print("Battery too low")
```
## Repetition
A for loop allows the program to repeat instructions.
```python
for i in range(4):
    print("Moving")
```
## Functions
Functions allow us to organize and reuse instructions.
```python
def fly_forward():
    print("Moving forward")
```
These concepts will now become tools for programming a real drone.

---


# 15. Connect to the Tello

Open:

```text
07_tello_connection.py
```

## Before connecting

Make sure:

- The Tello is powered on.
- Your computer is connected to the Tello Wi-Fi network.
- The drone is sitting on a safe, level surface.
- The flight area is clear.
- The battery is sufficiently charged.

Run the program in PyCharm:
* Open 07_tello_connection.py.
* Right-click inside the editor.
* Select Run '07_tello_connection'.

You can also click the green Run ▶ button.

From a terminal, you can run:

```bash
python 07_tello_connection.py
```

The program should connect to the drone and display the battery percentage.

Example:

```text
Connected to Tello!
Battery: 87 %
```

The important programming idea is that the drone can provide information to our Python program.

For example:
```python
battery = tello.get_battery()
```

The drone provides the battery information, and Python stores it in the variable battery.

---

# 16. First Flight: Takeoff and Land

Open:

```text
08_tello_takeoff_land.py
```

This program combines several programming concepts we have already learned.

It will:

1. Connect to the Tello.
2. Check the battery.
3. Use an if statement to decide whether the battery is sufficient.
4. Take off.
5. Wait three seconds.
6. Land.

Run the program from PyCharm:
```text
Right-click → Run '08_tello_takeoff_land'
```

Or use the terminal:

```bash
python 08_tello_takeoff_land.py
```

The basic flight commands are:
```python
tello.takeoff()
```
and:

```python
tello.land()
```

The program can now turn Python instructions into physical drone actions.

---

## Important

Do not modify flight commands until you understand what they do.

Always test flight programs in a safe, open, approved area.

---

# 17. Tello Movement

Open:

```text
09_tello_movement.py
```

You will learn basic movement commands such as:

```python
tello.move_forward(50)
tello.move_back(50)

tello.move_left(50)
tello.move_right(50)

tello.move_up(50)
tello.move_down(50)

tello.rotate_clockwise(90)
tello.rotate_counter_clockwise(90)
```

The numbers represent distances in centimeters or angles in degrees, depending on the command.

For example:

```python
tello.move_forward(100)
```

means:

> Move forward approximately 100 centimeters.

And:

```python
tello.rotate_counter_clockwise(90)
```

means:

> Rotate counter-clockwise approximately 90 degrees.

---

# 18. Programming a Flight Path

Open:

```text
10_tello_flight_path.py
```

Now we will combine everything we have learned to program a simple flight path.

The challenge is:

Can you make the Tello fly a square?

The basic pattern is:


```text

        100 cm
    ┌────────────┐
    │            │
    │            │
100 │            │ 100
 cm │            │ cm
    │            │
    └────────────┘
        100 cm

```

The drone will:
* Take off.
* Move forward 100 cm.
* Rotate 90 degrees.
* Move forward 100 cm.
* Rotate 90 degrees.
* Move forward 100 cm.
* Rotate 90 degrees.
* Move forward 100 cm.
* Rotate 90 degrees.
* Land.

At first, we will write the commands explicitly.

For example:

```python
tello.move_forward(100)
tello.rotate_counter_clockwise(90)

tello.move_forward(100)
tello.rotate_counter_clockwise(90)

tello.move_forward(100)
tello.rotate_counter_clockwise(90)

tello.move_forward(100)
tello.rotate_counter_clockwise(90)
```

### Think About It

Look carefully at the code.

What do you notice?

The same two commands are repeated four times.

This is a good programming problem:

Can we make our code shorter without changing what the drone does?


---

# 19. Improving the Flight Path with a for Loop

Open:

```text
11_tello_flight_path_loop.py
```

We can use the for loop we learned earlier.

Instead of writing:

```python
tello.move_forward(100)
tello.rotate_counter_clockwise(90)

tello.move_forward(100)
tello.rotate_counter_clockwise(90)

tello.move_forward(100)
tello.rotate_counter_clockwise(90)

tello.move_forward(100)
tello.rotate_counter_clockwise(90)
```

we can write:

```python
for i in range(4):
    tello.move_forward(100)
    tello.rotate_counter_clockwise(90)
```

This tells Python:

Repeat these two instructions four times.

The complete flight is now much easier to understand:

```text
Takeoff
   ↓
Repeat 4 times:
   Move forward
   Turn 90°
   ↓
Land
```

This is an important programming idea:

Use computers to automate repetitive work.

---

### Think About It
What would happen if we changed:

```python
range(4)
```

to:

```python
range(6)
```

Would the drone still fly a square?

Before testing it, predict what the drone might do.

Then test your prediction only in a safe and approved flight area.

---

# 20. Flight Path Challenge

Create your own flight path.
* Start with the square example and experiment with:
* Different distances.
* Different angles.
* Different numbers of repetitions.
* Different movement commands.

For example:

```python
for i in range(4):
    tello.move_forward(75)
    tello.rotate_counter_clockwise(90)
```

How is this different from:

```python
for i in range(4):
    tello.move_forward(150)
    tello.rotate_counter_clockwise(90)
```

Think about how the change affects the size of the flight path.

---

# 21. Tello Camera


Open:

```text
12_tello_video.py
```

The Tello is not only a flying robot. It can also provide a live video stream.

This program uses:
* djitellopy to communicate with the drone.
* OpenCV to display the camera image.

Run the program in PyCharm or from the terminal:


```bash
python 12_tello_video.py
```

A window should appear showing the Tello's camera feed.

Press:

```text
Q
```

to close the video window.

---

# 22. From Video to Computer Vision

The basic video program introduces one of the most important ideas in this course:

A drone can use its camera to collect information about the world.

The basic workflow is:

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

Or:

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

# 23. DJITelloPy API Reference

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

As you become more comfortable with programming, use the API documentation to discover additional commands rather than memorizing every command.

---

# 24. Mini-Project: "Hello, Drone!"

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
- Check the battery before flying.
- Change the amount of time the drone remains in the air.
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

# 25. Pair Programming Challenge

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
- Thinks about what the program will do before it runs.

Switch roles halfway through the activity.


---

# 26. Safety Checklist

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

Follow your instructor's classroom flight rules and all applicable local regulations.

---

# 27. Troubleshooting

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

make sure PyCharm is using the correct .venv.

Then install DJITelloPy through either:

### PyCharm

```text
Settings → Project → Python Interpreter → +
```
Search for:

```text
djitellopy
```
and click Install Package.
### Terminal

```bash
pip install djitellopy
```

---

## OpenCV cannot be imported
If you see:

```text
ModuleNotFoundError: No module named 'cv2'
```

install OpenCV.
### PyCharm
Go to:
```text
Settings → Project → Python Interpreter → +
```

Search for:
```text
opencv-python
```

and click Install Package.
### Terminal

```bash
pip install opencv-python
```

Note: The package is installed as opencv-python, but imported in Python as cv2.

---

## PyCharm is using the wrong Python interpreter
If a package appears to be installed but Python cannot find it:
* Open:
  Settings → Project → Python Interpreter
* Check the selected interpreter.
* Make sure it is the project's .venv.
* Install the package into that interpreter.
* Run the program again.

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
- The Tello camera stream has not been left running by another program.

---

# 28. What You Should Know Before Moving On

Before starting the computer-vision projects, you should be comfortable with:

## Python

* Basic Python syntax.
* Variables.
* Strings and numbers.
* Comments.
* if statements.
* for loops.
* Functions.
* Imports.
* Debugging.
* Reading error messages.

## Python Environment

* Installing Python.
* Using PyCharm.
* Running Python programs in PyCharm.
* Using the PyCharm terminal.
* Creating a virtual environment.
* Installing Python packages.
* Understanding which Python interpreter your project is using.

## Tello

* Connecting to the Tello.
* Checking battery level.
* Taking off.
* Landing.
* Moving the drone.
* Rotating the drone.
* Programming a simple flight path.
* Using loops to automate repeated flight commands.

## Computer Vision

* Starting the Tello video stream.
* Receiving video frames.
* Displaying frames with OpenCV.
* Understanding the basic relationship between a camera, images, computer vision, and drone control.

---


# 29. From Programming to AI

You have now built the foundation for the rest of the course.

You started with:

```text
Python
```

Then learned:

```text
Python
   ↓
Sequence
   ↓
Decisions
   ↓
Loops
   ↓
Functions
```


Then applied those concepts to:

```text
Python
   ↓
Tello
   ↓
Flight Commands
   ↓
Flight Paths
```


Then added:


```text
Tello
   ↓
Camera
   ↓
OpenCV
```


The next step is to teach the computer to understand what the camera sees:

```text
Camera
   ↓
Image
   ↓
Computer Vision
   ↓
Detection
   ↓
Decision
   ↓
Drone Action
```

This leads directly to the projects in the main course repository.

---

# 30. Next Steps

After completing this section, continue with the project folders:

- [`Tello_Aruco`](../Tello_Aruco) – ArUco marker tracking
- [`Tello_QRCode`](../Tello_QRCode) – QR code tracking
- [`Tello_GestureCTRL`](../Tello_GestureCTRL) – Gesture-based control
- [`Tello_PoseCTRL`](../Tello_PoseCTRL) – Pose-based control
- [`Tello_YOLO`](../Tello_YOLO) – Object detection with YOLO

The goal is to move from **programming the drone directly** to **programming the drone to perceive and respond to its environment**.

---

# 31. Resources

- Python: https://www.python.org/
- PyCharm: https://www.jetbrains.com/pycharm/download/
- DJITelloPy Documentation: https://djitellopy.readthedocs.io/en/latest/
- DJITelloPy Tello API: https://djitellopy.readthedocs.io/en/latest/tello/
- OpenCV Documentation: https://docs.opencv.org/

---

**IDEAL Fall 2026 – Taking the Plunge: Intro to Drones & AI**
