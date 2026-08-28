"""
IDEAL Fall 2026 - Introduction to Programming
06_functions.py

Learning Objectives:
- Understand what a function is.
- Create a function.
- Call a function.
- Understand why functions help us avoid repeated code.

Key Idea:
A function is a reusable group of instructions.

Instead of writing the same instructions again and again,
we can put them inside a function and call the function
whenever we need it.
"""

# ---------------------------------------------------------
# Example 1: A simple function
# ---------------------------------------------------------

def say_hello():
    print("Hello, Drone!")


# Defining a function does not run it.
#
# We need to CALL the function:

say_hello()


# ---------------------------------------------------------
# Example 2: Calling a function multiple times
# ---------------------------------------------------------

say_hello()
say_hello()
say_hello()


# ---------------------------------------------------------
# Example 3: A function with a parameter
# ---------------------------------------------------------

def greet_drone(drone_name):
    print("Hello,", drone_name)


greet_drone("Tello")
greet_drone("Drone 1")


# The value inside the parentheses is called an argument.
#
# greet_drone("Tello")
#              ↓
#          drone_name


# ---------------------------------------------------------
# Example 4: A function for a repeated task
# ---------------------------------------------------------

def show_mission_start():
    print("-------------------------")
    print("Starting drone mission")
    print("-------------------------")


show_mission_start()


# ---------------------------------------------------------
# YOUR TURN
# ---------------------------------------------------------

# Create a function called:
#
# show_mission_complete()
#
# It should print:
#
# "Mission complete!"
#
# Then call your function.

# Write your code below:


# ---------------------------------------------------------
# DRONE CONNECTION
# ---------------------------------------------------------

# Functions become especially useful when controlling a drone.
#
# For example, later we could create:
#
# def fly_forward():
#     tello.move_forward(100)
#
# Then instead of writing:
#
# tello.move_forward(100)
#
# every time, we can write:
#
# fly_forward()
