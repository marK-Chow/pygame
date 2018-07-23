# version 0.0.0.0.1

import sys, pygame, random

from pygame.locals import *

# Basic
pygame.init()

screen_w = 600
screen_h = 500

screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Bomb catching game")

### font
font1 = pygame.font.Font(None, 24)

### color
white = 255, 255, 255
red = 220, 50, 50
yellow = 230, 230, 0
black = 0, 0, 0
blue = 0, 0 , 200

### Func
def print_text(font, x, y, text, color = white):
    imgTxt = font.render(text, True, color)
    screen.blit(imgTxt, (x, y))

class Bomb(object):
    def __init__(self):
        self.x = 30
        self.y = 25
        self.speed = 0.01
        self.radius = 5
        self.color = white
        self.down = True
        self.left = True


    def move(self):

        # Hit the wall
        if self.x + self.radius  > screen_w or self.x - self.radius  < 0 :
            self.left = not self.left
        if self.y - self.radius  <= 0 :
            self.down = not self.down

        # Bomb x move
        if self.left :
            self.x -= self.speed
        else :
            self.x += self.speed

        # Bomb y move
        if self.down :
            self.y += self.speed
        else :
            self.y -= self.speed

class Catcher(object):
    def __init__(self):
        self.x = 0
        self.y = 495
        self.width = 50
        self.height = 5
        self.speed = 20
        self.color = blue

class BombCatcher(object):
    def __init__(self):
        self.score = 0
        self.live = 1
        self.game_over = False
        self.bomb = Bomb()
        self.catcher = Catcher()

bcgame = BombCatcher()

# Game loop
while True:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            sys.exit()
        elif ev.type == KEYDOWN :
            if ev.key == K_ESCAPE:
                sys.exit()
            if ev.key == K_LEFT and bcgame.catcher.x - bcgame.catcher.speed >= 0 :
                bcgame.catcher.x -= bcgame.catcher.speed
            if ev.key == K_RIGHT and (bcgame.catcher.x + bcgame.catcher.width + bcgame.catcher.speed)<= screen_w :
                bcgame.catcher.x += bcgame.catcher.speed

    screen.fill((0, 0, 100))

    if bcgame.game_over:
        print_text(font1, 200, 200, "You lost!!! Please <Enter> to restart!!!")
    else :
        if (bcgame.bomb.y + bcgame.bomb.radius) >= bcgame.catcher.y and bcgame.bomb.x >= bcgame.catcher.x and bcgame.bomb.x <= (bcgame.catcher.x + bcgame.catcher.width):
            bcgame.score += 1
            bcgame.bomb.down = False
            bcgame.bomb.move()
        elif (bcgame.bomb.y + bcgame.bomb.radius) == screen_h:
            bcgame.live -= 1
            if bcgame.live == 0 :
                bcgame.game_over = True
                bcgame.bomb.speed = 0
                bcgame.catcher.speed = 0
        else :
            bcgame.bomb.move()

    pygame.draw.rect(screen, bcgame.catcher.color, (bcgame.catcher.x, bcgame.catcher.y, bcgame.catcher.width,bcgame.catcher.height), 0)
    pygame.draw.circle(screen, bcgame.bomb.color, (int(bcgame.bomb.x), int(bcgame.bomb.y)), bcgame.bomb.radius, 0)

    pygame.display.update()
