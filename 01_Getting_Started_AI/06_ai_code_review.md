# Activity 06: Ask AI to Review Your Code

## Goal

Learn how to use AI as a code reviewer.

This is different from asking AI to rewrite your program.

----

## Step 1: Use Your Triangle Program

Use your completed triangle program from:


[04_square_to_triangle.md](./04_square_to_triangle.md)


----

## Step 2: Ask AI to Review It

Use:

````text
I am learning Python and drone programming.

Here is my program:

[PASTE CODE HERE]

Review my program.

Do not rewrite the program.

Instead:

1. Identify possible programming errors.
2. Identify possible logic errors.
3. Identify anything that may not behave as I expect.
4. Identify anything that could be unsafe for a physical drone.
5. Identify unnecessary complexity.
6. Suggest what I should test.

Explain your reasoning.
````

----

## Step 3: Evaluate the Review

Create this table:

| AI Suggestion | Do I Agree? | How Can I Verify It?|
|---------------|-------------|---------------------|
|               |             |                     |
|               |             |                     |
|               |             |                     |
|               |             |                     |
|               |             |                     |


The purpose is to make you evaluate AI suggestions instead of accepting them automatically.

----

## AI Hallucinations

AI systems can generate information that sounds convincing but is incorrect.

For example, an AI might invent a function:

````python
tello.fly_in_circle(100)
````

You must check whether that function actually exists.

Never assume that an AI-generated function or library exists.

----

## Verification Sources

When possible, verify programming information using:
* Existing course examples.
* Python documentation.
* Library documentation.
* Working programs.
* Error messages.
* Experiments.

----

## Physical Systems Require Extra Care

A wrong answer in a text program might cause an error.

A wrong answer in a drone program might cause the drone to move unexpectedly.

Therefore:

AI-generated physical-control code must be reviewed carefully before execution.

----

## Reflection

Answer:
1. Did AI identify a real issue?
2. Did AI identify anything that was not actually a problem?
3. How did you determine whether AI was correct?
4. What would happen if you blindly trusted the review?


