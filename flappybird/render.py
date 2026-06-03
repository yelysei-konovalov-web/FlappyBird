import pygame

from config import GROUND_Y, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE
from state import reset_game


def create_restart_button_rect(button_image):
  rect = button_image.get_rect()
  rect.topleft = (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100)
  return rect


def draw_text(screen, text, font, color, x, y):
  image = font.render(text, True, color)
  screen.blit(image, (x, y))


def draw_button(screen, button_rect, button_image):
  screen.blit(button_image, button_rect)
  return button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1


def draw_game(screen, state, assets, font, button_rect):
  screen.blit(assets["bg"], (0, 0))

  for pipe in state["pipes"]:
    screen.blit(pipe["image"], pipe["rect"])

  bird = state["bird"]
  screen.blit(bird["image"], bird["rect"])

  screen.blit(assets["ground"], (state["ground_scroll"], GROUND_Y))
  draw_text(screen, str(state["score"]), font, WHITE, SCREEN_WIDTH // 2, 20)

  if state["game_over"] and draw_button(screen, button_rect, assets["button"]):
    state["game_over"] = False
    reset_game(state, assets)
