#!/usr/bin/env python3

from PIL import Image, ImageOps # Image manipulation
from timeit import default_timer as timer   # Time management
import pyscreenshot             # Screenshot tool, PIL friendly
import pytesseract              # OCR
import pyautogui                # Mouse control
import keyboard                 # Keyboard management
import config                   # Config file
import sys
import re


def getChampions():
    file = open('champions.txt', 'r')
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
    # Retrieve champions list
    allChampions = getChampions()
    selectedChampions = sys.argv[1:]
    print("Selected champions: ", selectedChampions)

    # Get screen's width/height
    width, height = pyautogui.size()

    # ROI factors of the champion zone starting top left and individual champion panel size
    left, top, right, bottom = (int(width * 0.25), int(height * 0.96), int(width * 0.77), int(height * 0.99))
    coordinates = (left, top, right, bottom)
    panelWidth, panelHeight = ((right - left) / 5, bottom - top)

    end = 0
    tick = 0

    while config.isRunning:
        dt = timer() - end
        end = timer()
        tick = tick + dt

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