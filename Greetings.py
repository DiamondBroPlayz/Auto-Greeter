import os
import shutil
from datetime import datetime
from os.path import exists
from win10toast import ToastNotifier
import time

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create the batch file path
batch_file_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'launch_script.bat')

# Create the content of the batch file
batch_file_content = '''@echo off
py "{}"
'''.format(os.path.join(script_dir, 'script.py'))

# Write the batch file
with open(batch_file_path, 'w') as batch_file:
    batch_file.write(batch_file_content)

# Run the Python script
os.system('python "{}"'.format(os.path.join(script_dir, 'script.py')))

# Function to determine the part of the day based on the current hour
def get_part_of_day(h):
    return (
        "morning"
        if 5 <= h <= 11
        else "afternoon"
        if 12 <= h <= 17
        else "evening"
        if 18 <= h <= 22
        else "night"
    )

# Function to get the names from the file or prompt the user for input and save it
def get_names():
    if exists('name.txt'):
        with open('name.txt') as file_object:
            names = file_object.read()
    else:
        names = input("What is your name? ")
        with open('name.txt', 'w') as file_object:
            file_object.write(names)
    return names

# Function to display the greeting message and show a toast notification
def display_greeting(names):
    h = datetime.now().hour
    part_of_day = get_part_of_day(h)
    print(f"Good {part_of_day}, {names}!")

    toast = ToastNotifier()
    toast.show_toast(
        "Greetings!",
        f"Good {part_of_day}, {names}",
        duration=20,
        icon_path="icon.ico",
        threaded=True,
    )

# Initialize previous part of the day as None
prev_part_of_day = None

# Main loop to check for changes in the part of the day
while True:
    names = get_names()
    h = datetime.now().hour
    part_of_day = get_part_of_day(h)

    # Check if the part of the day has changed
    if part_of_day != prev_part_of_day:
        display_greeting(names)

    prev_part_of_day = part_of_day

    # Sleep for 1 minute before checking again
    time.sleep(60)
