# BIBLIOTEKI PYTHONA
import math
import time

import pygame
from pygame.constants import *
import random


# Funkcje pozwalające rysować przezroczyste powierzchnie:
def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


# Koło
def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)


# Funkcja sprawdzająca kolizje między dwoma okrągłymi obiektami.
def checkCircleCollision(movingObject, staticObject):
    # Zapisanie potrzebnych danych do zmiennych.
    # Współrzędne obiektów;
    x1, y1 = movingObject.x, movingObject.y
    x2, y2 = staticObject.x, staticObject.y

    # Promienie obiektów
    rad1 = movingObject.radius
    rad2 = staticObject.radius

    # Wykrywanie kolizji na podstawie twierdzenia Pitagorasa.
    return (x1 - x2) ** 2 + (y1 - y2) ** 2 < (rad1 + rad2) ** 2


# Funkcja, która sprawia, że dwa obiekty (koliste) nie nachodzą na siebie;

def solve_collision_static(dynamic, static):
    diff_x = dynamic.x - static.x
    diff_y = dynamic.y - static.y

    distance = (diff_x ** 2 + diff_y ** 2) ** 0.5 + 0.00000001

    normalized = (diff_x / distance, diff_y / distance)
    delta = dynamic.radius + static.radius - distance
    dynamic.x += delta * normalized[0]
    dynamic.y += delta * normalized[1]


def solve_collision_dynamic(object1, object2):

    diff_x = object1.x - object2.x
    diff_y = object1.y - object2.y

    distance = (diff_x ** 2 + diff_y ** 2) ** 0.5 + 0.00000001

    normalized = (diff_x / distance, diff_y / distance)
    delta = object1.radius + object2.radius - distance
    object1.x += 0.5 * delta * normalized[0]
    object1.y += 0.5 * delta * normalized[1]

    object2.x -= 0.5 * delta * normalized[0]
    object2.y -= 0.5 * delta * normalized[1]


# Funkcja zwraca liczbę między minimum i maximum.
def mathClamp(number, minimum, maximum):
    return max(min(number, maximum), minimum)

# Wrzucasz wektor, zwracasz wektor długości 1.
def normalize(vector):
    vectorLength = (vector[0] ** 2 + vector[1] ** 2) ** (1 / 2) + 0.0001
    vectorToTargetNorm = (vector[0] / vectorLength, vector[1] / vectorLength)
    return vectorToTargetNorm


def draw_text(text, x, y, color):
    label = pygame.font.SysFont('chalkduster.ttf', 72).render(text, True, color)
    screen.blit(label, (x, y))


class Line:
    def __init__(self, startPoint, endPoint):
        self.startPoint = startPoint
        self.endPoint = endPoint
        x1, y1 = self.startPoint
        x2, y2 = self.endPoint
        self.a = y1 - y2
        self.b = x2 - x1
        self.c = y1 * (x1 - x2) + x1 * (y2 - y1)

    def checkIfIntersect(self, circle):
        isTouchingLine = ((self.a * circle.x + self.b * circle.y + self.c) ** 2) < (circle.radius ** 2) * (
                    (self.a ** 2) + (self.b ** 2))

        minX, maxX = min(self.startPoint[0], self.endPoint[0]), max(self.startPoint[0], self.endPoint[0])
        minY, maxY = min(self.startPoint[1], self.endPoint[1]), max(self.startPoint[1], self.endPoint[1])
        isBetween = (minX < circle.x < maxX) or (minY < circle.y < maxY)
        return isTouchingLine and isBetween

    def setNewPos(self, startPoint, endPoint):
        self.startPoint = startPoint
        self.endPoint = endPoint
        x1, y1 = self.startPoint
        x2, y2 = self.endPoint
        self.a = y1 - y2
        self.b = x2 - x1
        self.c = y1 * (x1 - x2) + x1 * (y2 - y1)

    def draw(self):
        x1, y1 = self.startPoint
        x2, y2 = self.endPoint
        pygame.draw.line(screen, (255, 0, 0), (x1 - offsetX, y1 - offsetY), (x2 - offsetX, y2 - offsetY))


