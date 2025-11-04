# Dino Game AI & Player Mode  

This project is a clone of the popular Google Chrome "No Internet" Dino game, featuring both an AI-powered mode and a manual player mode. The AI is trained using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm, allowing it to learn and improve its ability to navigate obstacles over multiple generations.  

This project serves as an introduction to AI-driven gameplay and evolutionary algorithms, demonstrating how machine learning techniques can be applied to classic games.

Release Date: October 9, 2025

Developer: [Simon Oszust](https://github.com/Soszust40)

Languages: English & Spanish

## Controls  
- **Play Game:** Starts the game in manual Player Mode.
  - **Controls:** Press **[Space]** or **[Up Arrow]** to jump. Press **[Down Arrow]** to duck. Press **[ESC]** to exit.
- **Run AI Mode:** Begins training the NEAT algorithm. The game will play itself, generation by generation.
  - **Controls:** Press **[ESC]** to stop the training and return to the main menu.
- **Settings:** Opens the settings menu to configure game and AI parameters.
- **Quit:** Exits the application.

[Settings Help](https://github.com/Soszust40/Dino-Game/wiki)

## Features  
- **AI Mode** – Uses NEAT to train an AI that learns to jump over obstacles and improve its survival time.  
- **Player Mode** – Allows users to play the game manually, replicating the experience of the original Google Dino game.  
- **Obstacle Avoidance** – The AI learns to recognize and react to obstacles such as cacti and birds.  
- **Neural Network Visualization** – Displays the AI's decision-making process in real time.  

## How It Works  
- The AI evolves over multiple generations, improving its performance based on a fitness scoring system.  
- The fitness function rewards survival time and penalizes collisions with obstacles.
- The AI has access to the dino's y position, X distance to next obstacle, and Y distance to next obstacle.
- Players can switch between AI mode and manual mode for different gameplay experiences.  

## Technologies Used  
- **Python**  
- **Pygame** for graphics and game mechanics.
- **PySide6 (Qt for Python)** for the main menu and settings UI.
- **NEAT-Python** for AI training and evolution.

## Requirements:

#### Supported Devices:

* **Storage**: 500 MB
* **Operating Systems**: Windows & MacOS

## Additional Information:

#### Permissions: 
* Read/write access to files on your device
