import pygame

from app.config import GROUND_Y, PIPE_FREQUENCY, SCROLL_SPEED
from app.entities import create_pipe_pair


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
