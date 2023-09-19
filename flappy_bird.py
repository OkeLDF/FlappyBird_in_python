import pygame as pg
import time
import random as rd

# constantes
gravity = 0.98
jump = -10

class Obstacle:
    superior_pillar = 0
    inferior_pillar = 0
    color = ''
    width = 0
    hole_size = 0

    def __init__(self, screen_x:float, screen_y:float, obstacle_width=80, hole_size=200, color='darkviolet'):
        self.color = color
        self.hole_size = hole_size
        self.width = obstacle_width
        self.superior_pillar = pg.Rect(screen_x, 0, obstacle_width, 0)
        self.inferior_pillar = pg.Rect(screen_x, hole_size, obstacle_width, screen_y)
    
    def addto_x(self, value:float):
        self.superior_pillar.left += value
        self.inferior_pillar.left += value

    def get_x(self):
        return self.get_pillars()[0].x
    
    def get_y(self):
        return self.get_pillars()[0].y

    def set_x(self, value:int):
        self.superior_pillar.left = value
        self.inferior_pillar.left = value

    def set_y(self, value:int):
        self.superior_pillar.update(self.superior_pillar.left, self.superior_pillar.top, self.superior_pillar.width, value)
        self.inferior_pillar.update(self.inferior_pillar.left, value + self.hole_size, self.inferior_pillar.width, self.inferior_pillar.height)

    def randomize_in_right(self, screen_width):
        self.set_x(screen_width)
        self.set_y(rd.choice(range(0,450)))

    def get_pillars(self):
        return [self.superior_pillar, self.inferior_pillar]

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.superior_pillar, 10)
        pg.draw.rect(screen, self.color, self.inferior_pillar, 10)

class Player:
    coordinate = 0
    color = ''
    radius = 0
    velocity = 0
    img = 0
    collision = 0

    def __init__(self, x: int, y: int):
        self.coordinate = pg.Vector2(x,y)
        self.img = pg.image.load('files/mug.png')
        self.collision = pg.Rect(self.coordinate.x - self.img.get_width()/2 + 10, self.coordinate.y - self.img.get_height()/2, 58, 76)
        self.velocity = 0

    def touching(self, obstacle:Obstacle):
        for pillar in obstacle.get_pillars():
            is_between_x1_and_x2 = self.coordinate.x + 29 > pillar.left and pillar.right > self.coordinate.x - 29
            is_between_y1_and_y2 = self.coordinate.y + 38 > pillar.top and pillar.bottom > self.coordinate.y - 38
        
            if is_between_x1_and_x2 and is_between_y1_and_y2:
                return True
        return False
    
    def draw(self, screen):
        screen.blit(self.img, pg.Vector2(self.coordinate.x - self.img.get_width()/2 - 8, self.coordinate.y - self.img.get_height()/2))
        #pg.draw.rect(screen, 'yellow', self.collision, 2)

pg.init()
screen = pg.display.set_mode((620, 720))
screen_y_center = screen.get_height()/2
clock = pg.time.Clock()
pg.display.set_caption("Flappy Bird in Python")
pg.display.set_icon(pg.image.load('files/flappy.ico'))

player = Player(310, screen_y_center)
obstacles = [
    Obstacle(screen.get_width(), screen.get_height()),
    Obstacle(screen.get_width(), screen.get_height())
]

score = 0
font = pg.font.Font('files/Grand9K Pixel.ttf', 100)
text = font.render(str(score), True, 'gray50', None)
TextRect = text.get_rect()
TextRect.center = (screen.get_width() / 2, 200)

def new_game(sleep_one_sec=True):
    if sleep_one_sec: time.sleep(1)

    global obstacles
    global player
    global score
    score = 0
    player.coordinate.y = screen_y_center
    player.velocity = 0
    obstacles[0].randomize_in_right(screen.get_width())
    obstacles[1].randomize_in_right(1.5 * screen.get_width() + 50)

new_game(False)
running = True
while running:
    # events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # gravity effects and obstacle movement
    player.velocity += gravity
    player.coordinate.y += player.velocity
    for obstacle in obstacles:
        obstacle.addto_x(-5)

    # keys
    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE]:
        player.velocity = jump

    # draws
    screen.fill('black')
    text = font.render(str(score), True, 'gray50', None)
    screen.blit(text, TextRect)
    
    player.draw(screen)
    obstacles[0].draw(screen)
    obstacles[1].draw(screen)
    pg.display.flip()

    # player's death
    for obstacle in obstacles:
        if player.touching(obstacle):
            new_game()
        
        if player.coordinate.x == obstacle.get_x():
            score += 1

    if player.coordinate.y < 0 or player.coordinate.y > 730:
        new_game()

    # obstacle in front again
    for obstacle in obstacles:
        if obstacle.superior_pillar.right < 0:
            obstacle.set_x(screen.get_width())
            obstacle.set_y(rd.choice(range(0,450)))

    clock.tick(60)

pg.quit()