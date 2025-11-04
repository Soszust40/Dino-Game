import os, pygame, random, sys

ground_img = None
cloud_img = None
groundHeight = 350

def resource_path(relativePath):
    try:
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, relativePath)

def load_scenery_images(mode="Day"):
    global ground_img, cloud_img
    suffix = "_night" if mode == "Night" else ""
    
    try:
        ground_img = pygame.image.load(resource_path(os.path.join("Data", f"ground{suffix}.png")))
        cloud_img = pygame.image.load(resource_path(os.path.join("Data", f"cloud{suffix}.png")))
    except pygame.error as e:
        print(f"Error loading scenery images for {mode} mode: {e}. Falling back to Day mode.")
        ## Fallback
        ground_img = pygame.image.load(resource_path(os.path.join("Data", "ground.png")))
        cloud_img = pygame.image.load(resource_path(os.path.join("Data", "cloud.png")))

class Ground:
    
    def __init__(self):
        if ground_img is None: 
            load_scenery_images()
        self.image = ground_img
        self.WIDTH = self.image.get_width()
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
        if cloud_img is None:
            load_scenery_images()
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