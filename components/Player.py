import pygame

from constant import *
from .Paddle import Paddle

class Player(Paddle):
  def __init__(self, screen):
    super().__init__(
      screen,
      COLOR_BLUE,
      PADDING_BORDER_DISTANCE_X,
      PADDING_BORDER_DISTANCE_Y
    )
    
    self.isExtend = False   # state whether the paddle is extend
    self.energy = ENERGY_MAX      # energy for extend the paddle
  
  def render(self):

    # render paddle
    if self.isExtend and self.energy > 0:
      pygame.draw.rect(self.screen, COLOR_LIGHT_BLUE, pygame.Rect(
        self.rect.x,
        self.rect.y - PADDLE_EXTEND,
        self.rect.width,
        PADDLE_EXTEND
      ))
      pygame.draw.rect(self.screen, COLOR_BLUE, self.rect)
      pygame.draw.rect(self.screen, COLOR_LIGHT_BLUE, pygame.Rect(
        self.rect.x,
        self.rect.y + PADDLE_HEIGHT,
        self.rect.width,
        PADDLE_EXTEND
      ))
    else:
      super().render()

    # render energy frame
    pygame.draw.rect(self.screen, COLOR_WHITE, pygame.Rect(
      SCREEN_WIDTH / 2 - ENERGY_WIDTH / 2 - 2 * (ENERGY_SPACE + ENERGY_WIDTH) - 1.5 * ENERGY_SPACE,
      SCREEN_HEIGHT - 200 - 1.5 * ENERGY_SPACE,
      5 * ENERGY_WIDTH + 7 * ENERGY_SPACE,
      ENERGY_HEIGHT + 3 * ENERGY_SPACE
    ))
    pygame.draw.rect(self.screen, COLOR_WHITE, pygame.Rect(
      SCREEN_WIDTH / 2 + 2.5 * ENERGY_WIDTH + 3.5 * ENERGY_SPACE,
      SCREEN_HEIGHT - 200 + ENERGY_HEIGHT / 2 - 10,
      10,
      20
    ))
    pygame.draw.rect(self.screen, COLOR_BACKGROUND, pygame.Rect(
      SCREEN_WIDTH / 2 - ENERGY_WIDTH / 2 - 2 * (ENERGY_SPACE + ENERGY_WIDTH) - ENERGY_SPACE,
      SCREEN_HEIGHT - 200 - ENERGY_SPACE,
      5 * ENERGY_WIDTH + 6 * ENERGY_SPACE,
      ENERGY_HEIGHT + 2 * ENERGY_SPACE
    ))
  
    # render energy
    for i in range(-2, 3):
      if self.energy > 10 * (i + 2):
        pygame.draw.rect(self.screen, COLOR_GREEN, pygame.Rect(
          SCREEN_WIDTH / 2 - ENERGY_WIDTH / 2 + i * (ENERGY_SPACE + ENERGY_WIDTH),
          SCREEN_HEIGHT - 200,
          ENERGY_WIDTH,
          ENERGY_HEIGHT
        ))
