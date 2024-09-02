import pygame

from constant import *
from .Paddle import Paddle

class Bot(Paddle):
  def __init__(self, screen, mode):
    
    super().__init__(
      screen,
      COLOR_ORANGE if mode == BOT_EASY else COLOR_RED,
      SCREEN_WIDTH - PADDLE_WIDTH - PADDING_BORDER_DISTANCE_X,
      SCREEN_HEIGHT - PADDLE_HEIGHT - PADDING_BORDER_DISTANCE_Y,
    )

    self.mode = mode
    