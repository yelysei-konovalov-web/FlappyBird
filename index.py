import random

import pygame


SCREEN_WIDTH = 864
SCREEN_HEIGHT = 936
FPS = 60
GROUND_Y = 768
PIPE_GAP = 150
PIPE_FREQUENCY = 1500
SCROLL_SPEED = 4
WHITE = (255, 255, 255)


def load_assets():
  return {
    "bg": pygame.image.load("images/bg.png"),
    "ground": pygame.image.load("images/ground.png"),
    "button": pygame.image.load("images/restart.png"),
    "bird_images": [pygame.image.load(f"images/bird{num}.png") for num in range(1, 4)],
    "pipe": pygame.image.load("images/pipe.png"),
    "flap_sound": pygame.mixer.Sound("sounds/flap.mp3"),
    "die_sound": pygame.mixer.Sound("sounds/die.mp3"),
    "pass_sound": pygame.mixer.Sound("sounds/pass.mp3"),
  }


def create_bird(images):
  rect = images[0].get_rect()
  rect.center = [100, SCREEN_HEIGHT // 2]
  return {
    "rect": rect,
    "velocity": 0,
    "clicked": False,
    "image_index": 0,
    "animation_counter": 0,
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


def reset_game(state, assets):
  state["pipes"] = []
  state["bird"] = create_bird(assets["bird_images"])
  state["score"] = 0
  state["pass_pipe"] = False
  state["death_sound_played"] = False
  state["last_pipe"] = pygame.time.get_ticks() - PIPE_FREQUENCY


def draw_text(screen, text, font, color, x, y):
  image = font.render(text, True, color)
  screen.blit(image, (x, y))


def draw_button(screen, button_rect, button_image):
  screen.blit(button_image, button_rect)
  return button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1


def update_bird(bird, flying, game_over, bird_images, flap_sound):
  if flying:
    bird["velocity"] += 0.5
    if bird["velocity"] > 8:
      bird["velocity"] = 8
    if bird["rect"].bottom < GROUND_Y:
      bird["rect"].y += int(bird["velocity"])

  if game_over:
    bird["image"] = pygame.transform.rotate(bird_images[bird["image_index"]], -90)
    return

  if pygame.mouse.get_pressed()[0] == 1 and not bird["clicked"]:
    bird["clicked"] = True
    bird["velocity"] = -10
    flap_sound.play()
  if pygame.mouse.get_pressed()[0] == 0:
    bird["clicked"] = False

  bird["animation_counter"] += 1
  if bird["animation_counter"] > 5:
    bird["animation_counter"] = 0
    bird["image_index"] = (bird["image_index"] + 1) % len(bird_images)

  bird["image"] = pygame.transform.rotate(
    bird_images[bird["image_index"]],
    bird["velocity"] * -2,
  )


def update_pipes(pipes):
  for pipe in pipes:
    pipe["rect"].x -= SCROLL_SPEED
  return [pipe for pipe in pipes if pipe["rect"].right >= 0]


def update_score(state, pass_sound):
  pipes = state["pipes"]
  if not pipes:
    return

  bird_rect = state["bird"]["rect"]
  first_pipe_rect = pipes[0]["rect"]

  if (
    bird_rect.left > first_pipe_rect.left
    and bird_rect.right < first_pipe_rect.right
    and not state["pass_pipe"]
  ):
    state["pass_pipe"] = True

  if state["pass_pipe"] and bird_rect.left > first_pipe_rect.right:
    state["score"] += 1
    pass_sound.play()
    state["pass_pipe"] = False


def has_collision(bird_rect, pipes):
  if bird_rect.top < 0 or bird_rect.bottom >= GROUND_Y:
    return True
  return any(bird_rect.colliderect(pipe["rect"]) for pipe in pipes)


def play_death_sound_once(state, die_sound):
  if not state["death_sound_played"]:
    die_sound.play()
    state["death_sound_played"] = True


def handle_events(state):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      state["run"] = False
    if event.type == pygame.MOUSEBUTTONDOWN and not state["flying"] and not state["game_over"]:
      state["flying"] = True


def draw_game(screen, state, assets, font, button_rect):
  screen.blit(assets["bg"], (0, 0))

  bird = state["bird"]
  screen.blit(bird["image"], bird["rect"])

  for pipe in state["pipes"]:
    screen.blit(pipe["image"], pipe["rect"])

  screen.blit(assets["ground"], (state["ground_scroll"], GROUND_Y))
  draw_text(screen, str(state["score"]), font, WHITE, SCREEN_WIDTH // 2, 20)

  if state["game_over"] and draw_button(screen, button_rect, assets["button"]):
    state["game_over"] = False
    reset_game(state, assets)


def update_game(state, assets):
  update_bird(
    state["bird"],
    state["flying"],
    state["game_over"],
    assets["bird_images"],
    assets["flap_sound"],
  )
  update_score(state, assets["pass_sound"])

  if has_collision(state["bird"]["rect"], state["pipes"]):
    play_death_sound_once(state, assets["die_sound"])
    state["game_over"] = True
    if state["bird"]["rect"].bottom >= GROUND_Y:
      state["flying"] = False

  if state["game_over"] or not state["flying"]:
    return

  time_now = pygame.time.get_ticks()
  if time_now - state["last_pipe"] > PIPE_FREQUENCY:
    state["pipes"].extend(create_pipe_pair(assets["pipe"]))
    state["last_pipe"] = time_now

  state["ground_scroll"] -= SCROLL_SPEED
  if abs(state["ground_scroll"]) > 35:
    state["ground_scroll"] = 0

  state["pipes"] = update_pipes(state["pipes"])


def main():
  pygame.init()

  clock = pygame.time.Clock()
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  pygame.display.set_caption("Flappy Bird")
  font = pygame.font.SysFont("Bauhaus 93", 60)
  assets = load_assets()

  button_rect = assets["button"].get_rect()
  button_rect.topleft = (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100)

  state = {
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

  while state["run"]:
    clock.tick(FPS)
    handle_events(state)
    update_game(state, assets)
    draw_game(screen, state, assets, font, button_rect)
    pygame.display.update()

  pygame.quit()


if __name__ == "__main__":
  main()
