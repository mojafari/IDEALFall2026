# Activity 04: Square → Triangle

## Goal

Use AI to transform an existing drone flight path.

This activity combines:

* geometry
* Python
* loops
* drone control
* prompting
* AI evaluation

----

## Step 1: Think Before Asking AI

Your current program flies a square.

A square has:

````text
4 sides
````

A triangle has:

````text
3 sides
````

Before asking AI, determine:

````text
Triangle sides = ______

Movement distance = ______

Turn angle = ______
````

----

## Step 2: Explain Your Reasoning

Write:

````text
I think the drone should turn ______ degrees because:

[YOUR EXPLANATION]
````

Do not ask AI yet.

----

## Step 3: Ask AI to Check Your Reasoning

Use:

````text
I am learning Python and drone programming.

I have a Tello program that flies a square.

I want to change it into a triangle.

My reasoning is:

[PASTE YOUR REASONING HERE]

Check my reasoning.

Do not modify my code yet.

Tell me:

1. Whether my reasoning is correct.
2. If it is incorrect, explain what I misunderstood.
3. What the correct turn angle should be.
4. Why that angle is correct.

Use beginner-friendly language.
````

----

## Step 4: Modify the Code

Once you understand the geometry, ask:

````text
Now modify my original program.

Requirements:

- Create a three-sided flight path.
- Use 100 cm for each side.
- Use the correct turn angle.
- Keep the existing Tello connection.
- Keep takeoff.
- Keep landing.
- Do not introduce advanced concepts.

Show the modified code.

Then explain every change.
````

----

## Step 5: Use a Loop

Now ask AI:

````text
Rewrite my triangle flight path using a Python for loop.

Requirements:

- 3 sides
- 100 cm per side
- correct turn angle
- takeoff
- landing

Explain the for loop as if I have only recently learned loops.
````

----

## Step 6: Compare the Programs

Compare:

````text
Original Square Program
````

with:

````text
Triangle Program Without a Loop
````

and:

````text
Triangle Program With a Loop
````

Answer:

1. Which program is easiest to understand?
2. Which program is shortest?
3. Which program is easiest to change?
4. What would happen if you wanted a pentagon?
5. What would happen if you wanted a hexagon?

----

## Challenge

Ask AI:

````text
Can this program be generalized so that I can specify the number of sides and the side length?

Explain the idea before writing code.
````

Do not immediately accept the generated program.

Try to understand the idea first.

----

## Optional Extension

Ask AI:

````text
If I give you the number of sides of a regular polygon, how can we calculate the turn angle?

Explain the geometry without assuming I know advanced mathematics.
````

----


## Reflection

Complete:

````text
The most useful thing AI did was:

________________________________________

The most important thing I had to verify was:

________________________________________

One thing I understand better now is:

________________________________________
````
