import pygame


def load_assets():
  return {
    "bg": pygame.image.load("../images/bg.png"),
    "ground": pygame.image.load("../images/ground.png"),
    "button": pygame.image.load("../images/restart.png"),
    "bird_images": [
      pygame.image.load(f"../images/bird{num}.png")
      for num in range(1, 4)
    ],
    "pipe": pygame.image.load("../images/pipe.png"),
    "flap_sound": pygame.mixer.Sound("../sounds/flap.mp3"),
    "die_sound": pygame.mixer.Sound("../sounds/die.mp3"),
    "pass_sound": pygame.mixer.Sound("../sounds/pass.mp3"),
  }
