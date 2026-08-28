"""
IDEAL Fall 2026 - Introduction to Programming
03_how_code_executes.py

Learning Objectives:
- Understand that Python normally executes code from top to bottom.
- Understand what happens when a program reaches each line.
- Learn to predict program output before running the code.
- Understand that some programming structures can change the normal flow.

Key Idea:
A computer does not "understand" the whole program at once.
It follows instructions one step at a time.
"""

# ---------------------------------------------------------
# Example 1: Code executes from top to bottom
# ---------------------------------------------------------

print("Step 1")

print("Step 2")

print("Step 3")


# When you run this program, Python executes:
#
# print("Step 1")
#       ↓
# print("Step 2")
#       ↓
# print("Step 3")
#
# The output is:
#
# Step 1
# Step 2
# Step 3


# ---------------------------------------------------------
# Example 2: Variables are also processed step by step
# ---------------------------------------------------------

drone_name = "Tello"

print("The drone is:", drone_name)

battery = 85

print("Battery:", battery, "%")


# Python first creates drone_name.
# Then it prints drone_name.
# Then it creates battery.
# Then it prints battery.


# ---------------------------------------------------------
# Example 3: Predict the output
# ---------------------------------------------------------

print("Taking off")

height = 50

print("Height:", height)

print("Moving forward")

print("Landing")


# BEFORE running the program:
# Write down what you think the output will be.
#
# Then run the program and compare your answer.


# ---------------------------------------------------------
# YOUR TURN
# ---------------------------------------------------------

# Create a simple five-step drone mission.
#
# For example:
#
# Step 1: Print a message that the mission is starting.
# Step 2: Create a variable for the drone's speed.
# Step 3: Print the speed.
# Step 4: Print a message that the drone is moving.
# Step 5: Print a message that the mission is complete.

# Write your code below:
