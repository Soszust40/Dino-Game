import json, os, sys

APP_NAME = "Dino Game"
ORG_NAME = "Oszust Industries"

def get_app_data_dir():
    if sys.platform == 'win32': ## Windows
        return os.path.join(os.getenv('APPDATA'), ORG_NAME, APP_NAME)
    elif sys.platform == 'darwin': ## macOS
        return os.path.join(os.path.expanduser('~/Library/Application Support'), ORG_NAME, APP_NAME)
    else: ## Linux
        return os.path.join(os.path.expanduser('~'), '.local', 'share', ORG_NAME, APP_NAME)

APP_DATA_DIR = get_app_data_dir()

os.makedirs(APP_DATA_DIR, exist_ok=True)

## File PAths
SETTINGS_FILE = os.path.join(APP_DATA_DIR, "settings.json")
HIGHSCORE_FILE = os.path.join(APP_DATA_DIR, "highscorePlayer.txt")
HIGHSCORE_AI_FILE = os.path.join(APP_DATA_DIR, "highscoreAI.txt")
NEAT_CONFIG_FILE = os.path.join(APP_DATA_DIR, "neat-config.txt")

## Default Settings
SETTINGS = {
    "window_width": 800,
    "window_height": 400,
    "music_volume": 50,
    "daylight_cycle": "Auto",
    "game_speed": 5,
    "gravity": 1.0,
    "max_generations": 50,
    "bird_spawn_score": 300
}

def load_settings():
    global SETTINGS
    try:
        with open(SETTINGS_FILE, "r") as f:
            loaded_settings = json.load(f)
            SETTINGS.update(loaded_settings)
    except (FileNotFoundError, json.JSONDecodeError):
        save_settings()

def save_settings():
    with open(SETTINGS_FILE, "w") as f:
        json.dump(SETTINGS, f, indent=4)

load_settings()