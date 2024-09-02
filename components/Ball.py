import pygame, random

from constant import *

class Ball:
  def __init__(self, screen, x, y, width = BALL_SIZE, height = BALL_SIZE):
    self.screen=screen

    self.rect = pygame.Rect(x, y, width, height)

    self.dx = 0
    self.dy = 0

  def isCollide(self, paddle):
    # first, check to see if the left edge of either is farther to the right
    # than the right edge of the other
    if self.rect.x > paddle.rect.x + paddle.rect.width or paddle.rect.x > self.rect.x + self.rect.width:
      return False
    
    # then check to see if the bottom edge of either is higher than the top
    # edge of the other

    if hasattr(paddle, 'isExtend'):
      if self.rect.y > paddle.rect.y + paddle.rect.height + (PADDLE_EXTEND if paddle.isExtend else 0) \
        or paddle.rect.y - self.rect.height - (PADDLE_EXTEND if paddle.isExtend else 0) > self.rect.y:
        return False
    else:
      if self.rect.y > paddle.rect.y + paddle.rect.height or paddle.rect.y - self.rect.height > self.rect.y:
        return False
      
    # otherwise, the ball and the paddle are collapsed
    return True

  def init(self):
    self.rect.x = SCREEN_WIDTH / 2 - BALL_SIZE / 2
    self.rect.y = SCREEN_HEIGHT / 2 - BALL_SIZE / 2
    self.dx = 0
    self.dy = 0

  def update(self, dt):
    self.rect.x += self.dx * dt
    self.rect.y += self.dy * dt

  def render(self):
    pygame.draw.rect(self.screen, COLOR_WHITE, self.rect)
