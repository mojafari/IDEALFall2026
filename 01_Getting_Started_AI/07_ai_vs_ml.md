# Activity 07: AI, Machine Learning, and Generative AI

## Why Are We Talking About This?

So far, you have been using AI to:
* explain code
* generate code
* modify code
* debug code
* review code

But what exactly is AI?

And is what we are doing the same thing as machine learning?

Not exactly.

----

## Artificial Intelligence

Artificial Intelligence is a broad field concerned with creating systems that perform tasks that we associate with intelligence.

Examples include:

* understanding language
* recognizing images
* planning
* making predictions
* recognizing speech
* controlling robots
* generating content

----

## Machine Learning


Machine learning is one approach to creating AI systems.

A simplified traditional programming model is:

````text
Rules + Data
     ↓
  Program
     ↓
  Answer
````

A simplified machine-learning model is:

````text
Examples
    ↓
Learning Algorithm
    ↓
Trained Model
    ↓
New Data
    ↓
Prediction
````

----

## Example: Object Recognition

Imagine a drone camera.

We want the drone to recognize:

````text
Person
Car
Tree
Building
````

We can provide many example images:

````text
Image → Person
Image → Person
Image → Car
Image → Tree
Image → Building
...
````

A machine-learning system learns patterns from these examples.

Later:

````text
New Image
    ↓
ML Model
    ↓
Prediction: Person
````

----

## Generative AI

ChatGPT is an example of generative AI.

Generative AI can produce new content such as:

* text
* code
* images
* audio
* other forms of content

When you ask:

````text
Explain this Python program.
````

the AI generates a response.

When you ask:

````text
Modify this program.
````

the AI generates code.


----

## A Simplified Relationship

Think about the relationship like this:


````text
Artificial Intelligence
│
├── Machine Learning
│   │
│   ├── Supervised Learning
│   ├── Unsupervised Learning
│   └── Reinforcement Learning
│
└── Generative AI
    │
    ├── Text Generation
    ├── Code Generation
    ├── Image Generation
    └── Other Generation
````

This is a simplified conceptual diagram.

The boundaries between these technologies can be more complicated in real systems.

----

## Why Does This Matter for Drones?

A drone has sensors.

For example:

````text
Camera
Battery sensor
Altitude sensor
Motion sensors
GPS
````


The drone can collect information.

AI and machine learning can help interpret that information.

For example:

````text
Camera
   ↓
Image
   ↓
Computer Vision
   ↓
Machine Learning
   ↓
Object Detected
   ↓
Decision
   ↓
Drone Action
````

----

## Example

Imagine:

````text
Drone Camera
     ↓
Image
     ↓
AI detects a person
     ↓
Where is the person?
     ↓
Calculate position
     ↓
Drone moves
````

Now we are moving from:

````text
AI helps me write drone code
````

toward:


````text
AI becomes part of the drone system
````

----

## Reflection

Answer:
1. What is artificial intelligence?
2. What is machine learning?
3. What is generative AI?
4. Is every AI system machine learning?
5. How could machine learning be useful for a drone?
6. What information could a drone camera provide to an AI system?


