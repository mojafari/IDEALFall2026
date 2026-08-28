"""
IDEAL Fall 2026 - Introduction to Programming
04_if_statements.py

Learning Objectives:
- Understand what an if statement does.
- Make a decision based on a condition.
- Understand comparison operators.
- Use if / else to create two possible outcomes.

Key Idea:
An if statement allows a program to make a decision.

Example:

    IF the battery is low
        → tell the user to charge the drone

    ELSE
        → tell the user the drone is ready
"""

# ---------------------------------------------------------
# Example 1: A simple decision
# ---------------------------------------------------------

battery = 80

if battery < 20:
    print("Battery is low!")

# Python checks:
#
# Is battery less than 20?
#
# If the answer is TRUE, the indented code runs.
# If the answer is FALSE, Python skips it.


# ---------------------------------------------------------
# Example 2: if + else
# ---------------------------------------------------------

battery = 80

if battery < 20:
    print("Battery is too low for flight.")
else:
    print("Battery level is OK.")


# There are now two possible outcomes:
#
# battery < 20
#       ↓
# "Battery is too low for flight."
#
# battery >= 20
#       ↓
# "Battery level is OK."


# ---------------------------------------------------------
# Example 3: Change the value
# ---------------------------------------------------------

battery = 15

if battery < 20:
    print("Battery is too low for flight.")
else:
    print("Ready for flight!")


# Try changing battery to:
#
# 10
# 25
# 50
# 100
#
# Run the program after each change.
#
# What happens?


# ---------------------------------------------------------
# Example 4: More than one condition
# ---------------------------------------------------------

height = 100

if height > 120:
    print("The drone is flying high.")
else:
    print("The drone is flying at a lower altitude.")


# ---------------------------------------------------------
# YOUR TURN
# ---------------------------------------------------------

# Create a variable called speed.
#
# If speed is greater than 50:
#     print("The drone is moving fast.")
#
# Otherwise:
#     print("The drone is moving slowly.")

# Write your code below:


# ---------------------------------------------------------
# DRONE CONNECTION
# ---------------------------------------------------------

# Later, we can use the same idea with a real Tello:
#
# battery = tello.get_battery()
#
# if battery < 20:
#     print("Do not fly!")
# else:
#     print("Ready for flight!")
#
# The important idea is that the program can:
#
#     GET INFORMATION
#          ↓
#     MAKE A DECISION
#          ↓
#     TAKE AN ACTION
