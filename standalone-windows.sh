#!/usr/bin/bash

SCRIPT='ocr_tft.py'
NAME='Windows-TFT-Auto-Buy'
OWNER='eikinel'
SRC_DIR='dist'
DEST_DIR='Standalone'

sudo docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows:python3 "pip install -r requirements.txt && pyinstaller --onefile $SCRIPT --name=$NAME";

#sudo chown $OWNER:$OWNER dist/$NAME;
#echo "Owner set to $OWNER:$OWNER"

#sudo mv $SRC_DIR/$NAME $DEST_DIR;
#echo "Moved .exe file from $SRC_DIR/ to $DEST_DIR/"

#sudo rm -rf $SRC_DIR/ build/ __pycache__/ $NAME.spec;
#echo "Cleared unecessary folders & files"