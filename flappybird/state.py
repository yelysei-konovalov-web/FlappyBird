import pygame

from config import PIPE_FREQUENCY
from entities import create_bird


def create_state(assets):
  return {
    "run": True,
    "flying": False,
    "game_over": False,
    "ground_scroll": 0,
    "score": 0,
    "pass_pipe": False,
    "death_sound_played": False,
    "last_pipe": pygame.time.get_ticks() - PIPE_FREQUENCY,
    "bird": create_bird(assets["bird_images"]),
    "pipes": [],
  }


def reset_game(state, assets):
  state["pipes"] = []
  state["bird"] = create_bird(assets["bird_images"])
  state["score"] = 0
  state["pass_pipe"] = False
  state["death_sound_played"] = False
  state["last_pipe"] = pygame.time.get_ticks() - PIPE_FREQUENCY
