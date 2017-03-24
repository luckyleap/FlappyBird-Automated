# Instructions
Please install python3 and pygame to run this game!
```
cd timowilken
python3 flappybird.py
```
## Game
This game is a clone of timowilken's flappybird in python, modified to automatically play itself using Q-reinforcement learning
## States
The project is setup with the states represented by 3 factors: the distance of the bird horizontally (x), vertically (y) away from the center of the pipe, and the vertical quadrant of the bird itself (defined discretely {0, 1, 2, 3}).

The horizontal distance is the absolute value of the difference between bird.x and pipe.x.
The vertical distance is the absolute value of the difference between bird.y and pipe.middl_y.
The quadrant is 4 possible values {0, 1, 2, 3} representing the y value of the bird in 4 different heights.

I have also tried using just the horizontal distance and vertical distance without the quadrants.
Finally, I have also tried using the bird.y, horizontal distance, and vertical distance.

## Exploration Approaches
The exploration approach is simply a chance of 60% with the average visits / 20 added on it.
I have tried tweaking different percentage, from 50% to 75% to 85%.

## Learning Rate
I made the learning rate inversely proportional to the number of visits in the state. This allows for high learning rate when the states have not been visited much and low learning rate when the state has already been visited.

## Training
The training took me 2 days. If I had more time, I would increase the number of state features as this would make the policy more accurate.
