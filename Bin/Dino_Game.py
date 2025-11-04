## Dino Game - Oszust Industries
## Created on: 2-24-25 - Last update: 11-4-25
softwareVersion = "v1.1.0"
systemName, systemBuild = "Dino Game", "dist"

from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QFormLayout, QSpinBox, QDoubleSpinBox, QMessageBox, QSlider, QComboBox, QGroupBox, QHBoxLayout
from PySide6.QtCore import Qt, QEvent, QLocale, QTranslator, QUrl
from PySide6.QtGui import QDesktopServices, QPixmap, QIcon
import pygame, os, sys, requests
import Player, ArtificialIntelligence, config
translator = QTranslator()
pygame.init()

def resource_path(relativePath):
    try:
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, relativePath)

def set_language(app, language_code):
    app.removeTranslator(translator)
    lang_file = f"translations/app_{language_code}.qm"
    lang_path = resource_path(lang_file)
    
    if translator.load(lang_path):
        app.installTranslator(translator)
    else:
        if translator.load(lang_file):
            app.installTranslator(translator)
        else:
            print(f"Could not load translation file: {lang_file} or {lang_path}")

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

        self.logo_label = QLabel()
        logo_path = resource_path(os.path.join("Data", "UI", "logo.png"))
        try:
            pixmap = QPixmap(logo_path)
            self.logo_label.setPixmap(pixmap.scaledToWidth(400, Qt.SmoothTransformation))
            self.logo_label.setAlignment(Qt.AlignCenter)
        except Exception as e:
            print(f"Could not load logo.png: {e}")
            self.logo_label.setText(self.tr("Dino Game"))
            self.logo_label.setObjectName("title_text")
            self.logo_label.setAlignment(Qt.AlignCenter)

        ## Highscore Display
        self.player_score_label = QLabel()
        self.ai_score_label = QLabel()
        self.player_score_label.setAlignment(Qt.AlignCenter)
        self.ai_score_label.setAlignment(Qt.AlignCenter)
        self.player_score_label.setObjectName("score_text")
        self.ai_score_label.setObjectName("score_text")
        self.update_highscores()

        self.play_button = QPushButton(self.tr("Play Game"))
        self.ai_button = QPushButton(self.tr("Run AI Mode"))
        self.settings_button = QPushButton(self.tr("Settings"))
        self.quit_button = QPushButton(self.tr("Quit"))

        self.play_button.clicked.connect(self.play_game)
        self.ai_button.clicked.connect(self.run_ai)
        self.settings_button.clicked.connect(self.open_settings)
        self.quit_button.clicked.connect(self.quit_game)

        self.version_label = QLabel()
        self.version_label.setAlignment(Qt.AlignCenter)
        self.version_label.setObjectName("version_label")
        self.version_label.setText(softwareVersion)
        self.version_label.mousePressEvent = self.open_version_page

        ## Version Check Color
        self.update_version_color()

        self.play_button.setCursor(Qt.PointingHandCursor)
        self.ai_button.setCursor(Qt.PointingHandCursor)
        self.settings_button.setCursor(Qt.PointingHandCursor)
        self.quit_button.setCursor(Qt.PointingHandCursor)
        self.version_label.setCursor(Qt.PointingHandCursor)

        layout.addWidget(self.logo_label)
        layout.addWidget(self.player_score_label)
        layout.addWidget(self.ai_score_label)
        layout.addStretch()
        layout.addWidget(self.play_button)
        layout.addWidget(self.ai_button)
        layout.addWidget(self.settings_button)
        layout.addWidget(self.quit_button)
        layout.addWidget(self.version_label)
        layout.addStretch()

        self.setLayout(layout)

    def update_version_color(self):
        try:
            newestVersion = ((requests.get(f"https://api.github.com/repos/Soszust40/{systemName.replace(" ", "-")}/releases/latest")).json())['tag_name']
            color = "#ff5555" if newestVersion != softwareVersion else "#ffffff"
        except:
            color = "#888888"
        self.version_label.setStyleSheet(f"color: {color};")

    def open_version_page(self, event):
        QDesktopServices.openUrl(QUrl(f"https://github.com/Soszust40/{systemName.replace(" ", "-")}/releases"))
            
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

        self.player_score_label.setText(self.tr("Player Highscore: {0}").format(player_score))
        self.ai_score_label.setText(self.tr("AI Highscore: {0}").format(ai_score))

    def showEvent(self, event):
        self.update_highscores()
        super().showEvent(event)

    def play_game(self):
        self.main_app.hide()
        Player.game_loop(self.main_app.show)

    def run_ai(self):
        self.main_app.hide()
        if ArtificialIntelligence.runNeat() == 2:
            style_backup = self.styleSheet()
            self.setStyleSheet("")
            QMessageBox.critical(self, "Error", "The current settings caused a crash.\nPlease restore defaults in Settings and try again.", QMessageBox.Ok)
            self.setStyleSheet(style_backup)
        self.main_app.show()

    def open_settings(self):
        self.stacked_widget.setCurrentIndex(1)

    def quit_game(self):
        pygame.quit()
        sys.exit()

    ## Handle Language Change
    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslate_ui()
        super().changeEvent(event)

    def retranslate_ui(self):
        self.play_button.setText(self.tr("Play Game"))
        self.ai_button.setText(self.tr("Run AI Mode"))
        self.settings_button.setText(self.tr("Settings"))
        self.quit_button.setText(self.tr("Quit"))
        
        if not self.logo_label.pixmap():
             self.logo_label.setText(self.tr("Dino Game"))
        
        self.update_highscores()


