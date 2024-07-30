import tkinter as tk
from pynput.keyboard import Controller, Listener, Key
import threading
import time


class KeyPresserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Key Presser App")

        self.keys = []
        self.interval = tk.DoubleVar(value=1.0)

        self.create_widgets()
        self.is_running = False
        self.keyboard = Controller()

        # Start the keyboard listener for shortcuts
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

    def create_widgets(self):
        tk.Label(self.root, text="Key:").grid(row=0, column=0, sticky="nsew")
        self.key_entry = tk.Entry(self.root)
        self.key_entry.grid(row=0, column=1, sticky="nsew")

        tk.Label(self.root, text="Interval (seconds):").grid(row=1, column=0, sticky="nsew")
        tk.Entry(self.root, textvariable=self.interval).grid(row=1, column=1, sticky="nsew")

        self.add_key_button = tk.Button(self.root, text="Add Key", command=self.add_key)
        self.add_key_button.grid(row=2, column=0, columnspan=2, sticky="nsew")

        self.start_button = tk.Button(self.root, text="Start (F3)", command=self.start_pressing)
        self.start_button.grid(row=3, column=0, columnspan=2, sticky="nsew")

        self.stop_button = tk.Button(self.root, text="Stop (F4)", command=self.stop_pressing)
        self.stop_button.grid(row=4, column=0, columnspan=2, sticky="nsew")

        self.keys_listbox = tk.Listbox(self.root)
        self.keys_listbox.grid(row=5, column=0, columnspan=2, sticky="nsew")

        # Configure the grid to expand
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def add_key(self):
        key = self.key_entry.get()
        if key:
            self.keys.append(key)
            self.keys_listbox.insert(tk.END, key)
            self.key_entry.delete(0, tk.END)
            print(f"Key added: {key}")

    def start_pressing(self):
        if not self.keys:
            print("Please add at least one key first.")
            return

        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self.press_keys)
            self.thread.start()
            print("Started pressing")

    def stop_pressing(self):
        self.is_running = False
        if hasattr(self, 'thread'):
            self.thread.join()
        print("Stopped pressing")

    def press_keys(self):
        while self.is_running:
            for key in self.keys:
                self.keyboard.press(key)
            for key in self.keys:
                self.keyboard.release(key)
            time.sleep(self.interval.get())

    def on_press(self, key):
        try:
            if key == Key.f3:
                self.start_pressing()
            elif key == Key.f4:
                self.stop_pressing()
        except AttributeError:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = KeyPresserApp(root)
    root.mainloop()
