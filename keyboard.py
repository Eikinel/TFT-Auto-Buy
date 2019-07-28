#!/usr/bin/env python3

from pynput import keyboard  # Keyboard management
import config

def onKeyPressed(key):
    try:
        key = key.char
    except:
        pass

    if key in config.keys:
        config.keys[key] = True
        current = [k for k in config.keys if config.keys[k]]
        
        # Iterate through shortcuts keys and get if all pressed key match it
        ss = [s for s in config.shortcuts if set(s) == set(current)]
        [config.shortcuts[s]() for s in ss]

def onKeyReleased(key):
    try:
        key = key.char
    except:
        pass

    if key in config.keys:
        config.keys[key] = False


listener = keyboard.Listener(
    on_press=onKeyPressed,
    on_release=onKeyReleased)
listener.start()