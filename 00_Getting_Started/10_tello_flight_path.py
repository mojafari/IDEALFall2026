"""
IDEAL Fall 2026 - Tello Flight Path
10_tello_flight_path.py

Learning Objectives:
- Combine multiple drone commands.
- Understand a sequence of movement commands.
- Program the Tello to fly a square.

Challenge:
Can you make the drone fly a square?

Flight pattern:

        100 cm
    ┌────────────┐
    │            │
    │            │
100 │            │ 100
 cm │            │ cm
    │            │
    └────────────┘
        100 cm

The drone will:
1. Take off.
2. Move forward 100 cm.
3. Rotate 90 degrees.
4. Repeat the pattern.
5. Land.
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
# SIDE 1
# ---------------------------------------------------------

tello.move_forward(100)
tello.rotate_counter_clockwise(90)

time.sleep(1)


# ---------------------------------------------------------
# SIDE 2
# ---------------------------------------------------------

tello.move_forward(100)
tello.rotate_counter_clockwise(90)

time.sleep(1)


# ---------------------------------------------------------
# SIDE 3
# ---------------------------------------------------------

tello.move_forward(100)
tello.rotate_counter_clockwise(90)

time.sleep(1)


# ---------------------------------------------------------
# SIDE 4
# ---------------------------------------------------------

tello.move_forward(100)
tello.rotate_counter_clockwise(90)

time.sleep(1)


# ---------------------------------------------------------
# Land
# ---------------------------------------------------------

tello.land()

print("Square flight complete!")
