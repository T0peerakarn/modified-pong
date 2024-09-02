import pygame, sys, random

from constant import *
from components.Ball import Ball
from components.Player import Player
from components.Bot import Bot

class PongGame:
  def __init__(self):
    pygame.init()

    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    self.music_channel = pygame.mixer.Channel(0)
    self.music_channel.set_volume(0.2)

    self.sounds_list = {
      SOUND_PADDLE_HIT: pygame.mixer.Sound(f"{ROOT_PATH}/assets/sounds/paddle_hit.wav"),
      SOUND_WALL_HIT: pygame.mixer.Sound(f"{ROOT_PATH}/assets/sounds/wall_hit.wav"),
      SOUND_SCORE: pygame.mixer.Sound(f"{ROOT_PATH}/assets/sounds/score.wav"),
    }

    self.small_font = pygame.font.Font(f"{ROOT_PATH}/assets/font/04b03.ttf", 24)
    self.large_font = pygame.font.Font(f"{ROOT_PATH}/assets/font/04b03.ttf", 48)
    self.score_font = pygame.font.Font(f"{ROOT_PATH}/assets/font/04b03.ttf", 96)

    self.player_score = 0
    self.bot_score = 0

    self.serving = PLAYER
    self.winning = 0

    self.player = Player(self.screen)
    self.bot = Bot(self.screen, BOT_EASY)

    self.ball = Ball(self.screen, SCREEN_WIDTH / 2 - 6, SCREEN_HEIGHT / 2 - 6)

    self.game_state = STATE_START

  def init(self):
    self.ball.init()

    self.player_score = 0
    self.bot_score = 0

    self.serving = PLAYER if self.winning == BOT else BOT

  def update(self, dt, events):
    for event in events:
      
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      if event.type == pygame.KEYDOWN:

        if event.key == pygame.K_RETURN:

          if self.game_state == STATE_START:
            self.game_state = STATE_SERVE

          elif self.game_state == STATE_SERVE:
            self.game_state = STATE_PLAY

          elif self.game_state == STATE_DONE:
            
            # reset the game
            self.game_state = STATE_SERVE
            self.bot = Bot(self.screen, BOT_EASY)
            self.init()

    if self.game_state == STATE_SERVE:

      # random dx, dy for the serve
      self.ball.dx = BALL_INITIAL_SPEED * (1 if self.serving == PLAYER else -1)
      self.ball.dy = random.uniform(-150, 150)

    elif self.game_state == STATE_PLAY:

      # ball hits paddle
      if self.ball.isCollide(self.player) or self.ball.isCollide(self.bot):
        self.ball.dx = -self.ball.dx * REFLECT_SPEED_MULTIPLIER
        self.ball.dy = random.uniform(30, 450) * (-1 if self.ball.dy <= 0 else 1)

        self.music_channel.play(self.sounds_list[SOUND_PADDLE_HIT])

      # ball hits top/bottom wall
      if self.ball.rect.y <= 0 or self.ball.rect.y >= SCREEN_HEIGHT - BALL_SIZE:
        self.ball.dy = -self.ball.dy

        self.music_channel.play(self.sounds_list[SOUND_WALL_HIT])

      # ball hits left wall - bot's score
      # player serves next
      if self.ball.rect.x <= 0:
        self.serving = PLAYER
        self.bot_score += 1

        self.music_channel.play(self.sounds_list[SOUND_SCORE])

        if self.bot_score == WINNING_SCORE:
          self.winning = BOT
          self.game_state = STATE_DONE

        else:
          self.game_state = STATE_SERVE
          self.ball.init()

      # ball hit right wall - player's score
      # bot serves next
      if self.ball.rect.x >= SCREEN_WIDTH:
        self.serving = BOT
        self.player_score += 1

        self.music_channel.play(self.sounds_list[SOUND_SCORE])

        if self.player_score == WINNING_SCORE:
          self.winning = PLAYER

          if self.bot.mode == BOT_EASY:
            self.game_state = STATE_SERVE
            self.bot = Bot(self.screen, BOT_HARD)
            self.init()

          else:
            self.game_state = STATE_DONE
            
        else:
          self.game_state = STATE_SERVE
          self.ball.init()

    key = pygame.key.get_pressed()

    # player's move
    if key[pygame.K_w]:
      self.player.dy = -PADDLE_SPEED
    elif key[pygame.K_s]:
      self.player.dy = PADDLE_SPEED
    else:
      self.player.dy = 0

    # extend the bar according to K_SPACE
    self.player.isExtend = key[pygame.K_SPACE]
    self.player.energy = max(0, self.player.energy - 1) if key[pygame.K_SPACE] else min(ENERGY_MAX, self.player.energy + 1)

    # bot's move
    if self.bot.mode == BOT_EASY:

      # for easy bot, it just move up and down alternatively
      self.bot.dy = -PADDLE_SPEED if self.bot.dy == 0 else self.bot.dy
      if self.bot.rect.y <= 0 or self.bot.rect.y + PADDLE_HEIGHT >= SCREEN_HEIGHT:
        self.bot.dy *= -1
    else:

      # for hard bot, if the ball is facing to player,
      # it will move to the center of screen
      # to prepare for the reflected ball
      if self.ball.dx <= 0:
        if abs(self.bot.rect.y + PADDLE_HEIGHT / 2 - SCREEN_HEIGHT / 2) <= BALL_SIZE / 2:
          self.bot.dy = 0
        else:
          self.bot.dy = PADDLE_SPEED if self.bot.rect.y + PADDLE_HEIGHT / 2 <= SCREEN_HEIGHT / 2 else -PADDLE_SPEED

      # otherwise, it predicts the position of the ball
      # and try to move to that position
      # which should be the optimal move
      else:
        tx = (SCREEN_WIDTH - PADDING_BORDER_DISTANCE_X - PADDLE_WIDTH - self.ball.rect.x - BALL_SIZE) / self.ball.dx
        sy = self.ball.rect.y + self.ball.dy * tx

        # just in case of reflect from top/bottom border
        while sy <= 0 or sy >= SCREEN_HEIGHT - BALL_SIZE:
          if sy <= 0:
            sy *= -1
          if sy >= SCREEN_HEIGHT - BALL_SIZE:
            sy = 2 * (SCREEN_HEIGHT - BALL_SIZE) - sy

        if abs(self.bot.rect.y + PADDLE_HEIGHT / 2 - sy - BALL_SIZE / 2) <= BALL_SIZE / 2:
          self.bot.dy = 0
        else:
          self.bot.dy = PADDLE_SPEED if self.bot.rect.y + PADDLE_HEIGHT / 2 <= sy + BALL_SIZE / 2 else -PADDLE_SPEED
    
    # update the position according to step of dt
    if self.game_state == STATE_PLAY:
      self.ball.update(dt)
      self.player.update(dt)
      self.bot.update(dt)

  def render(self):

    # background
    self.screen.fill(COLOR_BACKGROUND)

    if self.game_state == STATE_START:

      # welcome message

      t_welcome = self.large_font.render(
        "Welcome to Pong!",
        False,
        COLOR_WHITE,
      )
      text_rect = t_welcome.get_rect(center=(SCREEN_WIDTH / 2, 70))
      self.screen.blit(t_welcome, text_rect)

      t_press_enter_begin = self.small_font.render(
        "Press Enter to begin!",
        False,
        COLOR_WHITE,
      )
      text_rect = t_press_enter_begin.get_rect(center=(SCREEN_WIDTH / 2, 120))
      self.screen.blit(t_press_enter_begin, text_rect)

    elif self.game_state == STATE_SERVE:

      # display the current bot,
      # along with who serve next,
      # and color the text according to bot's mode
      # EASY -> green, HARD -> red

      t_bot_prefix = self.large_font.render(
        f"Playing with ",
        False,
        COLOR_WHITE
      )
      text_rect = t_bot_prefix.get_rect(center=(SCREEN_WIDTH / 2 - 111, 70))
      self.screen.blit(t_bot_prefix, text_rect)

      t_bot_mode = self.large_font.render(
        f"{'EASY' if self.bot.mode == BOT_EASY else 'HARD'}",
        False,
        COLOR_ORANGE if self.bot.mode == BOT_EASY else COLOR_RED
      )
      text_rect = t_bot_mode.get_rect(center=(SCREEN_WIDTH / 2 + 108, 70))
      self.screen.blit(t_bot_mode, text_rect)

      t_bot_suffix = self.large_font.render(
        f" bot",
        False,
        COLOR_WHITE
      )
      text_rect = t_bot_suffix.get_rect(center=(SCREEN_WIDTH / 2 + 219, 70))
      self.screen.blit(t_bot_suffix, text_rect)

      t_serve = self.small_font.render(
        f"{self.serving}'s serve!",
        False,
        COLOR_WHITE,
      )
      text_rect = t_serve.get_rect(center=(SCREEN_WIDTH / 2, 120))
      self.screen.blit(t_serve, text_rect)

      t_enter_serve = self.small_font.render(
        "Press Enter to serve!",
        False,
        COLOR_WHITE,
      )
      text_rect = t_enter_serve.get_rect(center=(SCREEN_WIDTH / 2, 160))
      self.screen.blit(t_enter_serve, text_rect)

    elif self.game_state == STATE_PLAY:

      # nothing display during the game

      pass

    elif self.game_state == STATE_DONE:

      # show the winner

      t_win = self.large_font.render(
        f"{self.winning}'s wins!",
        False,
        COLOR_WHITE,
      )
      text_rect = t_win.get_rect(center=(SCREEN_WIDTH / 2, 70))
      self.screen.blit(t_win, text_rect)

      t_restart = self.small_font.render(
        "Press Enter to restart",
        False,
        COLOR_WHITE,
      )
      text_rect = t_restart.get_rect(center=(SCREEN_WIDTH / 2, 120))
      self.screen.blit(t_restart, text_rect)

    self.displayPermanentText()

    # render player's paddle
    self.player.render()

    # render bot's paddle
    self.bot.render()

    # render ball
    self.ball.render()

  def displayPermanentText(self):

    # score
    t_player_score = self.score_font.render(
      f"{self.player_score}",
      False,
      COLOR_BLUE,
    )
    t_bot_score = self.score_font.render(
      f"{self.bot_score}",
      False,
      COLOR_ORANGE if self.bot.mode == BOT_EASY else COLOR_RED,
    )
    self.screen.blit(t_player_score, (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 3))
    self.screen.blit(t_bot_score, (SCREEN_WIDTH / 2 + 90, SCREEN_HEIGHT / 3))

    # energy description
    t_energy_description = self.small_font.render(
      f"Hold SPACE to extend your paddle",
      False,
      COLOR_WHITE,
    )
    text_rect = t_energy_description.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 105))
    self.screen.blit(t_energy_description, text_rect)

if __name__ == "__main__":

  game = PongGame()
  clock = pygame.time.Clock()

  while True:
    
    pygame.display.set_caption(f"Pong game running with {int(clock.get_fps())} FPS")

    # elapsed time from the last call
    dt = clock.tick(MAX_FRAME_RATE) / 1000.0

    events = pygame.event.get()
    game.update(dt, events)
    game.render()

    pygame.display.update()
