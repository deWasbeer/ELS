## PrintKeyStroke.py

import keyboard

def key_handler(key_event):
    print(key_event.name, key_event.event_type)

keyboard.hook(key_handler)

while True: pass
