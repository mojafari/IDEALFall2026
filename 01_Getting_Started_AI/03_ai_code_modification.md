# Activity 03: Ask AI to Modify Existing Code

## Goal

Learn how to ask AI to modify an existing program while controlling what it is allowed to change.

----

## Step 1: Open the Square Flight Program

Open:

[`10_tello_flight_path.py`](../00_Getting_Started/10_tello_flight_path.py)


Before using AI, understand the program.

The drone is programmed to fly a square.

Think about:

* How many sides does the square have?
* How many forward movements are there?
* How many rotations are there?
* What is the rotation angle?
* What is the movement distance?

----

## Step 2: Ask AI to Explain It

Use:

````text
I am learning Python and drone programming.

Here is my Tello program:

[PASTE CODE HERE]

Explain how this program creates a square flight path.

Do not modify the code.

Explain:

1. How many times the drone moves.
2. How many times it rotates.
3. Why the drone rotates by the angle used in the program.
4. How the program returns to its starting direction.
````

----

## Step 3: Modify the Program

Now give AI a controlled task:

````text
I am learning Python and drone programming.

Here is a Tello program that currently flies a square:

[PASTE CODE HERE]

Modify it so that the drone flies a triangle.

Requirements:

- Keep the Tello connection code.
- Keep takeoff.
- Keep landing.
- Keep the movement distance at 100 cm.
- Change only what is necessary to create a triangle.
- Explain every change you make.
- Do not introduce advanced Python concepts.
````

----

## Step 4: Inspect the Result

Do not immediately run the code.

Check:

* Did the AI change the connection code?
* Did it change the takeoff code?
* Did it change the landing code?
* Is the number of sides correct?
* Is the movement distance correct?
* Is the turn angle correct?
* Did it add unnecessary code?


----

## Step 5: Ask AI to Explain Its Changes

Use:

````text
Explain only the changes you made from the original program.

For every change:

1. Show the original code.
2. Show the new code.
3. Explain why the change was necessary.

Do not make any additional changes.
````

----

## Human Verification

Before testing the program, answer:

````text
How many sides should the drone fly?

Answer: __________

How many forward movements should there be?

Answer: __________

What should the turn angle be?

Answer: __________
````

If you cannot answer these questions, you do not yet understand the program well enough to run it.

----

## Key Idea

AI can modify code very quickly.

Your job is to make sure the modification is actually what you intended.

