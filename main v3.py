# BIBLIOTEKI PYTHONA
import math

import pygame
from pygame.constants import *
import random


# Funkcje pozwalające rysować przezroczyste powierzchnie:
def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


# Koło
def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

# Funkcja sprawdzająca kolizje między dwoma okrągłymi obiektami.
def checkCircleCollision(firstObject, staticObject):
    # Zapisanie potrzebnych danych do zmiennych.
    # Współrzędne obiektów;
    x1, y1 = firstObject.x, firstObject.y
    x2, y2 = staticObject.x, staticObject.y

    # Promienie obiektów
    rad1 = firstObject.radius
    rad2 = staticObject.radius

    # Wykrywanie kolizji na podstawie twierdzenia Pitagorasa.
    return (x1 - x2) ** 2 + (y1 - y2) ** 2 < (rad1 + rad2) ** 2


# Funkcja, która sprawia, że dwa obiekty (koliste) nie nachodzą na siebie;

def bounce(firstObject, secondObject):
    # Dane w osobnych zmiennychaw
    x1, y1 = firstObject.x, firstObject.y
    x2, y2 = secondObject.x, secondObject.y

    diam1 = firstObject.radius
    diam2 = secondObject.radius

    # Pozyskanie informacji o kącie wektora między dwoma punktami.
    angle = math.atan2(y2 - y1, x2 - x1)

    # Długości x i y wektora o długości sumy promieni oraz kącie wyliczonym wcześniej.
    dx = math.cos(angle) * (diam1 + diam2)
    dy = math.sin(angle) * (diam1 + diam2)

    # Ustawienie pierwszego obiektu z daleka od obiektu drugiego.
    firstObject.x = x2 - dx
    firstObject.y = y2 - dy


# Funkcja zwraca liczbę między minimum i maximum.
def mathClamp(number, minimum, maximum):
    return max(min(number, maximum), minimum)


# Wrzucasz wektor, zwracasz wektor długości 1.
def normalize(vector):
    vectorLength = (vector[0] ** 2 + vector[1] ** 2) ** (1 / 2)
    vectorToTargetNorm = (vector[0] / vectorLength, vector[1] / vectorLength)
    return vectorToTargetNorm


# Klasa gracza
class Player:
    """Klasa gracza."""

    def __init__(self, x, y, moveSpeed, radius=20):
        self.x = x
        self.y = y
        self.moveSpeed = moveSpeed
        self.radius = radius

    def draw(self):
        pygame.draw.circle(screen, (0, 0, 255), (self.x - offsetX, self.y - offsetY), self.radius)


# Klasa drzewa
class CoreTree:
    def __init__(self, x, y, radius=30):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self):
        pygame.draw.circle(screen, (160, 82, 45), (self.x - offsetX, self.y - offsetY), self.radius)


class Tree:
    def __init__(self, x, y, radius=120):
        self.x = x
        self.y = y
        self.isPlayerInside = False

        self.radius = radius
        self.core = CoreTree(self.x, self.y, 30)

    def draw(self):
        alphaChannel = 128 if self.isPlayerInside else 255

        if -100 < self.x - offsetX < SCREEN_WIDTH + 100:
            if -100 < self.y - offsetY < SCREEN_HEIGHT + 100:
                self.core.draw()
                draw_circle_alpha(screen, (0, 80, 0, alphaChannel), (self.x - offsetX, self.y - offsetY), self.radius)


class Enemy:
    """Klasa przeciwnika, który chodzi dokładnie za nami i nas ściga."""

    def __init__(self, x, y, target, speed=1):
        self.x = x
        self.y = y
        self.target = target
        self.radius = 20
        self.speed = speed

    def move(self):
        """Wróg porusza się w stronę celu."""
        vectorToTargetNorm = normalize((self.target.x - self.x, self.target.y - self.y))
        self.x += vectorToTargetNorm[0] * self.speed
        self.y += vectorToTargetNorm[1] * self.speed

    def draw(self):
        """Rysujemy przeciwnika"""
        pygame.draw.circle(screen, (255, 0, 0), (self.x - offsetX, self.y - offsetY), self.radius)


