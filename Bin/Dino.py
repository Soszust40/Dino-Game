import os, pygame, sys

def resource_path(relativePath):
    try:
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, relativePath)

dinoRunImages = [pygame.image.load(resource_path(os.path.join("Data", "dinoRun1.png"))), pygame.image.load(resource_path(os.path.join("Data", "dinoRun2.png")))]
dinoDuckImages = [pygame.image.load(resource_path(os.path.join("Data", "dinoDuck1.png"))), pygame.image.load(resource_path(os.path.join("Data", "dinoDuck2.png")))]
dinoJumpImage = pygame.image.load(resource_path(os.path.join("Data", "dinoRun1.png")))
dinoDeadImage = pygame.image.load(resource_path(os.path.join("Data", "dino_dead.png")))
groundHeight = 370

## Dino Class
class Dino:
    def __init__(self, gravity=1.0):
        self.runImages = dinoRunImages
        self.duckImages = dinoDuckImages
        self.jumpImage = dinoJumpImage
        self.deadImage = dinoDeadImage

        self.image = self.runImages[0]
        self.x = 50
        self.y = groundHeight - self.image.get_height()
        self.velY = 0
        self.jumpForce = -19
        self.gravity = gravity
        self.isJumping = False
        self.isDucking = False
        self.is_dead = False
        self.runIndex = 0

    def jump(self):
        if not self.isJumping and not self.is_dead:
            self.velY = self.jumpForce
            self.isJumping = True
            return True
        return False

    def duck(self):
        if  not self.is_dead:
            self.isDucking = True

    def unduck(self):
        self.isDucking = False

    def die(self):
        self.is_dead = True

    def move(self):
        if self.is_dead:
            return

        if self.isJumping and self.isDucking:
            self.velY += self.gravity * 3 

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
        if self.is_dead:
            self.image = self.deadImage
        elif self.isJumping:
            self.image = self.jumpImage
        elif self.isDucking:
            if not self.isJumping:
                self.image = self.duckImages[self.runIndex // 5]
        else:
            self.image = self.runImages[self.runIndex // 5]

        win.blit(self.image, (self.x, self.y))