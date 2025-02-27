## Hangman Game - Oszust Industries
## Created on: 2-24-25 - Last update: 2-27-25
softwareVersion = "v1.0.0"
systemName, systemBuild = "Dino", "dev"

import pygame, os, sys, json
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QFormLayout, QSpinBox, QDoubleSpinBox, QMessageBox, QSlider, QComboBox
from PySide6.QtCore import Qt
import Player, ArtificialIntelligence

pygame.init()

# Game Variables
winWidth = 800
winHeight = 400
WIN = None
pygame.display.set_caption("Dino Game")

class StartMenu(QWidget):
    def __init__(self, stacked_widget, main_app):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.main_app = main_app
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Google Dino AI")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        play_button = QPushButton("Play Game")
        ai_button = QPushButton("Run AI Mode")
        settings_button = QPushButton("Settings")
        quit_button = QPushButton("Quit")

        play_button.clicked.connect(self.play_game)
        ai_button.clicked.connect(self.run_ai)
        settings_button.clicked.connect(self.open_settings)
        quit_button.clicked.connect(self.quit_game)

        layout.addWidget(title)
        layout.addWidget(play_button)
        layout.addWidget(ai_button)
        layout.addWidget(settings_button)
        layout.addWidget(quit_button)

        self.setLayout(layout)

    def play_game(self):
        self.main_app.hide()
        Player.playerMode(self.main_app.show)

    def run_ai(self):
        self.main_app.hide()
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'neat-config.txt')
        ArtificialIntelligence.runNeat(self.main_app.show, config_path)

    def open_settings(self):
        self.stacked_widget.setCurrentIndex(1)

    def quit_game(self):
        pygame.quit()
        quit()

class SettingsMenu(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        layout = QVBoxLayout()

        # Game Settings
        game_layout = QFormLayout()
        game_title = QLabel("Game Settings")
        game_title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.window_width = QSpinBox()
        self.window_width.setRange(400, 1920)
        self.window_width.setValue(800)

        self.window_height = QSpinBox()
        self.window_height.setRange(300, 1080)
        self.window_height.setValue(600)

        self.music_volume = QSlider(Qt.Horizontal)
        self.music_volume.setRange(0, 100)
        self.music_volume.setValue(50)

        self.theme_mode = QComboBox()
        self.theme_mode.addItems(["Light", "Dark"])

        self.game_speed = QSpinBox()
        self.game_speed.setRange(1, 20)
        self.game_speed.setValue(5)

        self.gravity = QDoubleSpinBox()
        self.gravity.setRange(0.1, 5.0)
        self.gravity.setSingleStep(0.1)
        self.gravity.setValue(1.0)

        game_layout.addRow("Window Width:", self.window_width)
        game_layout.addRow("Window Height:", self.window_height)
        game_layout.addRow("Music Volume:", self.music_volume)
        game_layout.addRow("Theme Mode:", self.theme_mode)
        game_layout.addRow("Game Speed:", self.game_speed)
        game_layout.addRow("Gravity:", self.gravity)

        # AI Settings
        ai_layout = QFormLayout()
        ai_title = QLabel("AI Settings")
        ai_title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.population_size = QSpinBox()
        self.population_size.setRange(10, 200)
        self.population_size.setValue(50)

        self.mutation_rate = QDoubleSpinBox()
        self.mutation_rate.setRange(0.0, 1.0)
        self.mutation_rate.setSingleStep(0.01)
        self.mutation_rate.setValue(0.8)

        self.fitness_threshold = QSpinBox()
        self.fitness_threshold.setRange(1, 10000)
        self.fitness_threshold.setValue(1000)

        self.activation_function = QComboBox()
        self.activation_function.addItems(["relu", "sigmoid", "tanh"])

        self.max_generations = QSpinBox()
        self.max_generations.setRange(1, 500)
        self.max_generations.setValue(50)

        ai_layout.addRow("Population Size:", self.population_size)
        ai_layout.addRow("Mutation Rate:", self.mutation_rate)
        ai_layout.addRow("Fitness Threshold:", self.fitness_threshold)
        ai_layout.addRow("Activation Function:", self.activation_function)
        ai_layout.addRow("Max Generations:", self.max_generations)

        # Buttons
        save_button = QPushButton("Save Settings")
        back_button = QPushButton("Back to Menu")

        save_button.clicked.connect(self.save_settings)
        back_button.clicked.connect(self.go_back)

        layout.addWidget(game_title)
        layout.addLayout(game_layout)
        layout.addWidget(ai_title)
        layout.addLayout(ai_layout)
        layout.addWidget(save_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def save_settings(self):
        # Game settings
        game_settings = {
            "window_width": self.window_width.value(),
            "window_height": self.window_height.value(),
            "music_volume": self.music_volume.value(),
            "theme_mode": self.theme_mode.currentText(),
            "game_speed": self.game_speed.value(),
            "gravity": self.gravity.value()
        }

        with open("settings.json", "w") as f:
            json.dump(game_settings, f, indent=4)

        # AI settings
        ai_settings = f"""[NEAT]
fitness_threshold = {self.fitness_threshold.value()}
population_size = {self.population_size.value()}
mutation_rate = {self.mutation_rate.value()}
activation_function = {self.activation_function.currentText()}
max_generations = {self.max_generations.value()}"""

        with open("neat-config.txt", "w") as f:
            f.write(ai_settings)

        QMessageBox.information(self, "Settings Saved", "Settings have been saved successfully.")

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                game_settings = json.load(f)
                self.window_width.setValue(game_settings.get("window_width", 800))
                self.window_height.setValue(game_settings.get("window_height", 600))
                self.music_volume.setValue(game_settings.get("music_volume", 50))
                self.theme_mode.setCurrentText(game_settings.get("theme_mode", "Light"))
                self.game_speed.setValue(game_settings.get("game_speed", 5))
                self.gravity.setValue(game_settings.get("gravity", 1.0))
        except FileNotFoundError:
            pass

    def go_back(self):
        self.stacked_widget.setCurrentIndex(0)

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Google Dino AI Menu")
        self.resize(400, 500)
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