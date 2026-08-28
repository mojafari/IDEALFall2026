"""
IDEAL Fall 2026 - Tello Programming
09_tello_movement.py

Learning Objectives:
- Use basic Tello movement commands.
- Understand distance and angle parameters.
- Create a sequence of flight commands.

Today we will program:
    Takeoff
       ↓
    Forward
       ↓
    Turn
       ↓
    Forward
       ↓
    Land
"""

from djitellopy import Tello
import time


# Create the Tello object
tello = Tello()

# Connect to the drone
tello.connect()

# Check the battery
print("Battery:", tello.get_battery(), "%")


# ---------------------------------------------------------
# Takeoff
# ---------------------------------------------------------

tello.takeoff()

time.sleep(2)


# ---------------------------------------------------------
# Move forward
# ---------------------------------------------------------

# The number represents approximately centimeters.
#
# 100 = approximately 100 cm = 1 meter

tello.move_forward(100)

time.sleep(1)


# ---------------------------------------------------------
# Rotate
# ---------------------------------------------------------

# Rotate 90 degrees counter-clockwise.

tello.rotate_counter_clockwise(90)

time.sleep(1)


# ---------------------------------------------------------
# Move forward again
# ---------------------------------------------------------

tello.move_forward(100)

time.sleep(1)


# ---------------------------------------------------------
# Land
# ---------------------------------------------------------

tello.land()

print("Flight complete!")
