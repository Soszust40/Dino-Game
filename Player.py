import pygame
import random
import Dino
import Obstacles

# Game Variables
winWidth = 800
winHeight = 400
white = (255, 255, 255)
black = (0, 0, 0)
WIN = None

# Player Mode
def playerMode(show_menu_callback):
    global WIN
    if WIN is None:
        WIN = pygame.display.set_mode((winWidth, winHeight))

    clock = pygame.time.Clock()
    dino = Dino.Dino()
    obstacles = [Obstacles.Cactus(800)]
    run = True
    score = 0

    while run:
        clock.tick(min(30 + (score / 1000), 100))
        WIN.fill(white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()
                if event.key == pygame.K_DOWN:
                    dino.duck()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dino.unduck()

        # Move and draw obstacles
        for obstacle in obstacles:
            obstacle.move()
            obstacle.draw(WIN)

        # Make new obstacles
        if obstacles[-1].x < 500:
            if random.choice([True, False]):
                obstacles.append(Obstacles.Cactus(800 + random.randint(100, 300)))
            else:
                obstacles.append(Obstacles.Bird(800 + random.randint(100, 300)))

        obstacles = [ob for ob in obstacles if ob.x + ob.image.get_width() > 0]

        dino.move()
        dino.draw(WIN)

        for obstacle in obstacles:
            if obstacle.collide(dino):
                run = False

        score += 1

        # Scoreboard
        font = pygame.font.Font(None, 36)
        textSurface = font.render(f"Score: {score}", True, black)
        WIN.blit(textSurface, (winWidth - 150, 10))

        pygame.display.update()

    # Quit Game
    pygame.display.quit()
    WIN = None
    show_menu_callback()
