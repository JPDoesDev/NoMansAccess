"""
Quick tool to print out keystrokes to view what keys are "seen" as for reference in later key binding.
"""

import keyboard
import mouse

def on_key_event(event):
    print(f"Key pressed: {event.name}")

def on_mouse_event(event):
    if isinstance(event, mouse.ButtonEvent):
        if event.event_type == 'down':
            print(f"Mouse button pressed: {event.button}")

def main():
    print("Listening for keypresses and mouse button presses...")
    keyboard.hook(on_key_event)
    mouse.hook(on_mouse_event)
    keyboard.wait()

if __name__ == "__main__":
    main()
