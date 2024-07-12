import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os

from recorder import Recorder
from player import Player

class LWmacroApp:
    def __init__(self, root):
        self.root = root
        self.recorder = Recorder()
        self.player = Player()
        self.filename = "recording.rec"
        self.always_on_top = True
        self.draggable = True
        self.setup_gui()

    def setup_gui(self):
        self.root.title("LWmacro")
        self.root.geometry("700x400")
        self.root.configure(bg="#2c3e50")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", self.always_on_top)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"700x600+{screen_width - 700 - 20}+{screen_height - 500 - 200}")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", font=("Helvetica", 12), padding=10, background="#3498db", foreground="#fff", focuscolor="#2980b9", relief="flat", borderwidth=0)
        style.map("TButton", background=[("active", "#2980b9")])

        update_label = tk.Label(self.root, text="Version 2.0-beta.1", font=("Helvetica", 8), bg="#2c3e50", fg="#ecf0f1")
        update_label.place(relx=0.5, rely=0.0, anchor='n')

        title = tk.Label(self.root, text="LWmacro", font=("Helvetica", 16), bg="#2c3e50", fg="#ecf0f1")
        title.pack(pady=20)

        self.record_button = ttk.Button(self.root, text="Record", command=self.start_recording)
        self.record_button.pack(pady=10)

        self.new_file_button = ttk.Button(self.root, text="New File", command=self.create_new_file, width=10)
        self.new_file_button.pack(pady=10)

        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.play_button = ttk.Button(self.root, text="Play", command=self.play, state=tk.DISABLED)
        self.play_button.pack(pady=10)

        self.select_file_button = ttk.Button(self.root, text="Open File", command=self.select_file)
        self.select_file_button.pack(pady=10)

        self.rename_file_button = ttk.Button(self.root, text="Rename File", command=self.rename_file)
        self.rename_file_button.pack(pady=10)

        self.current_file_label = ttk.Label(self.root, text=f"Current File: {self.filename}", font=("Helvetica", 10), background="#2c3e50", foreground="#ecf0f1")
        self.current_file_label.pack(pady=10)

        self.open_file_location_button = ttk.Button(self.root, text="Open File Location", command=self.open_file_location)
        self.open_file_location_button.pack(pady=10)

        self.always_on_top_button = ttk.Button(self.root, text="Always on Top: On", command=self.toggle_always_on_top, width=15)
        self.always_on_top_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)

        self.lock_unlock_button = ttk.Button(self.root, text="Unlock", command=self.toggle_draggable)
        self.lock_unlock_button.place(relx=0.0, rely=0.0, anchor='nw', x=10, y=10)

        self.exit_button = ttk.Button(self.root, text="Exit", command=self.root.destroy)
        self.exit_button.pack(side=tk.BOTTOM, pady=10, fill=tk.X)

        self.changelog_button = ttk.Button(self.root, text="📜 Changelogs", command=self.show_changelogs)
        self.changelog_button.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

        self.credits_button = ttk.Button(self.root, text="Credits", command=self.show_credits)
        self.credits_button.place(relx=0.0, rely=1.0, anchor='sw', x=10, y=-10)

    def create_new_file(self):
        self.filename = "new_recording.rec"
        self.current_file_label.config(text=f"Current File: {self.filename}")
        messagebox.showinfo("Info", f"New file created: {self.filename}")

    def start_recording(self):
        self.record_button.state(['disabled'])
        self.stop_button.state(['!disabled'])
        self.play_button.state(['disabled'])
        threading.Thread(target=self.recorder.start).start()

    def stop(self):
        if self.recorder.recording:
            try:
                self.recorder.stop()
                self.recorder.save(self.filename)
                self.record_button.state(['!disabled'])
                self.stop_button.state(['disabled'])
                self.play_button.state(['!disabled'])
                messagebox.showinfo("Info", "Recording stopped and saved.")
            except Exception as e:
                self.show_warning(f"Error stopping the recording: {str(e)}")
        elif self.player.playing:
            try:
                self.player.stop()
                self.stop_button.state(['disabled'])
                self.play_button.state(['!disabled'])
            except Exception as e:
                self.show_warning(f"Error stopping the playback: {str(e)}")

    def play(self):
        try:
            self.player.load(self.filename)
            threading.Thread(target=self.play_macro).start()
        except Exception as e:
            self.show_warning(f"Failed to play recording from {self.filename}: {str(e)}")

    def play_macro(self):
        self.stop_button.state(['!disabled'])
        self.play_button.state(['disabled'])
        self.player.play(self.player.events)
        self.play_button.state(['!disabled'])

    def select_file(self):
        try:
            file_path = filedialog.askopenfilename(defaultextension=".rec",
                                                  filetypes=[("Recording files", "*.rec"), ("All files", "*.*")])
            if file_path:
                self.filename = file_path
                self.current_file_label.config(text=f"Current File: {self.filename}")
                self.play_button.state(['!disabled'])
        except Exception as e:
            self.show_warning(f"Failed to open file: {str(e)}")

    def rename_file(self):
        try:
            new_name = filedialog.asksaveasfilename(defaultextension=".rec",
                                                   filetypes=[("Recording files", "*.rec"), ("All files", "*.*")])
            if new_name:
                os.replace(self.filename, new_name)
                self.filename = new_name
                self.current_file_label.config(text=f"Current File: {self.filename}")
                messagebox.showinfo("Info", f"File renamed to: {self.filename}")
        except Exception as e:
            self.show_warning(f"Failed to rename file: {str(e)}")

    def open_file_location(self):
        try:
            file_dir = os.path.dirname(os.path.abspath(self.filename))
            os.startfile(file_dir)
        except Exception as e:
            self.show_warning(f"Failed to open file location: {str(e)}")

    def toggle_always_on_top(self):
        self.always_on_top = not self.always_on_top
        self.root.attributes("-topmost", self.always_on_top)
        status = "On" if self.always_on_top else "Off"
        self.always_on_top_button.config(text=f"Always on Top: {status}")

    def toggle_draggable(self):
        self.draggable = not self.draggable
        if self.draggable:
            self.root.overrideredirect(True)
            self.lock_unlock_button.config(text="Unlock")
        else:
            self.root.overrideredirect(False)
            self.lock_unlock_button.config(text="Lock")
            self.root.config(cursor="arrow")

    def show_changelogs(self):
        changelogs_window = tk.Toplevel(self.root)
        changelogs_window.title("Changelogs")
        changelogs_window.geometry("600x400")
        changelogs_window.resizable(False, False)

        frame = ttk.Frame(changelogs_window)
        frame.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure("Changelog.TFrame", background="#34495e")
        frame.config(style="Changelog.TFrame")

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        changelogs_text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, bg="#34495e", fg="#ecf0f1")
        changelogs_text.pack(fill=tk.BOTH, expand=True)

        changelogs = """
        Version 2.0-beta.1:
        - Release on GitHub
        - Open source

        Version 1.9.9:
        - Changed "New File" button to be smaller and placed under the record button.
        - Updated functionality for new file buttons to properly work.
        - Fixed crashing due to player.py
        - Added num_lock to key mapping

        Version 1.9.8:
        - Changed "Record New File" button to "New File" which creates a new file.
        - Updated functionality to record into the newly created file upon pressing "Record".

        Version 1.9.7:
        - Added a new button to start a new recording underneath the "Record New File" button.
        - Improved overall keybinding functionality and resolved issues with Control + A and other key bindings.

        Version 1.9.6:
        - Added repeat button smaller in size positioned to the right of the play button in LWmacroApp.
        - Fixed issues with keybindings and recording functionality.

        Version 1.9.5:
        - Added functionality to register every keybind and recording for playback in a .rec file.

        Version 1.9.4:
        - Added an "Open File Location" button underneath the current file display.

        Version 1.9.3:
        - Enhanced .rec file reading functionality to include keyboard press/hold timing.
        - Added a label for displaying updates at the top of the GUI.

        Version 1.9.2:
        - Fixed GUI visibility of exit and lock/unlock buttons.
        - Increased height of the GUI.

        Version 1.9.1:
        - Fixed button visibility and layout issues.
        - Added repeat button to the right of play button for infinite macro playback.

        Version 1.9:
        - Enhanced keyboard event recording to include press and hold timings.
        - Added Credits button.
        - Implemented draggable GUI with lock/unlock button.

        Version 1.8:
        - Added functionality to rename recording files.
        - Improved UI and fixed minor bugs.

        Version 1.7:
        - Changed recording file format to JSON for better compatibility and readability.
        - Improved error handling and user notifications.

        Version 1.6:
        - Reordered buttons into categories.
        - Placed "Always on Top" button in the top right corner, showing its status.
        - Added warning popup for unexpected errors.

        Version 1.5:
        - Moved Changelogs button to bottom-right corner with an emoji.
        - Added "Toggle Always on Top" button.

        Version 1.4:
        - Added "Always on Top" feature, enabled by default.
        - Added Changelogs button with version history.

        Version 1.3:
        - Added borderless window with draggable functionality.
        - Enhanced playback functionality to stop playback with the stop button.

        Version 1.2:
        - Improved GUI with modern styling.
        - Added buttons: Record, Stop, Play, Open File, Exit.

        Version 1.1:
        - Added file selection for saving and loading recordings.

        Version 1.0:
        - Basic recording and playback functionality for mouse and keyboard events.
        """.strip()

        changelogs_text.insert(tk.END, changelogs.strip())
        changelogs_text.config(state=tk.DISABLED)

        scrollbar.config(command=changelogs_text.yview)

        done_button = ttk.Button(changelogs_window, text="Done", command=changelogs_window.destroy)
        done_button.pack(pady=10)

    def show_credits(self):
        credits = """
        LWmacro 2.0-beta.1
        Developed by Jet

        Special thanks to:
        - Contributors and testers
        - Community support

        Libraries used:
        - Tkinter
        - Pynput
        - JSON
        - OS
        - Time

        Thank you for using LWmacro!
        """
        messagebox.showinfo("Credits", credits)

    def show_warning(self, message):
        messagebox.showwarning("Warning", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = LWmacroApp(root)
    root.mainloop()
