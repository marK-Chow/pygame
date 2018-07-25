# version 0.0.0.0.1

import sys, pygame, random, time

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
        self.x = random.randint(10, 590)
        self.y = random.randint(40, 200)
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
        self.width = 600
        self.height = 5
        self.speed = 20
        self.color = blue

class Brick(object):
    def __init__(self):
        self.show = False
        self.width = 50
        self.height = 10
        self.color = yellow
        self.x = random.randint(10, 590)
        self.y = random.randint(40, 200)

    def set_position(self, bomb):
        while not self.show:
            if bomb.x >= self.x and bomb.x <= self.x + self.width and bomb.y >= self.y and bomb.y <= self.y + self.height :
                self.x = random.randint(10, 590)
                self.y = random.randint(40, 200)
            else :
                self.show = True

class BombCatcher(object):
    def __init__(self):
        self.pause = False
        self.bspeed = 0
        self.cspeed = 0
        self.score = 0
        self.live = 100
        self.game_over = False
        self.bomb = Bomb()
        self.catcher = Catcher()
        self.brick = Brick()
        self.brick.set_position(self.bomb)


bcgame = BombCatcher()

# Game loop
while True:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            sys.exit()
        elif ev.type == KEYDOWN :
            if ev.key == K_ESCAPE:
                sys.exit()
            if not bcgame.game_over :
                if ev.key == K_SPACE :
                    bcgame.pause = not bcgame.pause
                    if bcgame.pause :
                        bcgame.bspeed = bcgame.bomb.speed
                        bcgame.cspeed = bcgame.catcher.speed
                        bcgame.bomb.speed = 0
                        bcgame.catcher.speed = 0
                    else :
                        bcgame.bomb.speed = bcgame.bspeed
                        bcgame.catcher.speed = bcgame.cspeed
                if not bcgame.pause :
                    if ev.key == K_LEFT and bcgame.catcher.x - bcgame.catcher.speed >= 0 :
                        bcgame.catcher.x -= bcgame.catcher.speed
                    if ev.key == K_RIGHT and (bcgame.catcher.x + bcgame.catcher.width + bcgame.catcher.speed)<= screen_w :
                        bcgame.catcher.x += bcgame.catcher.speed
                    if ev.key == K_UP :
                        bcgame.bomb.speed += 0.01
                    if ev.key == K_DOWN and bcgame.bomb.speed > 0.01 :
                        bcgame.bomb.speed -= 0.01
            elif ev.key == K_KP_ENTER or ev.key == K_RETURN :
                bcgame = BombCatcher()

    screen.fill((0, 0, 100))

    if bcgame.game_over:
        print_text(font1, 200, 200, "You lost!!! Please <Enter> to restart!!!")
    else :
        if ((bcgame.bomb.y + bcgame.bomb.radius) >= bcgame.catcher.y and bcgame.bomb.x >= bcgame.catcher.x and bcgame.bomb.x <= (bcgame.catcher.x + bcgame.catcher.width)) :
            bcgame.bomb.down = False
            if bcgame.score % 5 == 0 and bcgame.score > 0:
                bcgame.bomb.speed += 0.01
            bcgame.bomb.move()
        elif (bcgame.bomb.y + bcgame.bomb.radius) >= screen_h:
            bcgame.live -= 1
            if bcgame.live == 0 :
                bcgame.game_over = True
            else :
                time.sleep(0.3)
                bcgame.bomb = Bomb()
        elif ((bcgame.bomb.x + bcgame.bomb.radius) >= bcgame.brick.x and (bcgame.bomb.x - bcgame.bomb.radius) <= (bcgame.brick.x + bcgame.brick.width) and
            (bcgame.bomb.y + bcgame.bomb.radius) >= bcgame.brick.y and (bcgame.bomb.y - bcgame.bomb.radius) <= (bcgame.brick.y + bcgame.brick.height)) :
            bcgame.score += 1
            if ((bcgame.bomb.x + bcgame.bomb.radius) >= bcgame.brick.x and (bcgame.bomb.x - bcgame.bomb.radius) <= (bcgame.brick.x + bcgame.brick.width) and (bcgame.bomb.y < bcgame.brick.y or bcgame.bomb.y > bcgame.brick.y)) :
                bcgame.bomb.down = not bcgame.bomb.down
            elif ((bcgame.bomb.y + bcgame.bomb.radius) >= bcgame.brick.y and (bcgame.bomb.y - bcgame.bomb.radius) <= (bcgame.brick.y + bcgame.brick.height) and (bcgame.bomb.x < bcgame.brick.x or bcgame.bomb.x > bcgame.brick.x)) :
                bcgame.bomb.left = not bcgame.bomb.left
            bcgame.brick = Brick()
            bcgame.brick.set_position(bcgame.bomb)
            bcgame.bomb.move()
        else :
            bcgame.bomb.move()

    pygame.draw.rect(screen, bcgame.brick.color, (bcgame.brick.x, bcgame.brick.y, bcgame.brick.width, bcgame.brick.height), 0)
    pygame.draw.rect(screen, bcgame.catcher.color, (bcgame.catcher.x, bcgame.catcher.y, bcgame.catcher.width,bcgame.catcher.height), 0)
    pygame.draw.circle(screen, bcgame.bomb.color, (int(bcgame.bomb.x), int(bcgame.bomb.y)), bcgame.bomb.radius, 0)
    print_text(font1, 5, 5, "Score : " + str(bcgame.score))
    print_text(font1, 5, 35, "Live : " + str(bcgame.live))
    print_text(font1, 500, 5, "Speed : " + str(round(bcgame.bomb.speed,2)))
    pygame.display.update()
