# Activity 05: AI-Assisted Debugging

## Goal

Learn how to use AI to understand programming errors.

AI should not simply give you a replacement program.

It should help you understand the problem.

----

## Step 1: Introduce an Error

Take a working Python program.

Change:

````python
tello.move_forward(100)
````

to:

````python
tello.move_forward("100")
````

Run the program or inspect the resulting error.

----

## Step 2: Ask AI

Use:

````text
I am learning Python and drone programming.

I changed my code and now I have an error.

Here is the relevant code:

tello.move_forward("100")

Explain:

1. What is wrong?
2. Why is it wrong?
3. What type of Python concept does this demonstrate?
4. How could I fix it?

Do not just give me the corrected line.

Teach me how to recognize this type of problem myself.
````

----

## Step 3: Give AI the Actual Error

A better debugging prompt includes the actual error message.

Use:

````text
I am learning Python and drone programming.

I expected the drone to move forward 100 cm.

Instead, I received this error:

[PASTE EXACT ERROR HERE]

Here is the relevant code:

[PASTE CODE HERE]

Please:

1. Explain what the error means.
2. Identify the most likely cause.
3. Explain how I can fix it.
4. Explain how I could recognize this problem in the future.

Do not rewrite the entire program.
````

----

## The Debugging Process

A good debugging process is:

````text
Run Program
    ↓
Observe Problem
    ↓
Read Error
    ↓
Identify Relevant Code
    ↓
Form a Hypothesis
    ↓
Ask AI
    ↓
Evaluate AI's Explanation
    ↓
Make One Change
    ↓
Run Again
````

----

## Debugging Challenge

Create another error in your program.

Possible examples:

* Misspell a variable.
* Remove a quotation mark.
* Remove a parenthesis.
* Change capitalization.
* Change a number to a string.
* Change indentation.

Try to diagnose the error yourself first.

Then ask AI to check your reasoning.

----

## Reflection

Answer:
1. Did AI correctly identify your error?
2. Did it explain the cause?
3. Did it suggest unnecessary changes?
4. Did you understand the fix?
5. Could you fix a similar error without AI next time?

----

## Key Idea

The goal of AI-assisted debugging is not:

````text
AI fixes my code.
````

The goal is:

````text
AI helps me understand why my code is broken.
````
