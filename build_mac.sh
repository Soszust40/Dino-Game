#!/bin/bash
python3 -m PyInstaller Bin/Dino_Game.py \
    --noconsole \
    --noconfirm \
    --add-data "Data:Data" \
    --add-data "Bin:Bin"

