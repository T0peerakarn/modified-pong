import pygame

from constant import *

class Paddle:
  def __init__(self, screen, color, x, y, width = PADDLE_WIDTH, height = PADDLE_HEIGHT):

    self.screen = screen
    self.color = color
    self.rect = pygame.Rect(x, y, width, height)

    self.dy = 0 # speed in y-axis


  def update(self, dt):
    if self.dy > 0:
      if self.rect.y + self.rect.height < SCREEN_HEIGHT:
        self.rect.y += self.dy * dt
    else:
      if self.rect.y > 0:
        self.rect.y += self.dy * dt

  def render(self):

    # render paddle
    pygame.draw.rect(self.screen, self.color, self.rect)