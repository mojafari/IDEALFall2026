"""
IDEAL Fall 2026 - Tello Programming
08_tello_takeoff_land.py

Learning Objectives:
- Send commands to a physical drone.
- Understand how Python statements can cause physical actions.
- Use time.sleep() to pause a program.

SAFETY:
- Fly only in an approved area.
- Make sure the flight area is clear.
- Keep people away from the drone.
- Review the program before running it.
"""

from djitellopy import Tello
import time


# ---------------------------------------------------------
# Step 1: Create and connect to the Tello
# ---------------------------------------------------------

tello = Tello()
tello.connect()


# ---------------------------------------------------------
# Step 2: Check the battery
# ---------------------------------------------------------

battery = tello.get_battery()

print("Battery:", battery, "%")


# ---------------------------------------------------------
# Step 3: Use an IF statement
# ---------------------------------------------------------

# We learned about if statements before we introduced
# the drone.
#
# Now we can use that knowledge to make the drone program
# make a decision.

if battery < 20:

    print("Battery is too low for flight.")
    print("Please charge the drone.")

else:

    print("Battery level is OK.")
    print("Ready for takeoff!")

    # -----------------------------------------------------
    # Step 4: Take off
    # -----------------------------------------------------

    tello.takeoff()

    # -----------------------------------------------------
    # Step 5: Wait
    # -----------------------------------------------------

    time.sleep(3)

    # -----------------------------------------------------
    # Step 6: Land
    # -----------------------------------------------------

    tello.land()

    print("Flight complete!")
