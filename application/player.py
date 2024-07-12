# player.py

import json
from pynput import mouse, keyboard
import time

class Player:
    def __init__(self):
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()
        self.events = []
        self.playing = False

        # Mapping special key names to pynput key codes
        self.special_key_mapping = {
            'space': keyboard.Key.space,
            'esc': keyboard.Key.esc,
            'enter': keyboard.Key.enter,
            'backspace': keyboard.Key.backspace,
            'delete': keyboard.Key.delete,
            'f1': keyboard.Key.f1,
            'f2': keyboard.Key.f2,
            'f3': keyboard.Key.f3,
            'f4': keyboard.Key.f4,
            'f5': keyboard.Key.f5,
            'f6': keyboard.Key.f6,
            'f7': keyboard.Key.f7,
            'f8': keyboard.Key.f8,
            'f9': keyboard.Key.f9,
            'f10': keyboard.Key.f10,
            'f11': keyboard.Key.f11,
            'f12': keyboard.Key.f12,
            'print_screen': keyboard.Key.print_screen,
            'home': keyboard.Key.home,
            'tab': keyboard.Key.tab,
            'page_up': keyboard.Key.page_up,
            'page_down': keyboard.Key.page_down,
            'caps_lock': keyboard.Key.caps_lock,
            'shift': keyboard.Key.shift,
            'shift_r': keyboard.Key.shift_r,
            'end': keyboard.Key.end,
            'right': keyboard.Key.right,
            'down': keyboard.Key.down,
            'up': keyboard.Key.up,
            'left': keyboard.Key.left,
            'ctrl_r': keyboard.Key.ctrl_r,
            'alt_gr': keyboard.Key.alt_gr,
            'alt_l': keyboard.Key.alt_l,
            'cmd': keyboard.Key.cmd,
            'ctrl_l': keyboard.Key.ctrl_l,
            'insert': keyboard.Key.insert,
            # Add numpad keys
            'num_lock': keyboard.Key.num_lock,
        }

    def play(self, events):
        self.playing = True
        if not events:
            return

        start_time = events[0]['time']
        for event in events:
            if not self.playing:
                break
            elapsed = event['time'] - start_time
            time.sleep(elapsed)
            start_time = event['time']

            if event['type'] == 'mouse':
                if event['action'] == 'move':
                    self.mouse_controller.position = (event['x'], event['y'])
                elif event['action'] == 'click':
                    self.mouse_controller.position = (event['x'], event['y'])
                    if event['pressed']:
                        self.mouse_controller.press(mouse.Button[event['button']])
                    else:
                        self.mouse_controller.release(mouse.Button[event['button']])
                elif event['action'] == 'scroll':
                    self.mouse_controller.scroll(event['dx'], event['dy'])
            elif event['type'] == 'keyboard':
                if event['action'] == 'press':
                    key = event['key']
                    if key in self.special_key_mapping:
                        self.keyboard_controller.press(self.special_key_mapping[key])
                    elif len(key) == 1:
                        self.keyboard_controller.press(key)
                    else:
                        print(f"Invalid key character '{key}'")
                elif event['action'] == 'release':
                    key = event['key']
                    if key in self.special_key_mapping:
                        self.keyboard_controller.release(self.special_key_mapping[key])
                    elif len(key) == 1:
                        self.keyboard_controller.release(key)
                    else:
                        print(f"Invalid key character '{key}'")

        self.playing = False

    def stop(self):
        self.playing = False

    def load(self, filename):
        with open(filename, 'r') as f:
            self.events = json.load(f)
