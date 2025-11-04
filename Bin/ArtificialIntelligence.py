from PySide6.QtCore import QCoreApplication
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

## Load Font
try:
    font_path = resource_path(os.path.join("Data", "UI", "DinoFont.ttf"))
except pygame.error as e:
    print(f"Warning: Could not load font assets: {e}")

def draw_ai_network(win, net):
    if not hasattr(net, "node_evals"):
        return
    font = pygame.font.Font(None, 20)

    x_positions = { "input": 200, "hidden": 350, "output": 500 }
    nodeLabels = {
        -1: QCoreApplication.translate("ArtificialIntelligence", "DINO Y"),
        -2: QCoreApplication.translate("ArtificialIntelligence", "OBST X"),
        -3: QCoreApplication.translate("ArtificialIntelligence", "OBST Y"),
         0: QCoreApplication.translate("ArtificialIntelligence", "JUMP"),
         1: QCoreApplication.translate("ArtificialIntelligence", "DUCK")}
    layer_nodes = {"input": [-1, -2, -3], "output": [0, 1], "hidden": []}

    for nodeID, *_ in net.node_evals:
        if nodeID not in layer_nodes["output"]:
            layer_nodes["hidden"].append(nodeID)

    node_positions = {}
    y_spacing = 80
    for layer, nodes in layer_nodes.items():
        for i, node in enumerate(nodes):
            y = 100 + i * y_spacing
            x = x_positions[layer]
            node_positions[node] = (x, y)

    # Draw connections
    for nodeID, _, _, _, _, connections in net.node_evals:
        for inNode, weight in connections:
            if inNode in node_positions and nodeID in node_positions:
                start = node_positions[inNode]
                end = node_positions[nodeID]

                # Weight-based color and thickness
                intensity = min(255, int(50 + abs(weight) * 205))
                color = (0, 200, 0, intensity)
                thickness = max(1, int(abs(weight) * 3))

                pygame.draw.line(win, color[:3], start, end, thickness)

    # Draw nodes
    for node, pos in node_positions.items():
        if node in layer_nodes["input"]:
            color = (70, 130, 180)
        elif node in layer_nodes["output"]:
            color = (220, 20, 60)
        else:
            color = (128, 128, 128)

        pygame.draw.circle(win, (0, 0, 0), pos, 28)
        pygame.draw.circle(win, color, pos, 25)

        label = nodeLabels.get(node, str(node))
        text = font.render(label, True, (255, 255, 255))
        text_rect = text.get_rect(center=pos)
        win.blit(text, text_rect)

def load_high_score():
    try:
        with open(config.HIGHSCORE_AI_FILE, "r") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(score):
    with open(config.HIGHSCORE_AI_FILE, "w") as f:
        f.write(str(int(score)))

def runNeat():
    global WIN, stopTraining, errorCode, current_generation
    stopTraining = False
    errorCode = 0
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
    return errorCode

def main(genomes, neat_config):
    global WIN, stopTraining, errorCode, current_generation
    winWidth = config.SETTINGS.get("window_width", 800)
    winHeight = config.SETTINGS.get("window_height", 400)
    Dino.load_dino_images("Day")
    Obstacles.load_obstacle_images("Day")
    Scenery.load_scenery_images("Day")

    pygame.display.set_caption(QCoreApplication.translate("ArtificialIntelligence", "Dino Game - AI"))
    icon_path = resource_path(os.path.join("Data", "UI", "icon.png"))

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
        ground.move(game_speed)
        ground.draw(WIN)
        for obstacle in obstacles:
            obstacle.move(game_speed)
            obstacle.draw(WIN)

        if not obstacles or obstacles[-1].x < winWidth - 200 - random.randint(150, 450):
            cactus_types = [Obstacles.Cactus, Obstacles.CactusBig]

            if score < config.SETTINGS["bird_spawn_score"] or config.SETTINGS["bird_spawn_score"] == -1:
                chosen_cactus = random.choice(cactus_types)
                obstacles.append(chosen_cactus(winWidth + random.randint(100, 300)))
            else:
                if random.randint(1, 3) == 1:
                    obstacles.append(Obstacles.Bird(winWidth + random.randint(100, 300)))
                else:
                    chosen_cactus = random.choice(cactus_types)
                    obstacles.append(chosen_cactus(winWidth + random.randint(100, 300)))
        
        obstacles = [ob for ob in obstacles if ob.x + ob.image.get_width() > 0]
        for i, dino in enumerate(dinos):
            dino.move()
            ge[i].fitness += 0.1
            closestObstacle = None
            obstacle_list = [ob for ob in obstacles if ob.x + ob.image.get_width() > dino.x]
            if obstacle_list:
                closestObstacle = min(obstacle_list, key=lambda ob: ob.x)
            if closestObstacle:
                try: output = nets[i].activate((dino.y, abs(dino.x - closestObstacle.x), closestObstacle.y))
                except Exception as error:
                    if "expected" and "inputs" in str(error).lower():
                        run = False
                        stopTraining = True
                        errorCode = 2
                        break
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
        try:
            font = pygame.font.Font(font_path, 12)
        except Exception as e:
            font = pygame.font.Font(None, 24)
        text_surface = font.render(score_text, True, black)
        WIN.blit(text_surface, (winWidth - text_surface.get_width() - 10, 10))
        gen_text = font.render(f"Gen: {current_generation+1}", True, black)
        WIN.blit(gen_text, (10, 10))
        alive_string = QCoreApplication.translate("ArtificialIntelligence", "Alive: {0}").format(len(dinos))
        alive_text = font.render(alive_string, True, black)
        WIN.blit(alive_text, (10, 30))
        pygame.display.update()

    if score > high_score:
        high_score = score
        save_high_score(high_score)