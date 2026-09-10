# Getting Started with AI: Python, Prompting, and Drones

Welcome to the AI portion of IDEAL Fall 2026!

In the previous section, [`00_Getting_Started`](../00_Getting_Started) , you learned how to:

* Write basic Python programs.
* Use variables, conditions, loops, and functions.
* Connect Python to a DJI Tello drone.
* Send movement commands to the drone.
* Program a simple flight path.
* Use loops to simplify drone programs.
* Access the Tello camera and video stream.

Now we are going to introduce Artificial Intelligence.

However, we are not going to begin with complicated mathematics or neural networks.

Instead, we will begin with something you can use immediately:

AI as a programming assistant.

You will use an AI assistant such as ChatGPT to:
* Explain Python code.
* Explain drone-control code.
* Answer questions about programming concepts.
* Modify existing programs.
* Help debug programs.
* Review programs.
* Suggest improvements.
* Challenge your reasoning.
* Help you learn new concepts.

The goal is not to have AI do your programming for you.

The goal is to learn how to work with AI while remaining responsible for understanding, testing, and verifying your programs.


---

## Learning Objectives

By the end of this section, you should be able to:
* Explain what a prompt is.
* Write a useful prompt for an AI assistant.
* Ask an AI system to explain existing Python code.
* Ask an AI system to modify an existing program.
* Ask an AI system to help debug code.
* Evaluate whether an AI-generated answer makes sense.
* Identify possible errors in AI-generated code.
* Explain why AI-generated code should not be blindly trusted.
* Use AI to check your own reasoning.
* Explain the difference between AI, machine learning, and generative AI.
* Describe how AI could eventually be used inside an autonomous drone system.

---

## Important Rule

### AI is a tool, not a replacement for thinking.

Throughout this section, use the following workflow:

```text
Think
  ↓
Ask AI
  ↓
Read
  ↓
Question
  ↓
Verify
  ↓
Test
  ↓
Learn
```

Do not use this workflow:


```text
Ask AI
  ↓
Copy
  ↓
Run
  ↓
Hope
```

---

## Course Connection

This section builds directly on the programs in:


[`00_Getting_Started`](../00_Getting_Started) 


In particular, we will use:

[`09_tello_movement.py`](../00_Getting_Started/09_tello_movement.py) 

[`10_tello_flight_path.py`](../00_Getting_Started/10_tello_flight_path.py) 

[`11_tello_flight_path_loop.py`](../00_Getting_Started/11_tello_flight_path_loop.py) 

[`12_tello_video.py`](../00_Getting_Started/12_tello_video.py) 


as starting points for our AI activities.

---

## Module Progression


```text
Python + Drone Programming
          ↓
AI Explains My Code
          ↓
Writing Better Prompts
          ↓
AI Modifies My Code
          ↓
Square → Triangle
          ↓
AI Debugging
          ↓
AI Code Review
          ↓
AI vs. Machine Learning
          ↓
AI + Computer Vision
          ↓
AI-Powered Drone
```

---

## Activities

### 01 - AI Code Explanation

Learn how to ask AI to explain a program you already understand.

See:

```text
01_ai_code_explanation.md
```

---

### 02 - Prompting Basics

Learn what makes a prompt useful.

See:

```text
02_prompting_basics.md
```

---

### 03 - AI Code Modification

Learn how to ask AI to make a controlled change to an existing program.

See:

```text
03_ai_code_modification.md
```

---

### 04 - Square to Triangle

Use AI to help transform a drone flight path from a square into a triangle.

See:

```text
04_square_to_triangle.md
```

---

### 05 - AI Debugging

Learn how to use AI to help understand Python errors.

See:

```text
05_ai_debugging.md
```

---

### 06 - AI Code Review

Learn how to ask AI to review code without simply rewriting it.

See:

```text
06_ai_code_review.md
```

---


### 07 - AI vs. Machine Learning

Learn the difference between:

```text
Artificial Intelligence
Machine Learning
Generative AI
Large Language Models
```

See:

```text
07_ai_vs_ml.md
```

---

### 08 - AI Drone Challenge

Combine prompting, programming, and drone concepts in a small project.

See:

```text
08_ai_drone_challenge.md
```

---

## Safety

AI-generated code can control physical hardware.

That means we must be more careful than when generating a simple text program.

Before running AI-generated drone code:

* Read the entire program.
* Understand the movement commands.
* Check all movement distances.
* Check all rotation angles.
* Check all loops.
* Check the takeoff command.
* Check the landing command.
* Check the flight area.
* Check the drone battery.
* Test conservatively.
* Be prepared to stop the program.

Never blindly execute AI-generated code that controls a physical drone.

The AI does not know what is physically around your drone.

You do.

---

## The Big Idea

AI can help you write code.

But the more important skill is learning how to think with AI.

A strong programmer can ask:

"Is this answer correct?"

A stronger programmer can ask:

"How do I verify that this answer is correct?"

An AI-enabled engineer should be able to do both.


---

## Looking Ahead

Eventually, we will move from:

```text
Human → AI → Code
```

to:

```text
Drone Camera
      ↓
Computer Vision
      ↓
Machine Learning
      ↓
Prediction
      ↓
Decision
      ↓
Drone Action
```

---

This section is the first step toward that goal.

