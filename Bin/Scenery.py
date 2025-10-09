import os, pygame, random, sys

groundHeight = 350

def resource_path(relativePath):
    try:
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, relativePath)

ground_img = pygame.image.load(resource_path(os.path.join("Data", "ground.png")))
cloud_img = pygame.image.load(resource_path(os.path.join("Data", "cloud.png")))

class Ground:
    WIDTH = ground_img.get_width()
    
    def __init__(self):
        self.image = ground_img
        self.y = groundHeight
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self, speed):
        self.x1 -= speed
        self.x2 -= speed
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.image, (self.x1, self.y))
        win.blit(self.image, (self.x2, self.y))

class Cloud:
    def __init__(self, x, y):
        self.image = cloud_img
        self.x = x
        self.y = y
        self.vel = 1

    def move(self):
        self.x -= self.vel

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

def create_clouds(winWidth):
    clouds = []
    for _ in range(5):
        clouds.append(Cloud(random.randint(100, winWidth + 500), random.randint(50, 200)))
    return clouds