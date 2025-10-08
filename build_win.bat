@echo off
python -m PyInstaller ^
    --noconsole ^
    --noconfirm ^
    --add-data "data;data" ^
    --add-data "ArtificialIntelligence.py;." ^
    --add-data "config.py;." ^
    --add-data "Dino.py;." ^
    --add-data "Obstacles.py;." ^
    --add-data "Player.py;." ^
    --add-data "Scenery.py;." ^
    Dino_Game.py