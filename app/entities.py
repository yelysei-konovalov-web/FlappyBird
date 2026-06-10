import random
import pygame
from config import PIPE_GAP, SCREEN_HEIGHT, SCREEN_WIDTH


def create_bird(images):
  rect = images[0].get_rect()
  rect.center = [100, SCREEN_HEIGHT // 2]
  return {
    "rect": rect,
    "velocity": 0,
    "clicked": False,
    "image_index": 0,
    "counter": 0,
    "image": images[0],
  }


def create_pipe_pair(pipe_image):
  pipe_height = random.randint(-100, 100)
  pipe_center_y = SCREEN_HEIGHT // 2 + pipe_height

  top_image = pygame.transform.flip(pipe_image, False, True)
  top_rect = top_image.get_rect()
  top_rect.bottomleft = [SCREEN_WIDTH, pipe_center_y - PIPE_GAP // 2]

  bottom_rect = pipe_image.get_rect()
  bottom_rect.topleft = [SCREEN_WIDTH, pipe_center_y + PIPE_GAP // 2]

  return [
    {"image": top_image, "rect": top_rect},
    {"image": pipe_image, "rect": bottom_rect},
  ]
