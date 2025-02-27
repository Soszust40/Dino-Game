# Dino Class
import pygame
import os

# Game Variables
dinoRunImages = [pygame.image.load(os.path.join("data", "dinoRun1.png")), pygame.image.load(os.path.join("data", "dinoRun2.png"))]
dinoDuckImages = [pygame.image.load(os.path.join("data", "dinoDuck1.png")), pygame.image.load(os.path.join("data", "dinoDuck2.png"))]
dinoJumpImages = pygame.image.load(os.path.join("data", "dinoJump.png"))
groundHeight = 350

# Dino Class
class Dino:
    def __init__(self):
        self.runImages = dinoRunImages
        self.duckImages = dinoDuckImages
        self.jumpImages = dinoJumpImages
        self.image = self.runImages[0]
        self.x = 50
        self.y = groundHeight - self.image.get_height()
        self.velY = 0
        self.jumpForce = -18
        self.gravity = 1
        self.isJumping = False
        self.isDucking = False
        self.runIndex = 0

    def jump(self):
        if not self.isJumping:
            self.velY = self.jumpForce
            self.isJumping = True

    def duck(self):
        if not self.isJumping:
            self.isDucking = True

    def unduck(self):
        self.isDucking = False

    def move(self):
        self.velY += self.gravity
        self.y += self.velY

        if self.y >= groundHeight - self.image.get_height():
            self.y = groundHeight - self.image.get_height()
            self.velY = 0
            self.isJumping = False

        self.runIndex += 1
        if self.runIndex >= len(self.runImages) * 5:
            self.runIndex = 0

    def draw(self, win):
        if self.isJumping:
            self.image = self.jumpImages
        elif self.isDucking:
            self.image = self.duckImages[self.runIndex // 5]
        else:
            self.image = self.runImages[self.runIndex // 5]

        win.blit(self.image, (self.x, self.y))
