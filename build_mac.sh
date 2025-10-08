#!/bin/bash
python3 -m PyInstaller Bin/Dino_Game.py \
    --noconsole \
    --noconfirm \
    --hidden-import=ArtificialIntelligence \
    --hidden-import=config \
    --hidden-import=Dino \
    --hidden-import=Obstacles \
    --hidden-import=Player \
    --hidden-import=Scenery \
    --add-data "data:data"
