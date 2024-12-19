import os
import subprocess
import tarfile
import xml.etree.ElementTree as ET
import time
from datetime import datetime
import colorama
from colorama import Fore, Back, Style
colorama.init()

class ShellEmulator:
    def __init__(self, config_file):
        self.start_time = time.time()
        self.history = []
        self.load_config(config_file)

        with tarfile.open(self.vfs_path) as tar:
            tar.extractall(path=self.current_dir)

        self.load_startup_script(self.startup_script)

    def load_config(self, config_file):
        tree = ET.parse(config_file)
        root = tree.getroot()

        self.username = root.find('username').text
        self.vfs_path = root.find('tar_path').text
        self.startup_script = root.find('start_path').text
        self.current_dir = os.path.expanduser("~")

    def load_startup_script(self, script_path):
        if os.path.exists(script_path):
            with open(script_path) as f:
                for command in f:
                    self.execute_command(command.strip())

    def execute_command(self, command):
        self.history.append(command)
        if command == "exit":
            print("Выход...")
            return False
        elif command.startswith("cd "):
            self.change_directory(command[3:].strip())
        elif command == "ls":
            self.list_directory()
        elif command == "history":
            self.show_history()
        elif command == "uptime":
            self.show_uptime()
        elif command == "clear":
            self.clear_screen()
        else:
            self.history.pop()
            #print("no!")
            #print(f"{command}: command not found")
            #return False
        return True

    def change_directory(self, path):
        try:
            os.chdir(path)
            self.current_dir = os.getcwd()
        except FileNotFoundError:
            print(f"cd: {path}: No such file or directory")

    def list_directory(self):
        for item in os.listdir(self.current_dir):
            print(item)

    def show_history(self):
        for index, command in enumerate(self.history):
            print(f"{index + 1}: {command}")

    def show_uptime(self):
        uptime_seconds = time.time() - self.start_time
        print(f"Uptime: {uptime_seconds:.2f} seconds")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def run(self):
        print("Добро пожаловать в " + Fore.MAGENTA + "женскую " + Style.RESET_ALL + "консоль")
        while True:
            print(Fore.MAGENTA + f"{self.username}@shell:~$ ", end="" + Style.RESET_ALL)
            command = input()
            if not self.execute_command(command):
                break


if __name__ == "__main__":
    config_file = 'config1.xml'
    emulator = ShellEmulator(config_file)
    emulator.run()

