import pygame as pg
import time
import random as rd

class Obstacle:
    rect=0
    lefttop=0
    width_height=0
    x1=0
    y1=0
    x2=0
    y2=0
    width=0
    heigth=0

    def __init__(self, x:float, y:float, width:float, height:float):
        self.rect = pg.Rect(x, y, width, height)
        self.lefttop = pg.Vector2(x,y)
        self.width_height = pg.Vector2(width,height)
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.width=width
        self.heigth=height

class Player:
    coordinate = 0
    color = 'white'

    def __init__(self, x: int, y: int, color):
        self.coordinate = pg.Vector2(x,y)
        self.color = color

    def touching(self, obstacle:Obstacle):
        is_between_x1_and_x2 = self.coordinate.x+15 > obstacle.x1 and self.coordinate.x < obstacle.x2
        is_between_y1_and_y2 = self.coordinate.y+10 > obstacle.y1 and self.coordinate.y < obstacle.y2
        
        if is_between_x1_and_x2 and is_between_y1_and_y2:
            self.color='red'
            return True
        
        self.color='white'
        return False

pg.init()
running = True
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
pg.display.set_caption("Flappy Bird in Python")
bird = Player(500, screen.get_height()/2, 'white')

# constantes
gravity = 0.4
jump = -10
hole_size = 200
width = 50
y_center = screen.get_height()/2

#variáveis
velocity = 0
x = 0
y = rd.choice(range(0,450))

def new_game():
    global y
    global x
    global bird
    global velocity
    y = rd.choice(range(0,450))
    x = 0
    bird.coordinate.y = y_center
    velocity = 0

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill('black')
    pg.draw.circle(screen, bird.color, bird.coordinate, 20)

    velocity += gravity
    bird.coordinate.y += velocity

    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE]:
        velocity = jump

    x -= 5

    obstacles = [
        Obstacle(screen.get_width() + x, 0, width, y),
        Obstacle(screen.get_width() + x, y + hole_size, width, screen.get_height())
    ]
    pg.draw.rect(screen, 'purple', obstacles[0].rect, 10)
    pg.draw.rect(screen, 'purple', obstacles[1].rect, 10)

    if bird.touching(obstacles[0]) or bird.touching(obstacles[1]):
        time.sleep(1)
        new_game()
        #running = False

    if bird.coordinate.y < 0 or bird.coordinate.y > 730:
        time.sleep(1)
        new_game()
        #running = False

    if obstacles[0].x2 < 0:
        y = rd.choice(range(0,450))
        x = 0

    clock.tick(60)
    pg.display.flip()

pg.quit()