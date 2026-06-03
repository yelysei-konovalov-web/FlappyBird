import pygame

from flappybird.assets import load_assets
from flappybird.config import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from flappybird.events import handle_events
from flappybird.render import create_restart_button_rect, draw_game
from flappybird.state import create_state
from flappybird.update import update_game


def main():
  pygame.init()

  clock = pygame.time.Clock()
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  pygame.display.set_caption("Flappy Bird")
  font = pygame.font.SysFont("Bauhaus 93", 60)
  assets = load_assets()
  button_rect = create_restart_button_rect(assets["button"])
  state = create_state(assets)

  while state["run"]:
    clock.tick(FPS)
    handle_events(state)
    update_game(state, assets)
    draw_game(screen, state, assets, font, button_rect)
    pygame.display.update()

  pygame.quit()


main()
