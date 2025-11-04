import os, pygame, random, sys

groundHeight = 370
cactus_base_img = None
cactus_big_base_img = None
bird_images = []

def resource_path(relativePath):
    try:
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, relativePath)

def load_obstacle_images(mode="Day"):
    global cactus_base_img, cactus_big_base_img, bird_images
    suffix = "_night" if mode == "Night" else ""
    
    try:
        cactus_base_img = pygame.image.load(resource_path(os.path.join("Data", f"cactus{suffix}.png")))
        cactus_big_base_img = pygame.image.load(resource_path(os.path.join("Data", f"cactusBig{suffix}.png")))
        bird_images = [
            pygame.image.load(resource_path(os.path.join("Data", f"bird1{suffix}.png"))),
            pygame.image.load(resource_path(os.path.join("Data", f"bird2{suffix}.png")))
        ]
    except pygame.error as e:
        print(f"Error loading obstacle images for {mode} mode: {e}. Falling back to Day mode.")
        ## Fallback
        cactus_base_img = pygame.image.load(resource_path(os.path.join("Data", "cactus.png")))
        cactus_big_base_img = pygame.image.load(resource_path(os.path.join("Data", "cactusBig.png")))
        bird_images = [
            pygame.image.load(resource_path(os.path.join("Data", "bird1.png"))),
            pygame.image.load(resource_path(os.path.join("Data", "bird2.png")))
        ]

## Cactus Class
class Cactus:
    def __init__(self, x):
        self.isBird = False
        scale = random.uniform(0.6, 1.0)
        x_location = random.uniform(0, 1.0)
        if cactus_base_img is None: load_obstacle_images()
        
        original_width, original_height = cactus_base_img.get_size()
        
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        
        self.image = pygame.transform.scale(cactus_base_img, (new_width, new_height))

        self.x = x + (200 * x_location)
        self.y = groundHeight - self.image.get_height()

    def move(self, speed):
        self.x -= speed

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def collide(self, dino):
        dinoMask = pygame.mask.from_surface(dino.image)
        cactusMask = pygame.mask.from_surface(self.image)
        offset = (self.x - dino.x, self.y - round(dino.dino_height))
        return dinoMask.overlap(cactusMask, offset) != None

## Big Cactus Class
class CactusBig:
    def __init__(self, x):
        self.isBird = False
        scale = random.uniform(0.6, 0.8)
        x_location = random.uniform(0, 1.0)
        if cactus_big_base_img is None: load_obstacle_images()

        original_width, original_height = cactus_big_base_img.get_size()
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        self.image = pygame.transform.scale(cactus_big_base_img, (new_width, new_height))
        
        self.x = x + (200 * x_location)
        self.y = groundHeight - self.image.get_height()

    def move(self, speed):
        self.x -= speed

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def collide(self, dino):
        dinoMask = pygame.mask.from_surface(dino.image)
        cactusMask = pygame.mask.from_surface(self.image)
        offset = (self.x - dino.x, self.y - round(dino.dino_height))
        return dinoMask.overlap(cactusMask, offset) != None

## Bird Class
class Bird:
    def __init__(self, x):
        self.isBird = True
        if not bird_images: load_obstacle_images()
        self.images = bird_images
        self.imageIndex = 0
        self.image = self.images[self.imageIndex]
        x_location = random.uniform(0, 1.0)
        self.x = x + (200 * x_location)
        self.y = random.choice([groundHeight - 100, groundHeight - 140, groundHeight - 200])

        self.flap_count = 0

    def move(self, speed):
        self.x -= speed
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
        offset = (self.x - dino.x, self.y - round(dino.dino_height))
        return dinoMask.overlap(birdMask, offset) != None