class SettingsMenu(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        self.game_group = QGroupBox(self.tr("Game Settings"))
        self.game_layout = QFormLayout() 
        self.window_width = QSpinBox(); self.window_width.setRange(200, 3840)
        self.window_height = QSpinBox(); self.window_height.setRange(100, 2160)
        self.language = QComboBox()
        self.language.addItem(self.tr("English"), "English")
        self.language.addItem(self.tr("Spanish"), "Spanish")
        self.music_volume = QSlider(Qt.Horizontal)
        self.day_cycle = QComboBox()
        self.day_cycle.addItem(self.tr("Auto"), "Auto")
        self.day_cycle.addItem(self.tr("Day"), "Day")
        self.day_cycle.addItem(self.tr("Night"), "Night")
        self.game_speed = QSpinBox(); self.game_speed.setRange(1, 20)
        self.gravity = QDoubleSpinBox(); self.gravity.setRange(0.1, 5.0); self.gravity.setSingleStep(0.1)
        self.bird_spawn_score = QSpinBox(); self.bird_spawn_score.setRange(-1, 10000)
        window_size_layout = QHBoxLayout()
        window_size_layout.addWidget(self.window_width)
        window_size_layout.addWidget(self.window_height)
        
        self.game_layout.addRow(self.tr("Window Size:"), window_size_layout)
        self.game_layout.addRow(self.tr("Language:"), self.language)
        self.game_layout.addRow(self.tr("Music Volume:"), self.music_volume)
        self.game_layout.addRow(self.tr("Daylight Cycle:"), self.day_cycle)
        self.game_layout.addRow(self.tr("Initial Game Speed:"), self.game_speed)
        self.game_layout.addRow(self.tr("Dino Gravity:"), self.gravity)
        self.game_layout.addRow(self.tr("Bird Spawn Score:"), self.bird_spawn_score)
        self.game_group.setLayout(self.game_layout)

        self.ai_group = QGroupBox(self.tr("AI Settings (NEAT)"))
        self.ai_layout = QFormLayout()
        self.population_size = QSpinBox(); self.population_size.setRange(10, 500)
        self.fitness_threshold = QSpinBox(); self.fitness_threshold.setRange(1, 100000)
        self.max_generations = QSpinBox(); self.max_generations.setRange(1, 1000)
        self.reset_on_extinction = QComboBox()
        self.reset_on_extinction.addItem(self.tr("True"), "True")
        self.reset_on_extinction.addItem(self.tr("False"), "False")
        self.activation_function = QComboBox(); self.activation_function.addItems(["relu", "sigmoid", "tanh", "gauss"])
        self.mutation_rate = QDoubleSpinBox(); self.mutation_rate.setRange(0.0, 1.0); self.mutation_rate.setSingleStep(0.01)
        self.compatibility_threshold = QDoubleSpinBox(); self.compatibility_threshold.setRange(0.1, 10.0); self.compatibility_threshold.setSingleStep(0.1)
        self.max_stagnation = QSpinBox(); self.max_stagnation.setRange(1, 100)
        self.survival_threshold = QDoubleSpinBox(); self.survival_threshold.setRange(0.01, 1.0); self.survival_threshold.setSingleStep(0.01)
        self.elitism = QSpinBox(); self.elitism.setRange(0, 100)
        
        self.ai_layout.addRow(self.tr("Population Size:"), self.population_size)
        self.ai_layout.addRow(self.tr("Fitness Threshold:"), self.fitness_threshold)
        self.ai_layout.addRow(self.tr("Max Generations:"), self.max_generations)
        self.ai_layout.addRow(self.tr("Reset on Extinction:"), self.reset_on_extinction)
        self.ai_layout.addRow(self.tr("Activation Function:"), self.activation_function)
        self.ai_layout.addRow(self.tr("Weight Mutation Rate:"), self.mutation_rate)
        self.ai_layout.addRow(self.tr("Compatibility Threshold:"), self.compatibility_threshold)
        self.ai_layout.addRow(self.tr("Max Stagnation:"), self.max_stagnation)
        self.ai_layout.addRow(self.tr("Survival Threshold:"), self.survival_threshold)
        self.ai_layout.addRow(self.tr("Species Elitism:"), self.elitism)
        self.ai_group.setLayout(self.ai_layout)

        top_button_layout = QHBoxLayout()
        bottom_button_layout = QHBoxLayout()

        self.save_button = QPushButton(self.tr("Save Settings"))
        self.restore_defaults_button = QPushButton(self.tr("Restore Defaults"))
        self.reset_scores_button = QPushButton(self.tr("Reset High Scores"))
        self.back_button = QPushButton(self.tr("Back to Main Menu"))

        self.save_button.setCursor(Qt.PointingHandCursor)
        self.restore_defaults_button.setCursor(Qt.PointingHandCursor)
        self.reset_scores_button.setCursor(Qt.PointingHandCursor)
        self.back_button.setCursor(Qt.PointingHandCursor)

        top_button_layout.addWidget(self.restore_defaults_button)
        top_button_layout.addWidget(self.reset_scores_button)
        bottom_button_layout.addWidget(self.save_button)
        bottom_button_layout.addWidget(self.back_button)

        self.save_button.clicked.connect(self.save_settings)
        self.restore_defaults_button.clicked.connect(self.restore_defaults)
        self.reset_scores_button.clicked.connect(self.reset_scores)
        self.back_button.clicked.connect(self.go_back)

        main_layout.addWidget(self.game_group)
        main_layout.addWidget(self.ai_group)
        main_layout.addLayout(top_button_layout)
        main_layout.addLayout(bottom_button_layout)
        self.setLayout(main_layout)

    def change_language(self, lang_name):
        language_map = {
            "English": "en",
            "Spanish": "es",
        }
        lang_code = language_map.get(lang_name, "en")

        app = QApplication.instance()
        set_language(app, lang_code)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslate_ui()
        super().changeEvent(event)

    def retranslate_ui(self):
        self.game_group.setTitle(self.tr("Game Settings"))
        self.ai_group.setTitle(self.tr("AI Settings (NEAT)"))
    
        self.game_layout.itemAt(0, QFormLayout.LabelRole).widget().setText(self.tr("Window Size:"))
        self.game_layout.itemAt(1, QFormLayout.LabelRole).widget().setText(self.tr("Language:"))
        self.game_layout.itemAt(2, QFormLayout.LabelRole).widget().setText(self.tr("Music Volume:"))
        self.game_layout.itemAt(3, QFormLayout.LabelRole).widget().setText(self.tr("Daylight Cycle:"))
        self.game_layout.itemAt(4, QFormLayout.LabelRole).widget().setText(self.tr("Initial Game Speed:"))
        self.game_layout.itemAt(5, QFormLayout.LabelRole).widget().setText(self.tr("Dino Gravity:"))
        self.game_layout.itemAt(6, QFormLayout.LabelRole).widget().setText(self.tr("Bird Spawn Score:"))
    
        self.ai_layout.itemAt(0, QFormLayout.LabelRole).widget().setText(self.tr("Population Size:"))
        self.ai_layout.itemAt(1, QFormLayout.LabelRole).widget().setText(self.tr("Fitness Threshold:"))
        self.ai_layout.itemAt(2, QFormLayout.LabelRole).widget().setText(self.tr("Max Generations:"))
        self.ai_layout.itemAt(3, QFormLayout.LabelRole).widget().setText(self.tr("Reset on Extinction:"))
        self.ai_layout.itemAt(4, QFormLayout.LabelRole).widget().setText(self.tr("Activation Function:"))
        self.ai_layout.itemAt(5, QFormLayout.LabelRole).widget().setText(self.tr("Weight Mutation Rate:"))
        self.ai_layout.itemAt(6, QFormLayout.LabelRole).widget().setText(self.tr("Compatibility Threshold:"))
        self.ai_layout.itemAt(7, QFormLayout.LabelRole).widget().setText(self.tr("Max Stagnation:"))
        self.ai_layout.itemAt(8, QFormLayout.LabelRole).widget().setText(self.tr("Survival Threshold:"))
        self.ai_layout.itemAt(9, QFormLayout.LabelRole).widget().setText(self.tr("Species Elitism:"))

        self.save_button.setText(self.tr("Save Settings"))
        self.restore_defaults_button.setText(self.tr("Restore Defaults"))
        self.reset_scores_button.setText(self.tr("Reset High Scores"))
        self.back_button.setText(self.tr("Back to Main Menu"))

        current_lang_key = self.language.currentData()
        self.language.blockSignals(True)
        self.language.clear()
        self.language.addItem(self.tr("English"), "English")
        self.language.addItem(self.tr("Spanish"), "Spanish")
        
        index = self.language.findData(current_lang_key) 
        if index != -1:
            self.language.setCurrentIndex(index)
        
        self.language.blockSignals(False)

        current_daycycle_key = self.day_cycle.currentData()
        self.day_cycle.blockSignals(True)
        self.day_cycle.clear()
        self.day_cycle.addItem(self.tr("Day"), "Day")
        self.day_cycle.addItem(self.tr("Night"), "Night")
        self.day_cycle.addItem(self.tr("Auto"), "Auto")
        
        index = self.day_cycle.findData(current_daycycle_key)
        if index != -1:
            self.day_cycle.setCurrentIndex(index)
            
        self.day_cycle.blockSignals(False)

        current_reset_key = self.reset_on_extinction.currentData()
        self.reset_on_extinction.blockSignals(True) 
        self.reset_on_extinction.clear()
        self.reset_on_extinction.addItem(self.tr("True"), "True")
        self.reset_on_extinction.addItem(self.tr("False"), "False")
        
        index = self.reset_on_extinction.findData(current_reset_key)
        if index != -1:
            self.reset_on_extinction.setCurrentIndex(index)
            
        self.reset_on_extinction.blockSignals(False)

    def restore_defaults(self):
        reply = QMessageBox.question(self, 
            self.tr("Restore Defaults"), 
            self.tr("Are you sure you want to restore all settings to their default values?") + "\n" + self.tr("This won't be saved until you click 'Save Settings'."),
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.window_width.setValue(800)
            self.window_height.setValue(400)
            index = self.language.findData("English")
            if index != -1: self.language.setCurrentIndex(index)
            self.music_volume.setValue(50)
            index = self.day_cycle.findData("Auto")
            if index != -1: self.day_cycle.setCurrentIndex(index)
            self.game_speed.setValue(5)
            self.gravity.setValue(1.0)
            self.bird_spawn_score.setValue(300)
            
            self.population_size.setValue(50)
            self.fitness_threshold.setValue(10000)
            self.max_generations.setValue(50)
            index = self.reset_on_extinction.findData("True")
            if index != -1: self.reset_on_extinction.setCurrentIndex(index)
            self.activation_function.setCurrentText("relu")
            self.mutation_rate.setValue(0.8)
            self.compatibility_threshold.setValue(3.0)
            self.max_stagnation.setValue(15)
            self.survival_threshold.setValue(0.2)
            self.elitism.setValue(2)
            
            QMessageBox.information(self, 
                self.tr("Defaults Restored"), 
                self.tr("Settings have been reset to default values. Click 'Save Settings' to apply them permanently."))

    def reset_scores(self):
        reply = QMessageBox.question(
            self,
            self.tr('Reset High Scores'),
            self.tr("Are you sure you want to permanently reset both Player and AI high scores?") + "\n" + self.tr("This action cannot be undone."),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                if os.path.exists(config.HIGHSCORE_FILE):
                    os.remove(config.HIGHSCORE_FILE)
                if os.path.exists(config.HIGHSCORE_AI_FILE):
                    os.remove(config.HIGHSCORE_AI_FILE)
                QMessageBox.information(self, 
                    self.tr("High Scores Reset"), 
                    self.tr("Both Player and AI high scores have been deleted."))
            except Exception as e:
                QMessageBox.warning(self, 
                    self.tr("Error"), 
                    self.tr("Failed to delete high score files:\n{0}").format(e))

    def generate_neat_config(self):
        return f"""[NEAT]
                fitness_criterion     = max
                fitness_threshold     = {self.fitness_threshold.value()}
                pop_size              = {self.population_size.value()}
                reset_on_extinction   = {self.reset_on_extinction.currentData()}
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
                elitism              = {self.elitism.value()}
                survival_threshold   = {self.survival_threshold.value()}
                """

    def save_settings(self):
        config.SETTINGS["window_width"] = self.window_width.value()
        config.SETTINGS["window_height"] = self.window_height.value()
        config.SETTINGS["language"] = self.language.currentData()
        config.SETTINGS["music_volume"] = self.music_volume.value()
        config.SETTINGS["daylight_cycle"] = self.day_cycle.currentData()
        config.SETTINGS["game_speed"] = self.game_speed.value()
        config.SETTINGS["gravity"] = self.gravity.value()
        config.SETTINGS["max_generations"] = self.max_generations.value()
        config.SETTINGS["bird_spawn_score"] = self.bird_spawn_score.value()
        config.save_settings()

        lang_key = self.language.currentData()
        language_map = {
            "English": "en",
            "Spanish": "es",
        }
        lang_code = language_map.get(lang_key, "en")
        app = QApplication.instance()
        if app:
            set_language(app, lang_code)
        
        neat_config_content = self.generate_neat_config()
        with open(config.NEAT_CONFIG_FILE, "w") as f:
            f.write(neat_config_content)
                
        QMessageBox.information(self, 
            self.tr("Settings Saved"), 
            self.tr("Settings have been saved successfully."))

    def load_settings(self):
        lang_key = config.SETTINGS.get("language", "English")
        index = self.language.findData(lang_key)
        if index != -1:
            self.language.setCurrentIndex(index)

        daylight_key = config.SETTINGS.get("daylight_cycle", "Auto")
        daylight_index = self.day_cycle.findData(daylight_key)
        if daylight_index != -1:
            self.day_cycle.setCurrentIndex(daylight_index)

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
                        elif key == 'reset_on_extinction':
                            reset_key = value.capitalize()
                            reset_index = self.reset_on_extinction.findData(reset_key)
                            if reset_index != -1:
                                self.reset_on_extinction.setCurrentIndex(reset_index)
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
        self.setWindowIcon(QIcon(resource_path(os.path.join("Data", "UI", "icon.png"))))
        self.setWindowTitle(self.tr("Google Dino AI Menu"))
        self.resize(550, 600)
        
        self.stacked_widget = QStackedWidget()
        self.start_menu = StartMenu(self.stacked_widget, self)
        self.settings_menu = SettingsMenu(self.stacked_widget)
        
        self.stacked_widget.addWidget(self.start_menu)
        self.stacked_widget.addWidget(self.settings_menu)
        
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslate_ui()
        super().changeEvent(event)

    def retranslate_ui(self):
        self.setWindowTitle(self.tr("Google Dino AI Menu"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    try:
        config.load_settings() 
    except Exception as e:
        print(f"Could not load config: {e}. Using defaults.")

    language_name = config.SETTINGS.get("language", "English")
    language_map = {"English": "en", "Spanish": "es"}
    # & <Scripts_Path>\pyside6-lupdate.exe <path/to/python-script.py> -ts <path/to/translations/app_XX.ts>
    # & <Scripts_Path>\pyside6-lupdate.exe <path/to/python-script.py> <path/to/translations/app_XX.ts>
    # & <Scripts_Path>\pyside6-lupdate.exe <path/to/python-script.py> <path/to/translations/app_XX.ts> -qm <path/to/translations/app_XX.qm>
    lang_code = language_map.get(language_name)
    
    if not lang_code:
        system_locale = QLocale.system().name().split('_')[0]
        lang_code = system_locale

    set_language(app, lang_code)

    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec())