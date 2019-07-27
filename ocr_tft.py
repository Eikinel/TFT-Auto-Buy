#!/usr/bin/env python3

from PIL import Image, ImageOps     # Image manipulation
import pyscreenshot                 # Screenshot tool, PIL friendly
import pyautogui                    # Mouse control
import pytesseract                  # OCR
import time
import sys
import re


def getChampions():
    file = open('champions.txt', 'r')
    champions = { c: c for c in file.read().split('\n') }
    file.close()

    return champions

def takeScreenshotROI(coordinates):
    # Take a screenshot of the champion zone only
    return pyscreenshot.grab(coordinates)

def transformImage(roi):
    # Convert image to grayscale and invert colors
    return ImageOps.invert(roi.convert('L'))

def main():
    # Set a timer of 0.5 second between each PyAutoGUI calls
    pyautogui.PAUSE = 0.5

    # Retrieve champions list
    allChampions = getChampions()
    selectedChampions = sys.argv[1:]
    print("Selected champions: ", selectedChampions)

    # Get screen's width/height
    width, height = pyautogui.size()

    # ROI factors of the champion zone starting top left
    left, top, right, bottom = (int(width * 0.25), int(height * 0.96), int(width * 0.77), int(height * 0.99))
    coordinates = (left, top, right, bottom)

    while (1):
        # Take a screenshot and apply transformations to pixels
        roi = transformImage(takeScreenshotROI(coordinates))

        # Handles text recognition using PyTesseract and get only correct champions
        availableChampions = [c for c in re.split(r'([A-Z][a-z]+)', pytesseract.image_to_string(roi)) if c and c in allChampions]
        print("Detected available champions: ", availableChampions)

        # Compare champions found and selected, then mouve mouse and click accordingly
        matches = set(availableChampions).intersection(selectedChampions)

        if matches:
            print("These champions are on your wishlist: ", matches)
            panelWidth, panelHeight = ((right - left) / 5, bottom - top)

            for match in matches:
                x, y = (int(left + panelWidth / 2 + (panelWidth * availableChampions.index(match))), int(top - panelHeight / 2))
                print("Moving mouse to location [", x, " ; ", y, "]")
                pyautogui.click(x, y)
        else:
            print("No matches found")
    
    return

if __name__ == "__main__":
    main()