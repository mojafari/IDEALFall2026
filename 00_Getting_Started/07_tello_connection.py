"""
IDEAL Fall 2026 - Tello Programming
07_tello_connection.py

Learning Objectives:
- Import the DJITelloPy library.
- Create a Tello object.
- Connect to the drone.
- Read information from the drone.

Before running:
1. Turn on the Tello.
2. Connect your computer to the Tello Wi-Fi network.
3. Make sure the drone is on a safe, level surface.
"""

# Import the Tello class from DJITelloPy.
from djitellopy import Tello


# ---------------------------------------------------------
# Step 1: Create a Tello object
# ---------------------------------------------------------

tello = Tello()


# ---------------------------------------------------------
# Step 2: Connect to the drone
# ---------------------------------------------------------

tello.connect()


# ---------------------------------------------------------
# Step 3: Ask the drone for information
# ---------------------------------------------------------

battery = tello.get_battery()


# ---------------------------------------------------------
# Step 4: Display the information
# ---------------------------------------------------------

print("Connected to Tello!")
print("Battery:", battery, "%")


# ---------------------------------------------------------
# IMPORTANT PROGRAMMING IDEA
# ---------------------------------------------------------

# Notice what happened:
#
# 1. We created an object.
# 2. We called a function/method.
# 3. The drone returned information.
# 4. We stored that information in a variable.
# 5. We printed the variable.
#
# This is the same programming process we practiced
# before introducing the drone.
