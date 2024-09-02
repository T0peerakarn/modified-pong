# Modified Pong

## Overview

A Pong game developed in Pygame, where the first to score 2 points wins. The game features two AI opponents: an easy bot and a hard bot. After defeating the easy bot, the player will challenge the hard one.

## Bot Strategies

### Easy Bot

The easy bot moves up and down alternatively

### Hard Bot

The hard bot plays optimally by calculating the ball's final position based on its speed along the x-axis and y-axis, then moving to intercept it.

## Extendable Paddle

The player's paddle can be extended to make it easier to fight against the bot by holding down the 'SPACE' button. Note that an energy bar displayed in the middle of the screen will be depleted when the paddle is extended.

## Tools

- **Python**: The programming language used to implement the system.
- **Pygame**: A Python library used for creating the game
