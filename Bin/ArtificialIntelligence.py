import neat, os, pygame, random, sys
import Dino, Obstacles, Scenery, config

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
WIN = None
stopTraining = False
current_generation = 0

def resource_path(relativePath):
    try:
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, relativePath)

def draw_ai_network(win, net):
    nodePositions = { -1: (200, 60), -2: (200, 120), -3: (200, 180), 0: (350, 90), 1: (350, 150) }
    nodeLabels = { -1: "DINO Y", -2: "OBST X", -3: "OBST Y", 0: "JUMP", 1: "DUCK" }
    for node, pos in nodePositions.items():
        pygame.draw.circle(win, blue if node < 0 else red, pos, 30)
        font = pygame.font.Font(None, 18)
        label = font.render(nodeLabels[node], True, black)
        win.blit(label, (pos[0] - 20, pos[1] - 10))
    if hasattr(net, 'node_evals'):
        for nodeID, _, _, _, _, connections in net.node_evals:
            for inNode, weight in connections:
                if inNode in nodePositions and nodeID in nodePositions:
                    pygame.draw.line(WIN, black, nodePositions[inNode], nodePositions[nodeID], 2 if weight > 0 else 1)

def load_high_score():
    try:
        with open(config.HIGHSCORE_AI_FILE, "r") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(score):
    with open(config.HIGHSCORE_AI_FILE, "w") as f:
        f.write(str(int(score)))

def runNeat(show_menu_callback):
    global WIN, stopTraining, current_generation
    stopTraining = False
    config_path = config.NEAT_CONFIG_FILE
    neat_config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path
    )
    p = neat.Population(neat_config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    max_generations = config.SETTINGS.get("max_generations", 50)
    generation = 0
    while not stopTraining and generation < max_generations:
        current_generation = generation
        p.run(main, 1)
        generation += 1
    pygame.display.quit()
    WIN = None
    show_menu_callback()

def main(genomes, neat_config):
    global WIN, stopTraining, current_generation
    winWidth = config.SETTINGS.get("window_width", 800)
    winHeight = config.SETTINGS.get("window_height", 400)

    pygame.display.set_caption("Dino Game - AI")
    icon_path = resource_path(os.path.join("Data", "icon.png"))

    try:
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
    except Exception as e:
        print(f"Could not load icon: {e}")

    if WIN is None:
        WIN = pygame.display.set_mode((winWidth, winHeight))
    high_score = load_high_score()
    nets, ge, dinos = [], [], []
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, neat_config)
        nets.append(net)
        dinos.append(Dino.Dino(gravity=config.SETTINGS.get("gravity", 1.0)))
        g.fitness = 0
        ge.append(g)
    clock = pygame.time.Clock()
    ground = Scenery.Ground()
    clouds = Scenery.create_clouds(winWidth)
    obstacles = [Obstacles.Cactus(winWidth)]
    score = 0
    game_speed = config.SETTINGS.get("game_speed", 5)
    run = True
    while run and len(dinos) > 0:
        clock.tick(60)
        WIN.fill(white)
        
        if nets:
            draw_ai_network(WIN, nets[0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
                stopTraining = True
                break
        if not run:
            break
        for cloud in clouds:
            cloud.move()
            cloud.draw(WIN)
        ground.move(game_speed)
        ground.draw(WIN)
        for obstacle in obstacles:
            obstacle.move(game_speed)
            obstacle.draw(WIN)

        if not obstacles or obstacles[-1].x < winWidth - 200 - random.randint(150, 450):
            cactus_types = [Obstacles.Cactus, Obstacles.CactusBig]

            if score < config.SETTINGS["bird_spawn_score"]:
                chosen_cactus = random.choice(cactus_types)
                obstacles.append(chosen_cactus(winWidth + random.randint(100, 300)))
            else:
                if random.randint(1, 3) == 1:
                    obstacles.append(Obstacles.Bird(winWidth + random.randint(100, 300)))
                else:
                    chosen_cactus = random.choice(cactus_types)
                    obstacles.append(chosen_cactus(winWidth + random.randint(100, 300)))
        
        obstacles = [ob for ob in obstacles if ob.x + ob.image.get_width() > 0]
        clouds = [cloud for cloud in clouds if cloud.x + cloud.image.get_width() > 0]
        if len(clouds) < 5:
            clouds.append(Scenery.Cloud(winWidth + random.randint(50, 200), random.randint(50, 200)))
        for i, dino in enumerate(dinos):
            dino.move()
            ge[i].fitness += 0.1
            closestObstacle = None
            obstacle_list = [ob for ob in obstacles if ob.x + ob.image.get_width() > dino.x]
            if obstacle_list:
                closestObstacle = min(obstacle_list, key=lambda ob: ob.x)
            if closestObstacle:
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
            else:
                dino.unduck()
            dino.draw(WIN)
        score += 0.25
        if score > 0 and score % 100 == 0:
            game_speed = min(game_speed + 0.1, 15)

        score_text = f"HI {int(high_score):05d} {int(score):05d}"
        font = pygame.font.Font(None, 24)
        text_surface = font.render(score_text, True, black)
        WIN.blit(text_surface, (winWidth - text_surface.get_width() - 10, 10))
        gen_font = pygame.font.Font(None, 24)
        gen_text = gen_font.render(f"Gen: {current_generation+1}", True, black)
        WIN.blit(gen_text, (10, 10))
        pygame.display.update()

    if score > high_score:
        high_score = score
        save_high_score(high_score)