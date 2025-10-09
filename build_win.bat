@echo off
python -m PyInstaller ^
    --noconsole ^
    --noconfirm ^
    --icon="Data/exeIcon.ico" ^
    --add-data "Data;Data" ^
    --add-data "Bin;Bin" ^
    Bin/Dino_Game.py