import pygame

def handle_events(state):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      state["run"] = False
    if event.type == pygame.MOUSEBUTTONDOWN and not state["flying"] and not state["game_over"]:
      state["flying"] = True
