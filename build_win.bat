@echo off
python -m PyInstaller ^
    --noconsole ^
    --noconfirm ^
    --add-data "Data;Data" ^
    --add-data "Bin;Bin" ^
    Bin/Dino_Game.py