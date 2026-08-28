"""
IDEAL Fall 2026 - Introduction to Programming
05_for_loops.py

Learning Objectives:
- Understand why loops are useful.
- Use a for loop to repeat code.
- Understand range().
- Replace repetitive code with a loop.

Key Idea:
Computers are very good at repeating instructions.

Instead of writing the same code many times,
we can tell Python:

    "Repeat this for me."
"""

# ---------------------------------------------------------
# Example 1: Repeating code WITHOUT a loop
# ---------------------------------------------------------

print("Hello")
print("Hello")
print("Hello")
print("Hello")
print("Hello")


# This works, but it is repetitive.
#
# What if we wanted to print "Hello" 100 times?
#
# We would NOT want to write 100 print statements!


# ---------------------------------------------------------
# Example 2: Using a for loop
# ---------------------------------------------------------

for i in range(5):
    print("Hello")


# range(5) tells Python to repeat the code 5 times.
#
# The indented code belongs to the loop.
#
# The variable i keeps track of the repetition.


# ---------------------------------------------------------
# Example 3: See the loop counter
# ---------------------------------------------------------

for i in range(5):
    print("Loop number:", i)


# Notice that counting starts at 0:
#
# Loop number: 0
# Loop number: 1
# Loop number: 2
# Loop number: 3
# Loop number: 4
#
# That is five repetitions.


# ---------------------------------------------------------
# Example 4: A simple countdown
# ---------------------------------------------------------

for number in range(5, 0, -1):
    print(number)

print("Takeoff!")


# range(5, 0, -1) means:
#
# Start at 5
# Stop before 0
# Count backwards by 1


# ---------------------------------------------------------
# Example 5: Why loops are useful
# ---------------------------------------------------------

# WITHOUT a loop:

print("Checking sensor...")
print("Checking sensor...")
print("Checking sensor...")
print("Checking sensor...")


# WITH a loop:

for i in range(4):
    print("Checking sensor...")


# Both programs do approximately the same thing,
# but the second program is shorter and easier to change.


# ---------------------------------------------------------
# YOUR TURN
# ---------------------------------------------------------

# Write a loop that prints:
#
# "Drone is ready!"
#
# five times.

# Write your code below:


# ---------------------------------------------------------
# CHALLENGE
# ---------------------------------------------------------

# Write a loop that prints:
#
# "Moving..."
#
# 10 times.

# How would you change your code to print it 20 times?
