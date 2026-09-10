# Activity 01: Ask AI to Explain Your Code

## Goal

Use an AI assistant to help you understand a Python program that you have already written.

We are starting with explanation rather than code generation.

----

## Step 1: Open an Existing Program

Open:

````text
00_Getting_Started/09_tello_movement.py
````

Look at the program before using AI.

Do not ask AI anything yet.

Try to answer:

1. How does the program connect to the drone?
2. How does the drone take off?
3. How does the drone move?
4. How does the drone rotate?
5. How does the drone land?

Write down your answers.

----

## Step 2: Ask AI to Explain One Line

Open ChatGPT.

Use the following prompt:


````text
I am a first-year college student learning Python and drone programming.

Explain this line of Python code to a beginner:

tello.move_forward(100)

Explain:

1. What "tello" represents.
2. What "move_forward" represents.
3. What the number 100 represents.
4. What happens when the program executes this line.

Use simple language.

Do not assume that I have advanced programming knowledge.
````

----

## Step 3: Compare the Answer With Your Understanding

Ask yourself:
* Did the AI explanation match what you learned?
* Did it introduce a word you don't understand?
* Did it make any assumptions?
* Did it say anything that seems incorrect?

If you do not understand something, ask a follow-up question.

For example:

````text
You used the word "method".

What does "method" mean?

Explain it using a simple example involving the Tello drone.
````

----

## Step 4: Ask AI to Explain the Whole Program

Copy the contents of:

````text
09_tello_movement.py
````

into ChatGPT.

Use:

````text
I am a first-year college student learning Python and drone programming.

Here is my Tello drone Python program:

[PASTE CODE HERE]

Explain this program step by step.

For each important line or group of lines, explain:

1. What the code does.
2. Why it is needed.
3. What happens to the drone.
4. What Python concept is being used.

Assume I am a beginner.

Do not rewrite or modify the program.

I only want an explanation.
````

----

## Step 5: Ask AI to Explain the Program as a Flight Sequence

Now ask:

````text
Explain this program as if you were describing what a person would see while watching the drone.

Describe:

1. What happens first.
2. What happens next.
3. How the drone moves.
4. How the drone rotates.
5. How the flight ends.

Then connect each physical action to the Python command that causes it.
````

----

## Step 6: Check the AI

Do not assume the AI is correct.

Complete this table:


| Code | My Understanding | AI's Explanation | Agree? |
| -------- | -------- | -------- | -------- |
| tello.connect()   |    |    |    |
| tello.takeoff()   |    |    |    |
| tello.move_forward(100)   |    |    |    |
| tello.rotate_counter_clockwise(90)   |    |    |    |
| tello.land()   |    |    |    |

----

## Reflection

Answer:

1. What did AI explain well?
2. What did AI explain poorly?
3. Did AI use any terminology that you did not know?
4. Did you find an error in the AI's explanation?
5. What follow-up question did you ask?

----

## Key Idea

The first use of AI in this course is not:

````text
"Write my program."
````

It is:

````text
"Help me understand my program."
````

That distinction is important.




