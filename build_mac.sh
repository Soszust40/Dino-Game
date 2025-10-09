#!/bin/bash
python3 -m PyInstaller Bin/Dino_Game.py \
    --noconsole \
    --noconfirm \
    --icon="Data/exeIcon.ico" \
    --add-data "Data:Data" \
    --add-data "Bin:Bin"

