# recorder.py

import json
from pynput import mouse, keyboard
import time

class Recorder:
    def __init__(self):
        self.mouse_listener = None
        self.keyboard_listener = None
        self.events = []
        self.recording = False

    def on_click(self, x, y, button, pressed):
        if self.recording:
            event = {'type': 'mouse', 'action': 'click', 'x': x, 'y': y, 'button': button.name, 'pressed': pressed, 'time': time.time()}
            self.events.append(event)

    def on_move(self, x, y):
        if self.recording:
            event = {'type': 'mouse', 'action': 'move', 'x': x, 'y': y, 'time': time.time()}
            self.events.append(event)

    def on_scroll(self, x, y, dx, dy):
        if self.recording:
            event = {'type': 'mouse', 'action': 'scroll', 'x': x, 'y': y, 'dx': dx, 'dy': dy, 'time': time.time()}
            self.events.append(event)

    def on_press(self, key):
        if self.recording:
            try:
                event = {'type': 'keyboard', 'action': 'press', 'key': key.char if hasattr(key, 'char') else key.name, 'time': time.time()}
                self.events.append(event)
            except AttributeError:
                # Special keys handling
                event = {'type': 'keyboard', 'action': 'press', 'key': str(key), 'time': time.time()}
                self.events.append(event)

    def on_release(self, key):
        if self.recording:
            try:
                event = {'type': 'keyboard', 'action': 'release', 'key': key.char if hasattr(key, 'char') else key.name, 'time': time.time()}
                self.events.append(event)
            except AttributeError:
                # Special keys handling
                event = {'type': 'keyboard', 'action': 'release', 'key': str(key), 'time': time.time()}
                self.events.append(event)

    def start(self):
        self.events = []
        self.recording = True
        self.mouse_listener = mouse.Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop(self):
        self.recording = False
        if self.mouse_listener is not None:
            self.mouse_listener.stop()
        if self.keyboard_listener is not None:
            self.keyboard_listener.stop()

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.events, f, default=self.serialize_event)

    def serialize_event(self, event):
        # Custom serialization function to handle non-serializable objects
        if isinstance(event['button'], mouse.Button):
            return event['button'].name
        elif isinstance(event['key'], keyboard.Key):
            return event['key'].name
        elif isinstance(event['key'], str):
            return event['key']  # Already a string, no need to modify
        else:
            raise TypeError(f"Object of type {type(event)} is not JSON serializable")

    def load(self, filename):
        with open(filename, 'r') as f:
            self.events = json.load(f)


class Player:
    def __init__(self):
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()
        self.events = []
        self.playing = False

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
                    if isinstance(event['key'], str):
                        self.keyboard_controller.press(keyboard.KeyCode[event['key']])
                    else:
                        self.keyboard_controller.press(event['key'])
                elif event['action'] == 'release':
                    if isinstance(event['key'], str):
                        self.keyboard_controller.release(keyboard.KeyCode[event['key']])
                    else:
                        self.keyboard_controller.release(event['key'])
        self.playing = False

    def stop(self):
        self.playing = False

    def load(self, filename):
        with open(filename, 'r') as f:
            self.events = json.load(f)
