#!/usr/bin/env python3

from pynput.keyboard import Key

# Program states
isRunning = True
isPaused = True
maxCallsPerSecond = 1

def toggle():
    global isPaused

    isPaused = not isPaused
    print("\nProgram is now " + ("paused" if isPaused else "active") + "\n")

def stop():
    global isRunning

    print("\nShutdown\n")
    isRunning = False

shortcuts = {
    (Key.space,): toggle,
    (Key.ctrl, 'q'): stop
}

keys = {}

# Set relevant keyboard keys to default position (up)
for shortcut in shortcuts:
    for s in shortcut:
        keys[s] = False