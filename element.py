import random

class Catcher(object):
    def __init__(self, color = (0, 0, 0)):
        self.x = 0
        self.y = 495
        self.width = 600
        self.height = 5
        self.speed = 50
        self.color = color

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
