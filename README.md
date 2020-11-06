# Software_Fund_Repo
Repository is solely for the use of uploading project assignments
## Table of Contents
* [General info](#general-info)
* [Technologies](#technologies)
* [What does the code do?](#what-does-the-code-do)
* [How to use it](#how-to-use-it)
* [Setup](#setup)
* [Suggested improvements for the future](#suggested-improvements-for-the-future)
* [References user](#references-used)

## General info

This readme file is part of the C1 Practical Project Report.
For this project, i am tasked with creating a game, either one of my own or an existing game, using the pygame libraries. 
The game that i have decided to create for this project is an existing game, Connect4.
The basis of the game is to try and get four of your own counters in a row to win the game.

## Technologies

This project, Connect4, uses the following technologies:
* Python version: 3.7.6 (or higher)
* Spyder version: 4.0 (or higher)
* Microsoft Windows 10 x64 bit (or higher)
* Pygames & relevant modules enabled via PATH

## What does the code do?

A brief description of the code and what it does is simply a game of Connect4 that, before launching, will require the user to enter their name and choose a number between 0 and 2 for the difficulty of the game.
After this, the game will launch and on screen will be a traditional game of Connect4 tailored to the difficulty the user had previously selected.
Once the game is concluded, there will be an option to "click to continue" so they can retry the game, or simply close the window to end the game entirely.

## How to use it?

To use the game, simply open up the game file in a Python supported IDLE that has IPython for the user interactions post-startup. 
Once the pre-requisites are met, the steps are the following:

* run the source code in Spyder
* enter a name for the player 
* choose a number between 0 and 2 for the difficulty of the CPU
* once the game launches, the CPU will automatically have the first turn and the game will tell you how to take your turn
* play the game until there is a winner, or ends in a draw
* to replay the game, at the end, click anywhere on the screen and the game will reset and you will go first, depending on how many times you've reset the game

## Setup

Using the www.anaconda.com website, you can download both Anaconda & Spyder directly from the website. After doing so, run the installers through until the end where you can successfully open up and use the applications.
Once it's been installed fully, run the following commands in the anaconda command line
* pip install pygame
* pip install numpy
* python -m pip install --upgrade pip
Refer to the requirements.txt file to ensure that you have all the packages required for the game.

## Suggested improvements for the future

Although the game is finished and works perfectly, there are few improvements for the future development of the game that can be implemented to make the game better, and enhance user experience when playing.
Some of the the suggestions are the following:

* adding music or a soundtrack in the background to keep the user entertained
* allow the user to choose the colour of their counters
* allow there to be an option in the game to make it two player mode, player vs player as opposed to stricly player vs cpu

## References 

* https://www.pygame.org/docs/ref/image.html
* Allan, S. (2017, July 18). Win Connect 4: Connect Four Strategy, Rules & Instructions. Retrieved from siammandalay.com: https://www.siammandalay.com/blogs/puzzles/win-connect-4-connect-four-strategy-rules-instructions
* Pygame - Chapter 10. (n.d.). Retrieved from inventwithpython.com: https://inventwithpython.com/pygame/chapter10.html
* Pygame. (2019, April 25). Retrieved from pypi.org: https://pypi.org/project/pygame/#:~:text=Pygame%20is%20a%20Python%20wrapper,keyboard%2C%20mouse%20and%20joystick%20input.

