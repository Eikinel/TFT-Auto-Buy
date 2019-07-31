SCRIPT		=	ocr_tft.py
NAME		=	Windows-TFT-Auto-Buy
OWNER		=	eikinel
SRC_DIR		=	dist
DEST_DIR	=	Standalone

all: build clean

build:
	sudo docker run -v "$(shell pwd):/src/" cdrx/pyinstaller-windows:python3 "pip install -r requirements.txt && pyinstaller --onefile $(SCRIPT) --name=$(NAME)"
	sudo chown $(OWNER):$(OWNER) $(SRC_DIR)/$(NAME).exe
	sudo mv $(SRC_DIR)/$(NAME).exe $(DEST_DIR)

clean:
	sudo rm -rf $(SRC_DIR) build/ __pycache__ $(NAME).spec