# Import packages
import pyperclip
import pyautogui
import time
from datetime import datetime
import os

# Change this path to where you have saved contacts_icon.png and search_bar_icon.png
icon_dir = os.getcwd()
contacts_icon_path = os.path.join(icon_dir, 'contacts_icon.png')
search_icon_path = os.path.join(icon_dir, 'search_bar_icon.png')

# Change this dir to where you have saved schedule.txt and recipient.txt files
schedule_dir = os.getcwd()

'''Make sure you have WeChat pinned on top
Recipient name can ONLY be WeChat ID (Python has trouble dealing with file names containing Chinese or special characters)
Recipient name in schedule.txt has to match the name of recipient.txt
date,time_ in schedule.txt is in the format of YYYY-MM-DD,HH:MM:SS with HH being in 24 h format
'''

# Function to locate and click the 'Contacts' icon dynamically.
def click_contacts():
    # Make sure you have WeChat pinned on top
    try:
        location = pyautogui.locateOnScreen(contacts_icon_path, confidence=0.8)
        if location:
            center = pyautogui.center(location)
            pyautogui.click(center)  # Click the center of the found icon
            print("Clicked on 'Contacts' icon.")
        else:
            print("Error: 'Contacts' icon not found on the screen.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to locate and click the search bar dynamically.
def click_search():
    # Make sure you have WeChat pinned on top
    try:
        location = pyautogui.locateOnScreen(search_icon_path, confidence=0.8)
        if location:
            center = pyautogui.center(location)
            pyautogui.click(center)  # Click the center of the found icon
            print("Clicked on the search bar")
        else:
            print("Error: Search bar not found on the screen.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
# Function to load the schedule from schedule.txt
def load_schedule():
    schedule = []
    schedule_file = os.path.join(schedule_dir, "schedule.txt")
    
    with open(schedule_file, "r") as f:
        for line in f:
            line = line.strip() # strip() removes leading and trailing whitespace
            if line:
                recipient, date, time_ = line.split(',') # Recipient name can ONLY be WeChat ID
                # Read the corresponding message file
                message_file = os.path.join(schedule_dir, f"{recipient}.txt") # Recipient name can ONLY be WeChat ID
                if os.path.exists(message_file):
                    with open(message_file, "r") as mf:
                        message = mf.read().strip() # strip() removes leading and trailing whitespace
                    schedule.append({
                        'recipient': recipient,
                        'message': message,
                        'date': date,
                        'time': time_
                    })
                else:
                    print(f"Warning: Message file for {recipient} not found. Skipping.")
    
    schedule.sort(key=lambda x: f"{x['date']} {x['time']}") # Sort the schedule by date and time
    
    return schedule

# Function to pause script execution until the target time
def wait_until(target_time):
    now = datetime.now()
    while now < target_time:
        time.sleep(1)
        now = datetime.now()

# Function to open a chat window for the recipient using WeChat's search functionality
def open_chat_window(recipient):
    # MAKE SURE YOU HAVE WECHAT PINNED ON TOP!!!!
    click_contacts() # Click Contacts
    time.sleep(0.5)
    click_search() # Click on the search bar
    pyperclip.copy(recipient) # Copy recipient name
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v') # Paste recipient name
    time.sleep(0.5)
    pyautogui.press('enter') # Open the chat window

# Function to send a specified message in the current chat window.
def send_message(message):
    pyperclip.copy(message) # Copy the message
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v') # Paste the message
    time.sleep(0.5)
    pyautogui.press('enter')  # Send the message

# Function to schedule messages based on the provided schedule
def schedule_messages(schedule):
    for task in schedule:
        # Parse the scheduled date and time
        scheduled_time = datetime.strptime(f"{task['date']} {task['time']}", '%Y-%m-%d %H:%M:%S')
        
        # Wait until the scheduled time
        wait_until(scheduled_time)
        
        # Open the recipient's chat window and send the message
        open_chat_window(task['recipient'])
        send_message(task['message'])
        print(f"Message sent to {task['recipient']} at {datetime.now()}")

# Run this script
if __name__ == '__main__':
    schedule = load_schedule()
    if schedule:
        schedule_messages(schedule)
    else:
        print("No valid schedule found.")
