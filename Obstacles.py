import os, pygame, random

groundHeight = 350

try:
    cactus_base_img = pygame.image.load(os.path.join("data", "cactus.png"))
    cactus_big_base_img = pygame.image.load(os.path.join("data", "cactusBig.png"))
except pygame.error as e:
    print(f"Error loading cactus images: {e}")
    cactus_base_img = pygame.Surface((20, 40))
    cactus_big_base_img = pygame.Surface((40, 40))


# Cactus Class
class Cactus:
    def __init__(self, x):
        scale = random.uniform(0.6, 1.0)
        
        original_width, original_height = cactus_base_img.get_size()
        
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        
        self.image = pygame.transform.scale(cactus_base_img, (new_width, new_height))

        self.x = x
        self.y = groundHeight - self.image.get_height() + 20

    def move(self, speed):
        self.x -= speed

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def collide(self, dino):
        dinoMask = pygame.mask.from_surface(dino.image)
        cactusMask = pygame.mask.from_surface(self.image)
        offset = (self.x - dino.x, self.y - round(dino.y))
        return dinoMask.overlap(cactusMask, offset) != None

# Big Cactus Class
class CactusBig:
    def __init__(self, x):
        scale = random.uniform(0.6, 0.8)
        original_width, original_height = cactus_big_base_img.get_size()
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        self.image = pygame.transform.scale(cactus_big_base_img, (new_width, new_height))
        
        self.x = x
        self.y = groundHeight - self.image.get_height() + 20

    def move(self, speed):
        self.x -= speed

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
        self.y = random.choice([groundHeight - 100, groundHeight - 150, groundHeight - 60])
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
        offset = (self.x - dino.x, self.y - round(dino.y))
        return dinoMask.overlap(birdMask, offset) != None