class Bullet:
    """Klasa pocisku, którym może strzelać gracz."""

    def __init__(self, x, y, direction, speed=3):
        self.x = x
        self.y = y
        self.radius = 4
        self.direction = direction
        self.speed = speed


    def move(self):

        """Wróg porusza się w stronę celu."""
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

    def draw(self):
        """Rysujemy przeciwnika"""
        pygame.draw.circle(screen, (255, 255, 0), (self.x - offsetX, self.y - offsetY), self.radius)

pygame.init()
FPS = 60

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

offsetX = offsetY = 0

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

# PLAYER:
player = Player(250, 250, 2)

treeList = []
enemyList = []

bulletList = []
# Tworzenie drzew
for i in range(300):
    randX = random.randint(-2000, 2000)
    randY = random.randint(-2000, 2000)
    randDiameter = random.randint(50, 100)
    tree = Tree(randX, randY, randDiameter)
    treeList.append(tree)

# Tworzenie przeciwników
for i in range(30):
    randX = random.randint(-2000, 2000)
    randY = random.randint(-2000, 2000)
    randDiameter = random.randint(100, 200)
    randSpeed = random.randint(1, 4)

    enemy = Enemy(randX, randY, player, randSpeed)
    enemyList.append(enemy)

pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

running = 1
while running:

    # Przechwytywanie pozycji gracza
    keys = pygame.key.get_pressed()
    if keys[K_w]:
        player.y -= player.moveSpeed
    if keys[K_s]:
        player.y += player.moveSpeed
    if keys[K_a]:
        player.x -= player.moveSpeed
    if keys[K_d]:
        player.x += player.moveSpeed



    # Zabezpieczanie gracza przed opuszczeniem obszaru;
    if player.x - offsetX > SCREEN_WIDTH - 300:
        offsetX += ((player.x - offsetX) - (SCREEN_WIDTH - 300)) / 20
    if player.x - offsetX < 300:
        offsetX += (player.x - offsetX - 300) / 20

    if player.y - offsetY > SCREEN_HEIGHT - 300:
        offsetY += ((player.y - offsetY) - (SCREEN_HEIGHT - 300)) / 20
    if player.y - offsetY < 300:
        offsetY += (player.y - offsetY - 300) / 20

    # Wykrywanie kolizji drzew
    for tree in treeList:
        tree.isPlayerInside = checkCircleCollision(player, tree)

        if checkCircleCollision(player, tree.core):
            bounce(player, tree.core)

    # Akcje przeciwników
    for enemy in enemyList:
        enemy.move()

        # Wykrywanie kolizji przeciwników
        if checkCircleCollision(player, enemy):
            bounce(enemy, player)

        for secondEnemy in enemyList:
            if enemy != secondEnemy:
                if checkCircleCollision(enemy, secondEnemy):
                    bounce(enemy, secondEnemy)

        for tree in treeList:
            if checkCircleCollision(enemy, tree.core):
                bounce(enemy, tree.core)

    for bullet in bulletList:
        bullet.move()

        for tree in treeList:
            if checkCircleCollision(bullet, tree.core):
                bulletList.remove(bullet)

        for enemy in enemyList:
            if checkCircleCollision(bullet, enemy):
                bulletList.remove(bullet)
                enemyList.remove(enemy)


    # Bez tego nie wyjdziesz z gry
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                bulletList.append(
                    Bullet(player.x, player.y, normalize((x - (player.x - offsetX), y - (player.y - offsetY))), 10))

    # ================== RYSOWANIE OBIEKTÓW ====================
    screen.fill((0, 180, 0))
    player.draw()

    for enemy in enemyList:
        enemy.draw()

    for tree in treeList:
        tree.draw()

    for bullet in bulletList:
        bullet.draw()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
