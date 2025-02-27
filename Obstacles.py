import pygame
import os
import random

# Game Variables
groundHeight = 350

# Cactus Class
class Cactus:
    def __init__(self, x):
        self.image = pygame.image.load(os.path.join("data", "cactus.png"))
        self.x = x
        self.y = groundHeight - self.image.get_height()
        self.vel = 5

    def move(self):
        self.x -= self.vel

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def collide(self, dino):
        dinoMask = pygame.mask.from_surface(dino.image)
        cactusMask = pygame.mask.from_surface(self.image)
        offset = (self.x - dino.x, self.y - round(dino.y))
        return dinoMask.overlap(cactusMask, offset) != None

# Bird Class
class Bird:
    def __init__(self, x):
        self.images = [pygame.image.load(os.path.join("data", "bird1.png")), pygame.image.load(os.path.join("data", "bird2.png"))]
        self.imageIndex = 0
        self.image = self.images[self.imageIndex]
        self.x = x
        self.y = random.choice([groundHeight - 100, groundHeight - 150])
        self.vel = 7
        self.flap_count = 0

    def move(self):
        self.x -= self.vel
        self.flap_count += 1
        if self.flap_count >= 5:
            self.imageIndex = (self.imageIndex + 1) % len(self.images)
            self.image = self.images[self.imageIndex]
            self.flap_count = 0

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def collide(self, dino):
        dinoMask = pygame.mask.from_surface(dino.image)
        birdMask = pygame.mask.from_surface(self.image)
        offset = (self.x - dino.x, self.y - round(dino.y))
        return dinoMask.overlap(birdMask, offset) != None
