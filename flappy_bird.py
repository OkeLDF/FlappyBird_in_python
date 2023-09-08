import pygame as pg
import time
import random as rd

# constantes
gravity = 0.9
jump = -10
hole_size = 200
obstacle_width = 80
bird_radius = 30

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

    def __init__(self, x: int, y: int, color='white'):
        self.coordinate = pg.Vector2(x,y)
        self.color = color

    def touching(self, obstacle:Obstacle):
        half_bird_radius = bird_radius / 2
        is_between_x1_and_x2 = self.coordinate.x + half_bird_radius > obstacle.x1 and self.coordinate.x < obstacle.x2
        is_between_y1_and_y2 = self.coordinate.y + half_bird_radius > obstacle.y1 and self.coordinate.y < obstacle.y2
        
        if is_between_x1_and_x2 and is_between_y1_and_y2:
            return True
        return False

pg.init()
running = True
screen = pg.display.set_mode((620, 720))
y_center = screen.get_height()/2
clock = pg.time.Clock()
pg.display.set_caption("Flappy Bird in Python")

#variáveis
bird_velocity = 0
x = 0
y = rd.choice(range(0,450))

bird = Player(310, y_center)

def new_game():
    global y
    global x
    global bird
    global bird_velocity
    y = rd.choice(range(0,450))
    x = 0
    bird.coordinate.y = y_center
    bird_velocity = 0

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    bird_velocity += gravity
    bird.coordinate.y += bird_velocity

    screen.fill('black')
    pg.draw.circle(screen, bird.color, bird.coordinate, bird_radius)

    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE]:
        bird_velocity = jump

    x -= 5

    obstacles = [
        Obstacle(screen.get_width() + x, 0, obstacle_width, y),
        Obstacle(screen.get_width() + x, y + hole_size, obstacle_width, screen.get_height())
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