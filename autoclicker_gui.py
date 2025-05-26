import tkinter as tk
from tkinter import messagebox
import threading
import pyautogui
import keyboard
import time

class AutoClicker:
    def __init__(self, master):
        self.master = master
        master.title("Auto Clicker")
        master.geometry("300x200")
        master.resizable(False, False)

        self.clicking = False
        self.delay = 0.1

        self.label = tk.Label(master, text="Click Interval (ms):")
        self.label.pack(pady=10)

        self.entry = tk.Entry(master, justify="center")
        self.entry.insert(0, "100")
        self.entry.pack()

        self.start_button = tk.Button(master, text="Start Clicking", command=self.start_clicking)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(master, text="Stop Clicking", command=self.stop_clicking)
        self.stop_button.pack(pady=5)

        self.status = tk.Label(master, text="Status: Idle")
        self.status.pack(pady=10)

        self.listener_thread = threading.Thread(target=self.hotkey_listener, daemon=True)
        self.listener_thread.start()

    def click_loop(self):
        while self.clicking:
            pyautogui.click()
            time.sleep(self.delay)

    def start_clicking(self):
        try:
            ms = int(self.entry.get())
            self.delay = ms / 1000.0
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return

        if not self.clicking:
            self.clicking = True
            self.status.config(text="Status: Clicking")
            threading.Thread(target=self.click_loop, daemon=True).start()

    def stop_clicking(self):
        self.clicking = False
        self.status.config(text="Status: Idle")

    def hotkey_listener(self):
        keyboard.add_hotkey("F6", self.toggle_clicking)
        keyboard.wait("esc")
        self.master.quit()

    def toggle_clicking(self):
        if self.clicking:
            self.stop_clicking()
        else:
            self.start_clicking()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