# Klasa gracza
class Player:
    """Klasa gracza."""

    def __init__(self, x, y, moveSpeed, radius=20):
        self.x = x
        self.y = y
        self.moveSpeed = moveSpeed
        self.radius = radius
        self.pistol = Pistol(self, Bullet, 20, 2)
        self.isHidden = False
        self.trackPoint = Point(x, y)

    def update(self):
        self.pistol.update()
        if not self.isHidden:
            self.trackPoint.setPos((self.x, self.y))

    def draw(self):
        pygame.draw.circle(screen, (0, 0, 255), (self.x - offsetX, self.y - offsetY), self.radius)


# Klasa drzewa
class CoreTree:
    """Robię tę klasę osobno tylko po to, żeby pnie miały niezależne kolizje."""

    def __init__(self, x, y, radius=30):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self):
        pygame.draw.circle(screen, (160, 82, 45), (self.x - offsetX, self.y - offsetY), self.radius)


class Tree:
    """Po prostu drzewo, pod które można się schować."""

    def __init__(self, x, y, radius=120):
        self.x = x
        self.y = y
        self.isPlayerInside = False

        self.radius = radius
        self.core = CoreTree(self.x, self.y, 30)

    def draw(self):
        alphaChannel = 128 if self.isPlayerInside else 255

        if -2 * self.radius < self.x - offsetX < SCREEN_WIDTH + 2 * self.radius:
            if -2 * self.radius < self.y - offsetY < SCREEN_HEIGHT + 2 * self.radius:
                self.core.draw()
                draw_circle_alpha(screen, (0, 80, 0, alphaChannel), (self.x - offsetX, self.y - offsetY), self.radius)


class Enemy:
    """Klasa przeciwnika, który chodzi dokładnie za nami i nas ściga."""

    def __init__(self, x, y, speed=1):
        self.x = x
        self.y = y
        self.target = Point(x, y)
        self.radius = 20
        self.speed = speed
        self.bulletParticles = []
        self.line = Line((0, 0), (0, 0))
        self.isSeeingTarget = False

    def move(self):
        """Wróg porusza się w stronę celu."""

        vectorToTargetNorm = normalize((self.target.x - self.x, self.target.y - self.y))
        self.x += vectorToTargetNorm[0] * self.speed
        self.y += vectorToTargetNorm[1] * self.speed

    def draw(self):
        """Rysujemy pocisk"""
        if -self.radius < self.x - offsetX < SCREEN_WIDTH + self.radius:
            if -self.radius < self.y - offsetY < SCREEN_HEIGHT + self.radius:
                pygame.draw.circle(screen, (255, 0, 0), (self.x - offsetX, self.y - offsetY), self.radius)


class Bullet:
    """Klasa pocisku, którym może strzelać gracz."""

    def __init__(self, x, y, direction, speed=3, maxLifeTime=5.):
        self.x = x
        self.y = y
        self.radius = 4
        self.direction = direction
        self.speed = speed
        self.maxLifeTime = maxLifeTime
        self.startLifetime = time.time()

    def move(self):
        """Pociski poruszają się w stronę wyznaczoną przez zmienną direction i usuwają, kiedy przekroczymy czas życia"""
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

        if self.startLifetime + self.maxLifeTime < time.time():
            del self

    def draw(self):
        """Rysujemy przeciwnika"""
        if -self.radius < self.y - offsetY < SCREEN_HEIGHT +  self.radius:
            pygame.draw.circle(screen, (255, 255, 0), (self.x - offsetX, self.y - offsetY), self.radius)


class Pistol:
    def __init__(self, owner, bullet, clipsize=8, reloadTime=2):
        self.owner = owner
        self.bullet = bullet
        self.clipsize = clipsize
        self.bulletsInClip = self.clipsize
        self.reloadTime = reloadTime
        self.reloadStart = None

    def fire(self, target):
        if self.bulletsInClip > 0:
            self.bulletsInClip -= 1
            x, y = target
            bulletList.append(
                self.bullet(self.owner.x, self.owner.y,
                            normalize((x - (self.owner.x - offsetX), y - (self.owner.y - offsetY))), 20))

    def update(self):
        if self.reloadStart:
            if self.bulletsInClip == 0 and time.time() > self.reloadStart + self.reloadTime:
                self.bulletsInClip = self.clipsize
                self.reloadStart = None

    def reload(self):
        if self.bulletsInClip == 0:
            self.reloadStart = time.time()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def setPos(self, pos):
        self.x = pos[0]
        self.y = pos[1]


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


