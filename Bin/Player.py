from PySide6.QtCore import QCoreApplication
import os, pygame, random, sys
import Dino, Obstacles, Scenery, config
pygame.mixer.init()

WIN = None
restart_img_day = None
restart_img_night = None
restart_img = None
DAY_MODE = {
    "background": (255, 255, 255),
    "text": (0, 0, 0)
}
NIGHT_MODE = {
    "background": (20, 20, 20),
    "text": (255, 255, 255)
}

def resource_path(relativePath):
    try:
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, relativePath)

## Load UI Elements
try:
    font_path = resource_path(os.path.join("Data", "UI", "DinoFont.ttf"))
    restart_img_day = pygame.image.load(resource_path(os.path.join("Data", "UI", "restart_button.png")))
    restart_img_night = pygame.image.load(resource_path(os.path.join("Data", "UI", "restart_button_night.png")))
except pygame.error as e:
    restart_img_day = pygame.Surface((50,50), pygame.SRCALPHA)
    restart_img_night = restart_img_day
    print(f"Warning: Could not load image assets: {e}")

## Load Sounds
try:
    jump_sound = pygame.mixer.Sound(resource_path(os.path.join("Data", "Sound", "jump.wav")))
    die_sound = pygame.mixer.Sound(resource_path(os.path.join("Data", "Sound", "die.wav")))
    score_sound = pygame.mixer.Sound(resource_path(os.path.join("Data", "Sound", "point.wav")))
except pygame.error as e:
    print(f"Warning: Could not load sound assets: {e}")
    ## Create dummy sound objects if files are missing so the game doesn't crash
    jump_sound = die_sound = score_sound = pygame.mixer.Sound(buffer=b'')

def save_high_score(score):
    with open(config.HIGHSCORE_FILE, "w") as f:
        f.write(str(int(score)))

def load_high_score():
    try:
        with open(config.HIGHSCORE_FILE, "r") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0

