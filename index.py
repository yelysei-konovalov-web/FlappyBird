import pygame
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

font = pygame.font.SysFont('Bauhaus 93', 60)

white = (255, 255, 255)

ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #ms
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

run = True

bg = pygame.image.load('images/bg.png')
ground_img = pygame.image.load('images/ground.png')
button_img = pygame.image.load('images/restart.png')

def draw_text(text, font, text_color, x, y):
  img = font.render(text, True, text_color)
  screen.blit(img, (x, y))

def reset_game():
  pipe_group.empty()
  flappy.rect.x = 100
  flappy.rect.y = int(screen_height / 2)
  score = 0
  return score


class Bird(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.images = [pygame.image.load(f'images/bird{num}.png') for num in range(1, 4)]
    self.index = 0
    self.counter = 0
    self.image = self.images[self.index]
    self.rect = self.image.get_rect()
    self.rect.center = [x, y]
    self.velocity = 0
    self.clicked = False
    self.flap_sound = pygame.mixer.Sound('sounds/flap.mp3')
    self.die_sound = pygame.mixer.Sound('sounds/die.mp3')
    self.pass_sound = pygame.mixer.Sound('sounds/pass.mp3')

  def update(self):
    if flying:
      self.velocity += 0.5
      if self.velocity > 8:
        self.velocity = 8
      if self.rect.bottom < 768:
        self.rect.y += int(self.velocity)

    if not game_over:
      #jump
      if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
        self.clicked = True
        self.velocity = -10
        self.flap_sound.play()
      if pygame.mouse.get_pressed()[0] == 0:
        self.clicked = False

      #animation
      self.counter += 1
      flap_cooldown = 5

      if self.counter > flap_cooldown:
        self.counter = 0
        self.index += 1
        if self.index >= len(self.images):
          self.index = 0
      self.image = self.images[self.index]

      #rotation
      self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -2)
    else:
      self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
  def __init__(self, x, y, position):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('images/pipe.png')
    self.rect = self.image.get_rect()
    #position 1 is from the top,
    # -1 is from the bottom
    if position == 1:
      self.image = pygame.transform.flip(self.image, False, True)
      self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
    if position == -1:
      self.rect.topleft = [x, y + int(pipe_gap / 2)]

  def update(self):
    self.rect.x -= scroll_speed
    if self.rect.right < 0:
      self.kill()

class Button():
  def __init__(self, x, y, image):
    self.image = image
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)

  def draw(self):

    action = False

    #get mouse pos
    pos = pygame.mouse.get_pos()

    #check mouse hover
    if self.rect.collidepoint(pos):
      if pygame.mouse.get_pressed()[0] == 1:
        action = True


    #draw button
    screen.blit(self.image, (self.rect.x, self.rect.y))

    return action


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)

# create restart button

button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)



while run:
  clock.tick(fps)

  screen.blit(bg, (0,0))

  bird_group.draw(screen)
  bird_group.update()
  pipe_group.draw(screen)


  #draw ground
  screen.blit(ground_img, (ground_scroll, 768))

  #check the score

  if len(pipe_group) > 0:
    if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
      and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
      and not pass_pipe:
      pass_pipe = True
    if pass_pipe:
      if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
        score += 1
        flappy.pass_sound.play()
        pass_pipe = False

  draw_text(str(score), font, white, int(screen_width / 2), 20)


  #collision
  if (pygame.sprite.groupcollide(bird_group, pipe_group, False, False)
    or flappy.rect.top < 0):
    flappy.die_sound.play()
    game_over = True
  #checking bird died
  if flappy.rect.bottom >= 768:
    flappy.die_sound.play()
    game_over = True
    flying = False

  if not game_over and flying:

    time_now = pygame.time.get_ticks()
    if time_now - last_pipe > pipe_frequency:
      pipe_height = random.randint(-100, 100)
      top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
      bottom_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
      pipe_group.add(top_pipe)
      pipe_group.add(bottom_pipe)
      last_pipe = time_now

    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 35:
      ground_scroll = 0

    pipe_group.update()

  #check for game over and reset
  if game_over:
    if button.draw():
      game_over = False
      reset_game()
      score = reset_game()


  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    if (event.type == pygame.MOUSEBUTTONDOWN
      and flying == False
      and game_over == False):
      flying = True

  pygame.display.update()

pygame.quit()