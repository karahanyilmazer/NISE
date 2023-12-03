# %%
import csv
import os
from datetime import datetime

import keyboard

# %%
curr_path = os.getcwd()
data_path = r'/home/muhammed/Desktop/NISE/csv_data/keyboard/non_dominant'
os.chdir(data_path)
run_num = sum("keyboard_non_dominant" in f_name for f_name in os.listdir()) + 1


# Create a list to store key presses
key_presses = []


# Function to handle key events
def on_key_event(e):
    # Get the current timestamp
    timestamp = datetime.now()
    # Append the key and timestamp to the list
    key_presses.append([timestamp, e.name])


# Start listening to key events
keyboard.hook(on_key_event)

# Wait for the user to stop the script
input("Press Enter to stop recording...")

# Unhook the keyboard listener
keyboard.unhook_all()

# Write key presses to a CSV file
with open(f'keyboard_non_dominant{run_num}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(['Time', 'Letter'])
    # Write key presses
    writer.writerows(key_presses)

# %%
