## Dino Game - Oszust Industries
## Created on: 2-24-25 - Last update: 10-9-25
softwareVersion = "v1.0.0"
systemName, systemBuild = "Dino", "dist"

from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QFormLayout, QSpinBox, QDoubleSpinBox, QMessageBox, QSlider, QComboBox, QGroupBox, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon
import pygame, os, sys
import Player, ArtificialIntelligence, config
pygame.init()

def resource_path(relativePath):
    try:
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, relativePath)

class StartMenu(QWidget):
    def __init__(self, stacked_widget, main_app):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.main_app = main_app
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                background-color: #44475a;
                color: #f8f8f2;
                border: 2px solid #bd93f9;
                border-radius: 8px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #bd93f9;
                color: #282a36;
            }
            QPushButton:pressed {
                background-color: #ff79c6;
                border-color: #ff79c6;
            }
            QLabel#title_text {
                font-size: 48px; 
                font-weight: bold;
                color: #50fa7b;
                margin-bottom: 10px;
            }
            QLabel#score_text {
                font-size: 18px;
                color: #bd93f9;
                font-weight: bold;
            }
            QFrame#scoresFrame {
                border: 1px solid #44475a;
                border-radius: 8px;
                margin-top: 15px;
                padding: 10px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(50, 50, 50, 50)

        logo_label = QLabel()
        logo_path = resource_path(os.path.join("Data", "logo.png"))
        try:
            pixmap = QPixmap(logo_path)
            logo_label.setPixmap(pixmap.scaledToWidth(400, Qt.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignCenter)
        except Exception as e:
            print(f"Could not load logo.png: {e}")
            logo_label.setText("Dino Game")
            logo_label.setObjectName("title_text")
            logo_label.setAlignment(Qt.AlignCenter)

        ## Highscore Display
        self.player_score_label = QLabel()
        self.ai_score_label = QLabel()
        self.player_score_label.setAlignment(Qt.AlignCenter)
        self.ai_score_label.setAlignment(Qt.AlignCenter)
        self.player_score_label.setObjectName("score_text")
        self.ai_score_label.setObjectName("score_text")
        self.update_highscores()

        play_button = QPushButton("Play Game")
        ai_button = QPushButton("Run AI Mode")
        settings_button = QPushButton("Settings")
        quit_button = QPushButton("Quit")

        play_button.clicked.connect(self.play_game)
        ai_button.clicked.connect(self.run_ai)
        settings_button.clicked.connect(self.open_settings)
        quit_button.clicked.connect(self.quit_game)

        layout.addWidget(logo_label)
        layout.addWidget(self.player_score_label)
        layout.addWidget(self.ai_score_label)
        layout.addStretch()
        layout.addWidget(play_button)
        layout.addWidget(ai_button)
        layout.addWidget(settings_button)
        layout.addWidget(quit_button)
        layout.addStretch()

        self.setLayout(layout)

    def update_highscores(self):
        try:
            with open(config.HIGHSCORE_FILE, "r") as f:
                player_score = f.read().strip()
        except FileNotFoundError:
            player_score = "0"

        try:
            with open(config.HIGHSCORE_AI_FILE, "r") as f:
                ai_score = f.read().strip()
        except FileNotFoundError:
            ai_score = "0"

        self.player_score_label.setText(f"Player Highscore: {player_score}")
        self.ai_score_label.setText(f"AI Highscore: {ai_score}")

    def showEvent(self, event):
        self.update_highscores()
        super().showEvent(event)

    def play_game(self):
        self.main_app.hide()
        Player.game_loop(self.main_app.show)

    def run_ai(self):
        self.main_app.hide()
        ArtificialIntelligence.runNeat(self.main_app.show)

    def open_settings(self):
        self.stacked_widget.setCurrentIndex(1)

    def quit_game(self):
        pygame.quit()
        sys.exit()

class SettingsMenu(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        game_group = QGroupBox("Game Settings")
        game_layout = QFormLayout()
        self.window_width = QSpinBox(); self.window_width.setRange(200, 3840)
        self.window_height = QSpinBox(); self.window_height.setRange(100, 2160)
        self.music_volume = QSlider(Qt.Horizontal)
        self.game_speed = QSpinBox(); self.game_speed.setRange(1, 20)
        self.gravity = QDoubleSpinBox(); self.gravity.setRange(0.1, 5.0); self.gravity.setSingleStep(0.1)
        self.bird_spawn_score = QSpinBox(); self.bird_spawn_score.setRange(0, 1000)
        game_layout.addRow("Window Width:", self.window_width)
        game_layout.addRow("Window Height:", self.window_height)
        game_layout.addRow("Music Volume:", self.music_volume)
        game_layout.addRow("Initial Game Speed:", self.game_speed)
        game_layout.addRow("Dino Gravity:", self.gravity)
        game_layout.addRow("Bird Spawn Score:", self.bird_spawn_score)
        game_group.setLayout(game_layout)

        ai_group = QGroupBox("AI Settings (NEAT)")
        ai_layout = QFormLayout()
        self.population_size = QSpinBox(); self.population_size.setRange(10, 500)
        self.fitness_threshold = QSpinBox(); self.fitness_threshold.setRange(1, 100000)
        self.max_generations = QSpinBox(); self.max_generations.setRange(1, 1000)
        self.reset_on_extinction = QComboBox(); self.reset_on_extinction.addItems(["True", "False"])
        self.activation_function = QComboBox(); self.activation_function.addItems(["relu", "sigmoid", "tanh", "gauss"])
        self.mutation_rate = QDoubleSpinBox(); self.mutation_rate.setRange(0.0, 1.0); self.mutation_rate.setSingleStep(0.01)
        self.compatibility_threshold = QDoubleSpinBox(); self.compatibility_threshold.setRange(0.1, 10.0); self.compatibility_threshold.setSingleStep(0.1)
        self.max_stagnation = QSpinBox(); self.max_stagnation.setRange(1, 100)
        self.survival_threshold = QDoubleSpinBox(); self.survival_threshold.setRange(0.01, 1.0); self.survival_threshold.setSingleStep(0.01)
        self.elitism = QSpinBox(); self.elitism.setRange(0, 100)
        ai_layout.addRow("Population Size:", self.population_size)
        ai_layout.addRow("Fitness Threshold:", self.fitness_threshold)
        ai_layout.addRow("Max Generations:", self.max_generations)
        ai_layout.addRow("Reset on Extinction:", self.reset_on_extinction)
        ai_layout.addRow("Activation Function:", self.activation_function)
        ai_layout.addRow("Weight Mutation Rate:", self.mutation_rate)
        ai_layout.addRow("Compatibility Threshold:", self.compatibility_threshold)
        ai_layout.addRow("Max Stagnation:", self.max_stagnation)
        ai_layout.addRow("Survival Threshold:", self.survival_threshold)
        ai_layout.addRow("Species Elitism:", self.elitism)
        ai_group.setLayout(ai_layout)

        top_button_layout = QHBoxLayout()
        bottom_button_layout = QHBoxLayout()

        save_button = QPushButton("Save Settings")
        restore_defaults_button = QPushButton("Restore Defaults")
        reset_scores_button = QPushButton("Reset High Scores")
        back_button = QPushButton("Back to Main Menu")

        
        top_button_layout.addWidget(restore_defaults_button)
        top_button_layout.addWidget(reset_scores_button)
        bottom_button_layout.addWidget(save_button)
        bottom_button_layout.addWidget(back_button)

        save_button.clicked.connect(self.save_settings)
        restore_defaults_button.clicked.connect(self.restore_defaults)
        reset_scores_button.clicked.connect(self.reset_scores)
        back_button.clicked.connect(self.go_back)

        main_layout.addWidget(game_group)
        main_layout.addWidget(ai_group)
        main_layout.addLayout(top_button_layout)
        main_layout.addLayout(bottom_button_layout)
        self.setLayout(main_layout)

    def restore_defaults(self):
        reply = QMessageBox.question(self, 'Restore Defaults', "Are you sure you want to restore all settings to their default values?\nThis won't be saved until you click 'Save Settings'.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            ## Restore Game Settings UI
            self.window_width.setValue(800)
            self.window_height.setValue(400)
            self.music_volume.setValue(50)
            self.game_speed.setValue(5)
            self.gravity.setValue(1.0)
            self.bird_spawn_score.setValue(300)
            
            ## Restore AI Settings UI
            self.population_size.setValue(50)
            self.fitness_threshold.setValue(10000)
            self.max_generations.setValue(50)
            self.reset_on_extinction.setCurrentText("True")
            self.activation_function.setCurrentText("relu")
            self.mutation_rate.setValue(0.8)
            self.compatibility_threshold.setValue(3.0)
            self.max_stagnation.setValue(15)
            self.survival_threshold.setValue(0.2)
            self.elitism.setValue(2)
            QMessageBox.information(self, "Defaults Restored", "Settings have been reset to default values. Click 'Save Settings' to apply them permanently.")

    def reset_scores(self):
        reply = QMessageBox.question(
            self,
            'Reset High Scores',
            "Are you sure you want to permanently reset both Player and AI high scores?\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                if os.path.exists(config.HIGHSCORE_FILE):
                    os.remove(config.HIGHSCORE_FILE)
                if os.path.exists(config.HIGHSCORE_AI_FILE):
                    os.remove(config.HIGHSCORE_AI_FILE)
                QMessageBox.information(self, "High Scores Reset", "Both Player and AI high scores have been deleted.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete high score files:\n{e}")

    def generate_neat_config(self):
        return  f"""[NEAT]
                    fitness_criterion     = max
                    fitness_threshold     = {self.fitness_threshold.value()}
                    pop_size              = {self.population_size.value()}
                    reset_on_extinction   = {self.reset_on_extinction.currentText()}
                    [DefaultGenome]
                    activation_default      = {self.activation_function.currentText()}
                    activation_mutate_rate  = 0.0
                    activation_options      = {self.activation_function.currentText()}
                    aggregation_default     = sum
                    aggregation_mutate_rate = 0.0
                    aggregation_options     = sum
                    bias_init_mean          = 0.0
                    bias_init_stdev         = 1.0
                    bias_max_value          = 30.0
                    bias_min_value          = -30.0
                    bias_mutate_power       = 0.5
                    bias_mutate_rate        = 0.7
                    bias_replace_rate       = 0.1
                    compatibility_disjoint_coefficient = 1.0
                    compatibility_weight_coefficient   = 0.5
                    conn_add_prob           = 0.5
                    conn_delete_prob        = 0.5
                    enabled_default         = True
                    enabled_mutate_rate     = 0.01
                    feed_forward            = True
                    initial_connection      = full
                    node_add_prob           = 0.2
                    node_delete_prob        = 0.2
                    num_hidden              = 0
                    num_inputs              = 3
                    num_outputs             = 2
                    response_init_mean      = 1.0
                    response_init_stdev     = 0.0
                    response_max_value      = 30.0
                    response_min_value      = -30.0
                    response_mutate_power   = 0.0
                    response_mutate_rate    = 0.0
                    response_replace_rate   = 0.0
                    weight_init_mean        = 0.0
                    weight_init_stdev       = 1.0
                    weight_max_value        = 30
                    weight_min_value        = -30
                    weight_mutate_power     = 0.5
                    weight_mutate_rate      = {self.mutation_rate.value()}
                    weight_replace_rate     = 0.1
                    [DefaultSpeciesSet]
                    compatibility_threshold = {self.compatibility_threshold.value()}
                    [DefaultStagnation]
                    species_fitness_func = max
                    max_stagnation       = {self.max_stagnation.value()}
                    species_elitism      = 2
                    [DefaultReproduction]
                    elitism               = {self.elitism.value()}
                    survival_threshold    = {self.survival_threshold.value()}
                    """

    def save_settings(self):
        config.SETTINGS["window_width"] = self.window_width.value()
        config.SETTINGS["window_height"] = self.window_height.value()
        config.SETTINGS["music_volume"] = self.music_volume.value()
        config.SETTINGS["game_speed"] = self.game_speed.value()
        config.SETTINGS["gravity"] = self.gravity.value()
        config.SETTINGS["max_generations"] = self.max_generations.value()
        config.SETTINGS["bird_spawn_score"] = self.bird_spawn_score.value()
        config.save_settings()
        neat_config_content = self.generate_neat_config()
        with open(config.NEAT_CONFIG_FILE, "w") as f:
            f.write(neat_config_content)
        QMessageBox.information(self, "Settings Saved", "Settings have been saved successfully.")

    def load_settings(self):
        self.window_width.setValue(config.SETTINGS.get("window_width", 800))
        self.window_height.setValue(config.SETTINGS.get("window_height", 400))
        self.music_volume.setValue(config.SETTINGS.get("music_volume", 50))
        self.game_speed.setValue(config.SETTINGS.get("game_speed", 5))
        self.gravity.setValue(config.SETTINGS.get("gravity", 1.0))
        self.max_generations.setValue(config.SETTINGS.get("max_generations", 50))
        self.bird_spawn_score.setValue(config.SETTINGS.get("bird_spawn_score", 300))

        if not os.path.exists(config.NEAT_CONFIG_FILE):
            neat_config_content = self.generate_neat_config()
            with open(config.NEAT_CONFIG_FILE, "w") as f:
                f.write(neat_config_content)
            print(f"Created default NEAT config at: {config.NEAT_CONFIG_FILE}")

        try:
            with open(config.NEAT_CONFIG_FILE, "r") as f:
                for line in f:
                    if '=' in line:
                        key, value = [x.strip() for x in line.split('=', 1)]
                        if key == 'pop_size': self.population_size.setValue(int(value))
                        elif key == 'fitness_threshold': self.fitness_threshold.setValue(int(value))
                        elif key == 'reset_on_extinction': self.reset_on_extinction.setCurrentText(value.capitalize())
                        elif key == 'activation_default': self.activation_function.setCurrentText(value)
                        elif key == 'weight_mutate_rate': self.mutation_rate.setValue(float(value))
                        elif key == 'compatibility_threshold': self.compatibility_threshold.setValue(float(value))
                        elif key == 'max_stagnation': self.max_stagnation.setValue(int(value))
                        elif key == 'survival_threshold': self.survival_threshold.setValue(float(value))
                        elif key == 'elitism': self.elitism.setValue(int(value))
        except Exception as e:
            print(f"Failed to load NEAT config: {e}")

    def go_back(self):
        self.stacked_widget.setCurrentIndex(0)

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(resource_path(os.path.join("Data", "icon.png"))))
        self.setWindowTitle("Google Dino AI Menu")
        self.resize(550, 600)
        self.stacked_widget = QStackedWidget()
        self.start_menu = StartMenu(self.stacked_widget, self)
        self.settings_menu = SettingsMenu(self.stacked_widget)
        self.stacked_widget.addWidget(self.start_menu)
        self.stacked_widget.addWidget(self.settings_menu)
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec())