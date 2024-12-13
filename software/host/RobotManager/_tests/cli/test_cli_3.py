import curses
import subprocess
import time
import threading
import random
import os
import sys
from datetime import datetime


class SimpleCLI:
    def __init__(self):
        self.messages = [
            "Welcome to the Simple CLI!",
            "Type 'exit' to quit the application.",
            "Use UP/DOWN to scroll, Page Down to auto-scroll."
        ]
        self.running = True
        self.screen_lock = threading.Lock()
        self.scroll_offset = 0
        self.auto_scroll = True

    def start(self):
        # Check if running inside PyCharm terminal and relaunch in a proper terminal if so
        if "PYCHARM_HOSTED" in os.environ:
            print("Detected PyCharm terminal. Relaunching in a proper terminal window...")
            if sys.platform == "win32":
                subprocess.Popen(["cmd.exe", "/c", "set RELAUNCHED=1 && python", sys.argv[0]], creationflags=subprocess.CREATE_NEW_CONSOLE)
            elif sys.platform == "darwin":
                ...
                # os.system(f'osascript -e 'tell application "Terminal" to do script" python3 {sys.argv[0]}"'')
            else:
                os.system(f'gnome-terminal -- python3 {sys.argv[0]}')
            sys.exit()
        else:
            curses.wrapper(self.main)


    def add_message(self, message):
        with self.screen_lock:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.messages.append(f"[{timestamp}] {message}")
            if self.auto_scroll:
                self.scroll_offset = 0  # Reset scroll to bottom when a new message arrives
            self.display_messages()

    def display_messages(self):
        self.screen.clear()
        max_y, max_x = self.screen.getmaxyx()

        # Display scrolling instructions above the input field
        instructions = "Use UP/DOWN to scroll, Page Down to auto-scroll"
        self.screen.addnstr(max_y - 4, 0, instructions, max_x - 1, curses.A_REVERSE)

        # Display the last lines fitting on the screen considering the scroll offset
        start_index = max(0, len(self.messages) - (max_y - 5) - self.scroll_offset)
        end_index = min(len(self.messages), start_index + (max_y - 5))
        display_messages = self.messages[start_index:end_index]

        for idx, msg in enumerate(display_messages):
            if "User:" in msg:
                self.screen.attron(curses.color_pair(1))
            elif "System:" in msg:
                self.screen.attron(curses.color_pair(2))
            self.screen.addnstr(idx, 0, msg, max_x - 1)
            self.screen.attroff(curses.color_pair(1))
            self.screen.attroff(curses.color_pair(2))

        # Display scroll indicator
        if self.scroll_offset > 0:
            scroll_indicator = f"-- Scroll ({self.scroll_offset}) --"
            self.screen.addnstr(max_y - 3, 0, scroll_indicator, max_x - 1, curses.A_REVERSE)

        # Set cursor position to the input field at the bottom
        self.screen.addstr(max_y - 2, 0, "> {}".format(self.input_buffer))
        self.screen.refresh()

    def user_input_handler(self):
        self.input_buffer = ""
        while self.running:
            key = self.screen.getch()
            if key == curses.KEY_BACKSPACE or key == 127:
                self.input_buffer = self.input_buffer[:-1]
            elif key == curses.KEY_UP:  # Scroll up
                if self.scroll_offset < len(self.messages) - 1:
                    self.scroll_offset += 1
                    self.auto_scroll = False
            elif key == curses.KEY_DOWN:  # Scroll down
                if self.scroll_offset > 0:
                    self.scroll_offset -= 1
                if self.scroll_offset == 0:
                    self.auto_scroll = True
            elif key == curses.KEY_NPAGE:  # Page Down to re-enable auto scroll
                self.scroll_offset = 0
                self.auto_scroll = True
            elif key == 10:  # Enter key
                user_input = self.input_buffer
                self.input_buffer = ""
                if user_input.lower() == "exit":
                    self.running = False
                else:
                    self.add_message(f"User: {user_input}")
            else:
                self.input_buffer += chr(key)
            self.display_messages()

    def generate_random_messages(self):
        while self.running:
            time.sleep(random.uniform(1, 4))
            self.add_message("System: This is a random system message.")

    def main(self, screen):
        self.screen = screen
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # User messages in cyan
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # System messages in yellow
        curses.curs_set(1)  # Enable the cursor
        screen.clear()

        # Start user input handling in a separate thread
        user_input_thread = threading.Thread(target=self.user_input_handler, daemon=True)
        user_input_thread.start()

        # Generate random messages
        self.generate_random_messages()


if __name__ == "__main__":
    cli = SimpleCLI()
    cli.start()
