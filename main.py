# TU SĄ BIBLIOTEKI PYTHONA
import pygame
from pygame.constants import *
import random


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)


class Player:
    def __init__(self, x, y, moveSpeed, diameter=20):
        self.x = x
        self.y = y
        self.moveSpeed = moveSpeed
        self.diameter = diameter

        self.rect = pygame.Rect(self.x - self.diameter / 2, self.y - self.diameter / 2, self.diameter, self.diameter)

    def update(self):
        self.rect = pygame.Rect(self.x - self.diameter / 2, self.y - self.diameter / 2, self.diameter, self.diameter)

    def draw(self):
        pygame.draw.circle(screen, (0, 0, 255), (self.x - offsetX, self.y - offsetY), self.diameter)


class Tree:
    def __init__(self, x, y, diameter=120):
        self.x = x
        self.y = y
        self.isPlayerInside = False

        self.diameter = diameter
        self.rect = pygame.Rect(self.x - self.diameter / 2, self.y - self.diameter / 2, self.diameter, self.diameter)

    def update(self):
        self.rect = pygame.Rect(self.x - self.diameter / 2, self.y - self.diameter / 2, self.diameter, self.diameter)



    def draw(self):
        alphaChannel = 128 if self.isPlayerInside else 255


        pygame.draw.circle(screen, (160,82,45), (self.x - offsetX, self.y - offsetY), 30)
        draw_circle_alpha(screen, (0, 80, 0, alphaChannel), (self.x - offsetX, self.y - offsetY), self.diameter/2)


pygame.init()
FPS = 60

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

offsetX = 0
offsetY = 0

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

# PLAYER:
player = Player(250, 250, 2)

treeList = []
for i in range(1000):
    randX = random.randint(-5000, 5000)
    randY = random.randint(-5000, 5000)
    randDiameter = random.randint(100, 200)
    tree = Tree(randX, randY, randDiameter)
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


    player.update()

    if player.x - offsetX > SCREEN_WIDTH - 300:
        offsetX += ((player.x - offsetX) - (SCREEN_WIDTH - 300))/20
    if player.x - offsetX < 300:
        offsetX += (player.x - offsetX - 300)/20

    if player.y - offsetY > SCREEN_HEIGHT - 300:
        offsetY += ((player.y - offsetY) - (SCREEN_HEIGHT - 300))/20
    if player.y - offsetY < 300:
        offsetY += (player.y - offsetY - 300)/20



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 180, 0))

    player.draw()

    for tree in treeList:
        tree.draw()
        tree.isPlayerInside = tree.rect.colliderect(player.rect)


    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
