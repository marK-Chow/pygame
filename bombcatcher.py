# version 0.0.0.0.1

import sys, pygame, random, time
import element as el

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

class BombCatcher(object):
    def __init__(self):
        self.pause = False
        self.bspeed = 0
        self.cspeed = 0
        self.score = 0
        self.live = 100
        self.game_over = False

    def set_bomb(self, color = white):
        self.bomb = el.Bomb(color)

    def set_brick(self, color = yellow):
        self.brick = el.Brick(color)
        self.brick.set_position(self.bomb)

    def set_catcher(self, color = blue):
        self.catcher = el.Catcher(color)

    def hit_wall(self):
        if self.bomb.x + self.bomb.radius  > screen_w or self.bomb.x - self.bomb.radius  < 0 :
            self.bomb.changeDirLR()

        if self.bomb.y - self.bomb.radius <= 0 :
            self.bomb.changeDirUD()

    def set_game_element(self, catcher_color = blue, brick_color = yellow, bomb_color = white):
        self.set_bomb()
        self.set_catcher()
        self.set_brick()


bcgame = BombCatcher()
bcgame.set_game_element()
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
            bcgame.bomb.changeDirUD()
            bcgame.bomb.move()
        elif (bcgame.bomb.y + bcgame.bomb.radius) >= screen_h:
            bcgame.live -= 1
            if bcgame.live == 0 :
                bcgame.game_over = True
            else :
                time.sleep(0.3)
                bcgame.set_bomb()
        elif ((bcgame.bomb.x + bcgame.bomb.radius) >= bcgame.brick.x and (bcgame.bomb.x - bcgame.bomb.radius) <= (bcgame.brick.x + bcgame.brick.width) and
            (bcgame.bomb.y + bcgame.bomb.radius) >= bcgame.brick.y and (bcgame.bomb.y - bcgame.bomb.radius) <= (bcgame.brick.y + bcgame.brick.height)) :
            bcgame.score += 1
            if ((bcgame.bomb.x + bcgame.bomb.radius) >= bcgame.brick.x and (bcgame.bomb.x - bcgame.bomb.radius) <= (bcgame.brick.x + bcgame.brick.width) and (bcgame.bomb.y < bcgame.brick.y or bcgame.bomb.y > bcgame.brick.y)) :
                bcgame.bomb.changeDirUD()
            elif ((bcgame.bomb.y + bcgame.bomb.radius) >= bcgame.brick.y and (bcgame.bomb.y - bcgame.bomb.radius) <= (bcgame.brick.y + bcgame.brick.height) and (bcgame.bomb.x < bcgame.brick.x or bcgame.bomb.x > bcgame.brick.x)) :
                bcgame.bomb.changeDirLR()
            if bcgame.score % 5 == 0 and bcgame.score > 0:
                bcgame.bomb.speed += 0.01
            bcgame.set_brick()
            bcgame.brick.set_position(bcgame.bomb)
            bcgame.bomb.move()
        else :
            bcgame.hit_wall()
            bcgame.bomb.move()

    pygame.draw.rect(screen, bcgame.brick.color, (bcgame.brick.x, bcgame.brick.y, bcgame.brick.width, bcgame.brick.height), 0)
    pygame.draw.rect(screen, bcgame.catcher.color, (bcgame.catcher.x, bcgame.catcher.y, bcgame.catcher.width,bcgame.catcher.height), 0)
    pygame.draw.circle(screen, bcgame.bomb.color, (int(bcgame.bomb.x), int(bcgame.bomb.y)), bcgame.bomb.radius, 0)
    print_text(font1, 5, 5, "Score : " + str(bcgame.score))
    print_text(font1, 5, 35, "Live : " + str(bcgame.live))
    print_text(font1, 500, 5, "Speed : " + str(round(bcgame.bomb.speed,2)))
    pygame.display.update()