def game_loop(show_menu_callback):
    global WIN, restart_img
    winWidth = config.SETTINGS["window_width"]
    winHeight = config.SETTINGS["window_height"]
    if WIN is None:
        WIN = pygame.display.set_mode((winWidth, winHeight))
    high_score = load_high_score()
    
    volume = config.SETTINGS.get("music_volume", 50) / 100.0
    jump_sound.set_volume(volume)
    die_sound.set_volume(volume)
    score_sound.set_volume(volume)

    pygame.display.set_caption(QCoreApplication.translate("Player", "Dino Game - Player"))
    icon_path = resource_path(os.path.join("Data", "UI", "icon.png"))

    try:
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
    except Exception as e:
        print(f"Could not load icon: {e}")

    run = True
    while run:
        game_over = False
        score = 0
        prev_score = 0
        game_speed = config.SETTINGS["game_speed"]
        current_mode_setting = config.SETTINGS.get("daylight_cycle", "Auto")
        
        if current_mode_setting == "Night":
            active_theme = NIGHT_MODE
            asset_mode = "Night"
        else:
            active_theme = DAY_MODE
            asset_mode = "Day"

        ## Images
        Dino.load_dino_images(asset_mode)
        Obstacles.load_obstacle_images(asset_mode)
        Scenery.load_scenery_images(asset_mode)
        restart_img = restart_img_day if asset_mode == "Day" else restart_img_night
        
        dino = Dino.Dino(gravity=config.SETTINGS["gravity"])
        ground = Scenery.Ground()
        clouds = Scenery.create_clouds(winWidth)
        obstacles = [Obstacles.Cactus(winWidth)]
        restart_button_rect = restart_img.get_rect(center=(winWidth // 2, winHeight // 2 + 20))
        clock = pygame.time.Clock()
        session_run = True
        while session_run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    session_run = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run = False
                    session_run = False
                
                if game_over:
                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                        session_run = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if restart_button_rect.collidepoint(event.pos):
                            session_run = False
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                            if dino.jump():
                                jump_sound.play()
                        if event.key == pygame.K_DOWN:
                            dino.duck()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            dino.unduck()

            if not game_over:
                score += 0.25
                
                current_score_int = int(score)
                if current_score_int > prev_score and current_score_int % 100 == 0:
                    score_sound.play()
                
                if current_mode_setting == "Auto":
                    if current_score_int > prev_score and current_score_int > 0:
                        day_duration = 700
                        night_duration = 200
                        cycle_length = day_duration + night_duration                       
                        score_in_cycle = current_score_int % cycle_length                       
                        needs_switch = False
                        
                        ## Check for Day or Night
                        if score_in_cycle == day_duration and asset_mode == "Day":
                            asset_mode = "Night"
                            active_theme = NIGHT_MODE
                            needs_switch = True
                        elif score_in_cycle == 0 and asset_mode == "Night":
                            asset_mode = "Day"
                            active_theme = DAY_MODE
                            needs_switch = True
                        
                        ## Reload Assets
                        if needs_switch:
                            Dino.load_dino_images(asset_mode)
                            Obstacles.load_obstacle_images(asset_mode)
                            Scenery.load_scenery_images(asset_mode)
                            restart_img = restart_img_day if asset_mode == "Day" else restart_img_night
                            dino.runImages = Dino.dinoRunImages
                            dino.duckImages = Dino.dinoDuckImages
                            dino.jumpImage = Dino.dinoJumpImage
                            dino.deadImage = Dino.dinoDeadImage
                            ground.image = Scenery.ground_img
                            for cloud in clouds:
                                cloud.image = Scenery.cloud_img

                prev_score = current_score_int

                if score > 0 and int(score) % 100 == 0:
                    game_speed = min(game_speed + 0.1, 15)
                
                dino.move()
                ground.move(game_speed)

                for cloud in clouds:
                    cloud.move()

                for obstacle in obstacles:
                    obstacle.move(game_speed)
                    if obstacle.collide(dino):
                        if not game_over:
                            die_sound.play()
                        game_over = True
                        dino.isDead = True
                        if score > high_score:
                            high_score = score
                            save_high_score(high_score)
                
                if not obstacles or obstacles[-1].x < winWidth - 200 - random.randint(150, 450):
                    cactus_types = [Obstacles.Cactus, Obstacles.CactusBig]
                    
                    if score < config.SETTINGS["bird_spawn_score"] or config.SETTINGS["bird_spawn_score"] == -1:
                        chosen_cactus = random.choice(cactus_types)
                        obstacles.append(chosen_cactus(winWidth + 50))
                    else:
                        if random.randint(1, 3) == 1:
                            obstacles.append(Obstacles.Bird(winWidth + 50))
                        else:
                            chosen_cactus = random.choice(cactus_types)
                            obstacles.append(chosen_cactus(winWidth + 50))
                
                obstacles = [ob for ob in obstacles if ob.x + ob.image.get_width() > 0]

                clouds = [cloud for cloud in clouds if cloud.x + cloud.image.get_width() > 0]
                if len(clouds) < 5:
                    clouds.append(Scenery.Cloud(winWidth + random.randint(50, 200), random.randint(50, 200)))
            
            ## Drawing
            WIN.fill(active_theme["background"])
            for cloud in clouds:
                cloud.draw(WIN)
            ground.draw(WIN)
            for obstacle in obstacles:
                obstacle.draw(WIN)
            dino.draw(WIN)

            score_text = f"HI {int(high_score):05d} {int(score):05d}"
            try:
                font = pygame.font.Font(font_path, 12)
            except Exception as e:
                font = pygame.font.Font(None, 24)
            text_surface = font.render(score_text, True, active_theme["text"])
            WIN.blit(text_surface, (winWidth - text_surface.get_width() - 10, 10))

            if game_over:
                game_over_text = QCoreApplication.translate("Player", "GAME OVER")
                try:
                    font = pygame.font.Font(font_path, 28)
                except Exception as e:
                    font = pygame.font.Font(None, 64)
                text_surface = font.render(game_over_text, True, active_theme["text"])
                
                text_rect = text_surface.get_rect(center=(winWidth // 2, winHeight // 2 - 50))
                
                if asset_mode == "Night":
                     pygame.draw.rect(WIN, active_theme["background"], text_rect.inflate(20, 10))

                WIN.blit(text_surface, text_rect)

                WIN.blit(restart_img, restart_button_rect)

            pygame.display.update()
    
    pygame.display.quit()
    WIN = None
    show_menu_callback()