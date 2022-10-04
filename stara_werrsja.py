import pygame
from pygame.constants import *
import random

class Player:
    def __init__(self, x, y, moveSpeed):
        self.x = x
        self.y = y
        self.moveSpeed = moveSpeed

    def draw(self):
        pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), 20)


class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.circle(screen, (0, 80, 0), (self.x, self.y), 60)


pygame.init()
FPS = 60

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

# PLAYER:
player = Player(250, 250, 2)

treeList = []
for i in range(30):
    randX = random.randint(50, SCREEN_WIDTH - 50)
    randY = random.randint(50, SCREEN_HEIGHT - 50)

    tree = Tree(randX, randY)
    treeList.append(tree)



running = True
while running:

    keys = pygame.key.get_pressed()
    if keys[K_w]:
        player.y -= player.moveSpeed
    if keys[K_s]:
        player.y += player.moveSpeed
    if keys[K_a]:
        player.x -= player.moveSpeed
    if keys[K_d]:
        player.x += player.moveSpeed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 180, 0))

    player.draw()

    for tree in treeList:
        tree.draw()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()