for i in range(100):
    randX = random.randint(-2000, 2000)
    randY = random.randint(-2000, 2000)
    randDiameter = random.randint(50, 100)
    tree = Tree(randX, randY, randDiameter)
    treeList.append(tree)

# Tworzenie przeciwników
for i in range(60):
    randX = random.randint(-2000, 2000)
    randY = random.randint(-2000, 2000)
    randDiameter = random.randint(100, 200)
    randSpeed = random.randint(1, 4)

    enemy = Enemy(randX, randY, randSpeed)
    enemyList.append(enemy)

pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

nextSpawnTime = time.time() + 4

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
    if keys[K_r]:
        player.pistol.reload()

    # Sterowanie kamerą:
    if player.x - offsetX > SCREEN_WIDTH - 300:
        offsetX += ((player.x - offsetX) - (SCREEN_WIDTH - 300)) / 20
    if player.x - offsetX < 300:
        offsetX += (player.x - offsetX - 300) / 20

    if player.y - offsetY > SCREEN_HEIGHT - 300:
        offsetY += ((player.y - offsetY) - (SCREEN_HEIGHT - 300)) / 20
    if player.y - offsetY < 300:
        offsetY += (player.y - offsetY - 300) / 20

    player.update()

    # Wykrywanie kolizji drzew
    player.isHidden = False
    for tree in treeList:
        tree.isPlayerInside = checkCircleCollision(player, tree)

        if checkCircleCollision(player, tree):
            player.isHidden = True

        if checkCircleCollision(player, tree.core):
            solve_collision_static(player, tree.core)

    # Akcje przeciwników
    for i, enemy in enumerate(enemyList[:-1]):
        enemy.move()
        enemy.line.setNewPos((player.x, player.y), (enemy.x, enemy.y))
        # Wykrywanie kolizji przeciwników
        if checkCircleCollision(player, enemy):
            solve_collision_dynamic(player, enemy)

        for secondEnemy in enemyList[i + 1:]:
            if enemy != secondEnemy:
                if checkCircleCollision(enemy, secondEnemy):
                    solve_collision_dynamic(enemy, secondEnemy)
        counter = 0
        enemy.isSeeingTarget = True
        for tree in treeList:
            if checkCircleCollision(enemy, tree.core):
                solve_collision_static(enemy, tree.core)


            if enemy.line.checkIfIntersect(tree):
                counter += 1
                enemy.isSeeingTarget = False

        if enemy.isSeeingTarget and not player.isHidden:
            enemy.target.setPos((player.x, player.y))


    for bullet in bulletList:
        bullet.move()

        for tree in treeList:
            if checkCircleCollision(bullet, tree.core):
                try:
                    bulletList.remove(bullet)
                except:
                    pass

        for enemy in enemyList:
            if checkCircleCollision(bullet, enemy):
                try:
                    bulletList.remove(bullet)
                    enemyList.remove(enemy)
                except:
                    pass
    # TWORZENIE PRZECIWNIKÓW:
    if time.time() > nextSpawnTime:
        nextSpawnTime += 4
        enemyList.append(Enemy(4000, random.randint(-2000, 2000), random.randint(1, 5)))

    # Bez tego nie wyjdziesz z gry
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                player.pistol.fire(pygame.mouse.get_pos())
                if player.pistol.bulletsInClip >= 0:
                    for enemy in enemyList:
                        enemy.target.setPos((player.x, player.y))

    # ================== RYSOWANIE OBIEKTÓW ====================
    screen.fill((0, 180, 0))
    player.draw()

    for enemy in enemyList:
        enemy.draw()
        # enemy.line.draw()
        # pygame.draw.circle(screen, (255, 100, 100), (enemy.target.x - offsetX, enemy.target.y - offsetY), 5)

    for bullet in bulletList:
        bullet.draw()

    for tree in treeList:
        tree.draw()

    newString = str(player.pistol.bulletsInClip) if player.pistol.reloadStart is None else "Reloading..."
    draw_text(newString, 10, 10, (255, 100, 0))

    draw_text(str(len(enemyList)), 10, 60, (255, 100, 0))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()

