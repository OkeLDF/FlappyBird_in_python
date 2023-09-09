import pygame as pg
import time
import random as rd

# constantes
gravity = 0.9
jump = -10
hole_size = 200
obstacle_width = 80

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
    color='purple'

    def __init__(self, x:float, y:float, width:float, height:float, color='purple'):
        self.rect = pg.Rect(x, y, width, height)
        self.lefttop = pg.Vector2(x,y)
        self.width_height = pg.Vector2(width,height)

        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

        self.width = width
        self.heigth = height
        self.color = color

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 10)

class Player:
    coordinate = 0
    color = 'white'
    radius = 0
    velocity = 0

    def __init__(self, x: int, y: int, radius:int, color='white'):
        self.coordinate = pg.Vector2(x,y)
        self.color = color
        self.radius = radius
        self.velocity = 0

    def touching(self, obstacle:Obstacle):
        is_between_x1_and_x2 = self.coordinate.x + self.radius > obstacle.x1 and self.coordinate.x - self.radius < obstacle.x2
        is_between_y1_and_y2 = self.coordinate.y + self.radius > obstacle.y1 and self.coordinate.y - self.radius < obstacle.y2
        
        if is_between_x1_and_x2 and is_between_y1_and_y2:
            return True
        return False
    
    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.coordinate, self.radius)

pg.init()
running = True
screen = pg.display.set_mode((620, 720))
y_center = screen.get_height()/2
clock = pg.time.Clock()
pg.display.set_caption("Flappy Bird in Python")

#variáveis
x = 0
y = rd.choice(range(0,450))

bird = Player(310, y_center, 30)

def new_game():
    global y
    global x
    global bird
    y = rd.choice(range(0,450))
    x = 0
    bird.coordinate.y = y_center
    bird.velocity = 0

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    bird.velocity += gravity
    bird.coordinate.y += bird.velocity
    x -= 5

    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE]:
        bird.velocity = jump

    obstacles = [
        Obstacle(screen.get_width() + x, 0, obstacle_width, y),
        Obstacle(screen.get_width() + x, y + hole_size, obstacle_width, screen.get_height())
    ]

    screen.fill('black')
    bird.draw(screen)
    obstacles[0].draw(screen)
    obstacles[1].draw(screen)
    pg.display.flip()

    for obstacle in obstacles:
        if bird.touching(obstacle):
            time.sleep(1)
            new_game()

    if bird.coordinate.y < 0 or bird.coordinate.y > 730:
        time.sleep(1)
        new_game()

    if obstacles[0].x2 < 0:
        y = rd.choice(range(0,450))
        x = 0

    clock.tick(60)

pg.quit()