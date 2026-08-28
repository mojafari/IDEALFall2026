"""
IDEAL Fall 2026 - Tello Flight Path with a FOR Loop
11_tello_flight_path_loop.py

Learning Objectives:
- Use a for loop with a physical drone.
- Replace repeated code with a loop.
- Understand how programming concepts can make drone
  programs shorter and easier to modify.

Previous version:

    move_forward()
    rotate()

    move_forward()
    rotate()

    move_forward()
    rotate()

    move_forward()
    rotate()

We can improve this using a FOR loop.
"""

from djitellopy import Tello
import time


# ---------------------------------------------------------
# Connect to the Tello
# ---------------------------------------------------------

tello = Tello()
tello.connect()

print("Battery:", tello.get_battery(), "%")


# ---------------------------------------------------------
# Takeoff
# ---------------------------------------------------------

tello.takeoff()

time.sleep(2)


# ---------------------------------------------------------
# Fly a square using a FOR loop
# ---------------------------------------------------------

# We want to repeat the same two instructions four times:
#
#     1. Move forward 100 cm
#     2. Rotate 90 degrees
#
# range(4) tells Python to repeat the code four times.

for i in range(4):

    # Fly one side of the square
    tello.move_forward(100)

    # Turn for the next side
    tello.rotate_counter_clockwise(90)

    # Pause briefly between movements
    time.sleep(1)


# ---------------------------------------------------------
# Land
# ---------------------------------------------------------

tello.land()

print("Square flight complete!")


# ---------------------------------------------------------
# THINK ABOUT IT
# ---------------------------------------------------------

# What would happen if we changed:
#
#     range(4)
#
# to:
#
#     range(6)
#
# Would the drone still fly a square?
#
# What shape might it create?
#
# Try to predict the result BEFORE testing it.
