import random
# Catcher
class Catcher(object):
    def __init__(self, color = (0, 0, 0)):
        self.x = 0
        self.y = 495
        self.width = 600
        self.height = 5
        self.speed = 50
        self.color = color
# Brick
class Brick(object):
    def __init__(self, color = (0, 0, 0)):
        self.show = False
        self.width = 50
        self.height = 10
        self.color = color
        self.x = random.randint(10, 540)
        self.y = random.randint(40, 200)

    def set_position(self, bomb):
        while not self.show:
            if bomb.x >= self.x and bomb.x <= self.x + self.width and bomb.y >= self.y and bomb.y <= self.y + self.height :
                self.x = random.randint(10, 540)
                self.y = random.randint(50, 200)
            else :
                self.show = True
# Bomb
class Bomb(object):
    def __init__(self, color = (0, 0, 0)):
        self.x = random.randint(10, 590)
        self.y = random.randint(40, 200)
        self.speed = 0.01
        self.radius = 5
        self.color = color
        self.down = True
        self.left = True

    def move(self):
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

    def changeDirLR(self):
        self.left = not self.left

    def changeDirUD(self):
        self.down = not self.down
