import tkinter as tk
from tkinter import messagebox
from pynput.keyboard import Controller, Listener, Key
import threading
import time
import pygetwindow as gw


def get_active_window_title():
    active_window = gw.getActiveWindow()
    return active_window.title if active_window else None


class KeyPresserApp:
    def __init__(self, root):
        self.root = root
        self.thread = None

        self.keys_listbox = tk.Listbox(self.root)
        self.stop_button = tk.Button(self.root, text="Stop (F4)", command=self.stop_pressing)
        self.start_button = tk.Button(self.root, text="Start (F3)", command=self.start_pressing)
        self.add_key_button = tk.Button(self.root, text="Add Key", command=self.add_key)
        self.key_entry = tk.Entry(self.root)

        self.root.title("Key Presser App")

        self.keys = []
        self.interval = tk.DoubleVar(value=10.5)
        self.target_window_title = tk.StringVar(value="Path of Exile")

        self.create_widgets()
        self.is_running = False
        self.keyboard = Controller()

        # Keyboard listener
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

    def create_widgets(self):
        tk.Label(self.root, text="Key:").grid(row=0, column=0, sticky="nsew")
        self.key_entry.grid(row=0, column=1, sticky="nsew")

        tk.Label(self.root, text="Interval (seconds):").grid(row=1, column=0, sticky="nsew")
        tk.Entry(self.root, textvariable=self.interval).grid(row=1, column=1, sticky="nsew")

        tk.Label(self.root, text="Target Window Title:").grid(row=2, column=0, sticky="nsew")
        tk.Entry(self.root, textvariable=self.target_window_title).grid(row=2, column=1, sticky="nsew")

        self.add_key_button.grid(row=3, column=0, columnspan=2, sticky="nsew")

        self.start_button.grid(row=4, column=0, columnspan=2, sticky="nsew")

        self.stop_button.grid(row=5, column=0, columnspan=2, sticky="nsew")

        self.keys_listbox.grid(row=6, column=0, columnspan=2, sticky="nsew")

        # Expanding grid
        for i in range(7):
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
            print("Add at least one key first.")
            messagebox.showwarning("No no no", "Add at least one key first")
            return

        if not self.target_window_title.get():
            print("Set a target window title first.")
            messagebox.showinfo(
                "Just so you know",
                "You can set a target window so your macro will only run when "
                "it is focused. If you want it to be used everywhere, type *",
            )
            return

        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self.press_keys)
            self.thread.start()
            print(f"Started pressing at interval {self.interval.get()}")

    def stop_pressing(self):
        self.is_running = False
        if self.thread is not None:
            self.thread.join()
        self.thread = None
        print("Stopped pressing")

    def check_window(self, active_window):
        if active_window:
            return (self.target_window_title.get() == active_window.title) or self.is_any_window()

    def is_any_window(self):
        return self.target_window_title.get() == "*"

    def press_keys(self):
        while self.is_running:
            active_window = gw.getActiveWindow()
            if self.check_window(active_window):
                print(f"pressing {self.keys} \n")
                for key in self.keys:
                    self.keyboard.press(key)
                    time.sleep(0.05)
                    self.keyboard.release(key)
                time.sleep(self.interval.get())
            else:
                print("Not focused")
                time.sleep(0.5)

    def on_press(self, key):
        try:
            if key == Key.f3:
                self.start_pressing()
            elif key == Key.f4:
                self.stop_pressing()
        except AttributeError:
            pass


if __name__ == "__main__":
    # print(get_active_window_title()) Useful for finding your window title
    root = tk.Tk()
    app = KeyPresserApp(root)
    root.mainloop()
