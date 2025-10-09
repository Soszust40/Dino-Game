#!/bin/bash

python3 -m PyInstaller Bin/Dino_Game.py \
    --name "Dino Game" \
    --noconfirm \
    --windowed \
    --icon="Data/exeIcon.icns" \
    --hidden-import=PySide6 \
    --hidden-import=PySide6.QtCore \
    --hidden-import=PySide6.QtGui \
    --hidden-import=PySide6.QtWidgets \
    --add-data "Data:Data"