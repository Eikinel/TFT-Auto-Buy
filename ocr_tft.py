#!/usr/bin/env python3

from PIL import Image, ImageOps # Image manipulation
from timeit import default_timer as timer   # Time management
import pyscreenshot             # Screenshot tool, PIL friendly
import pytesseract              # OCR
import pyautogui                # Mouse control
import platform                # Behaviors control for each OS
import keyboard                 # Keyboard management
import config                   # Config file
import sys
import re


def getChampions():
    try:
        file = open('champions.txt', 'r')
    except FileNotFoundError:
        print("[ERROR] Cannot find 'champions.txt' file", file=sys.stderr)
        raise FileNotFoundError

    champions = [c for c in file.read().split('\n')]
    file.close()

    return champions

def takeScreenshotROI(coordinates):
    # Take a screenshot of the champion zone only
    return pyscreenshot.grab(coordinates, childprocess=False)

def transformImage(roi):
    # Convert image to grayscale and invert colors
    return ImageOps.invert(roi.convert('L'))


def main():
    os = platform.system()
    # Retrieve champions list
    try:
        allChampions = getChampions()
    except FileNotFoundError:
        return
    

    if os == "Windows":
        selectedChampions = [c for c in input("Select your champions (ex: Lissandra Garen Evelynn) > ").split(' ') if c]
        pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract"
    else:
        if len(sys.argv) < 2:
            print("Please provide at least one character. A list of characters is available on 'champions.txt' file.")
            return
        selectedChampions = sys.argv[1:]
    
    print("Selected champions: ", selectedChampions)

    # Get screen's width/height
    width, height = pyautogui.size()

    # ROI factors of the champion zone starting top left and individual champion panel size
    left, top, right, bottom = (int(width * 0.25), int(height * 0.96), int(width * 0.77), int(height * 0.99))
    coordinates = (left, top, right, bottom)
    panelWidth, panelHeight = ((right - left) / 5, bottom - top)

    # Time handling
    dt = end = tick = 0
    config.isRunning = True

    print("Starting main loop")

    # Main loop
    while config.isRunning:
        dt = timer() - end
        end = timer()
        tick = tick + dt

        # Process detection logic every maxCallsSeconds, as much
        if not config.isPaused and tick >= 1 / config.maxCallsPerSecond:
            tick = 0

            # Take a screenshot and apply transformations to pixels
            roi = transformImage(takeScreenshotROI(coordinates))

            # Handles text recognition using PyTesseract and get only correct champions
            availableChampions = [c for c in re.split(r'([A-Z][a-z]+)', pytesseract.image_to_string(roi)) if c and c in allChampions]
            print("Detected available champions: ", availableChampions)

            # Compare champions found and selected, then move mouse and click accordingly
            matches = set(availableChampions).intersection(selectedChampions)

            if matches:
                print("These champions are on your wishlist: ", matches)

                # Click on each matching panel
                for match in matches:
                    x, y = (int(left + panelWidth / 2 + (panelWidth * availableChampions.index(match))), int(top - panelHeight / 2))
                    print("Moving mouse to location [", x, " ; ", y, "]")
                    pyautogui.click(x, y)
            else:
                print("No matches found")

            print()

    return

if __name__ == "__main__":
    main()