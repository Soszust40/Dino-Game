import neat
import pygame
import random
import Dino
import Obstacles

# Game Variables
winWidth = 800
winHeight = 600
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
WIN = None
stopTraining = False

def draw_ai_network(win, net):
    nodePositions = {
        -1: (200, 60),
        -2: (200, 120),
        -3: (200, 180),
        0: (350, 90),
        1: (350, 150)
    }
    
    nodeLabels = {
        -1: "DINO Y",
        -2: "OBST X",
        -3: "OBST Y",
        0: "JUMP",
        1: "DUCK"
    }
    
    for node, pos in nodePositions.items():
        pygame.draw.circle(win, blue if node < 0 else red, pos, 30)
        font = pygame.font.Font(None, 18)
        label = font.render(nodeLabels[node], True, black)
        win.blit(label, (pos[0] - 20, pos[1] - 10))
    
    for nodeID, _, _, _, _, connections in net.node_evals:
        for inNode, weight in connections:
            if inNode in nodePositions and nodeID in nodePositions:
                pygame.draw.line(WIN, black, nodePositions[inNode], nodePositions[nodeID], 2 if weight > 0 else 1)

# NEAT Config
def runNeat(show_menu_callback, configFile):
    global WIN, stopTraining

    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        configFile
    )

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    generation = 0
    while not stopTraining and generation < 50:
        p.run(main, 1)
        generation += 1

    pygame.display.quit()
    WIN = None
    show_menu_callback()

# Main Game Loop for AI
def main(genomes, config):
    global WIN, stopTraining
    if WIN is None:
        WIN = pygame.display.set_mode((winWidth, winHeight))

    nets = []
    ge = []
    dinos = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        dinos.append(Dino.Dino())
        g.fitness = 0
        ge.append(g)

    clock = pygame.time.Clock()
    obstacles = [Obstacles.Cactus(800)]
    score = 0
    run = True

    while run and len(dinos) > 0:
        clock.tick(30)
        WIN.fill(white)

        draw_ai_network(WIN, nets[0])

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
                stopTraining = True

        for obstacle in obstacles:
            obstacle.move()
            obstacle.draw(WIN)

        if obstacles[-1].x < 500:
            if random.choice([True, False]):
                obstacles.append(Obstacles.Cactus(800 + random.randint(100, 300)))
            else:
                obstacles.append(Obstacles.Bird(800 + random.randint(100, 300)))

        obstacles = [ob for ob in obstacles if ob.x + ob.image.get_width() > 0]

        for i, dino in enumerate(dinos):
            dino.move()
            ge[i].fitness += 0.1

            closestObstacle = obstacles[0]
            output = nets[i].activate((dino.y, abs(dino.x - closestObstacle.x), closestObstacle.y))

            if output[0] > 0.5:
                dino.jump()
            elif output[1] > 0.5:
                dino.duck()
            else:
                dino.unduck()

            if closestObstacle.collide(dino):
                ge[i].fitness -= 1
                dinos.pop(i)
                nets.pop(i)
                ge.pop(i)

            dino.draw(WIN)

        score += 1

        # Scoreboard
        font = pygame.font.Font(None, 36)
        textSurface = font.render(f"Score: {score}", True, black)
        WIN.blit(textSurface, (winWidth - 150, 10))

        pygame.display.update()
