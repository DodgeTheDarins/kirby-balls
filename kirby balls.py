import os
import sys
import pygame
import subprocess
import glob

from pynput import keyboard
import threading
import re

os.environ["PYNPUT_BACKEND"] = "uinput"

text = []
pygame.init()

def mrbeast(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('./assets')

    return os.path.normpath(os.path.join(base_path, relative_path))

files_list_with_ext = glob.glob(mrbeast("./*.mp3"))
files_list = []

for file in files_list_with_ext:
    filenew = os.path.basename(file)
    filenew, extension = os.path.splitext(filenew)
    files_list.append(filenew)

print(os.getcwd())
print("Test")
print(files_list)
print("why")

def soundeffect(file):
    """plays sound effect"""
    effect = pygame.mixer.Sound(mrbeast(file))
    effect.play()
    
def list(input_list, x):
    return input_list[-x:]

def remove(string, lst):
    # Join the list into a string
    lst_str = ''.join(lst)
    # Create a regex pattern for case-insensitive matching
    pattern = re.compile(re.escape(string), re.IGNORECASE)
    # Replace the matched string with an empty string
    lst_str = pattern.sub('', lst_str)
    # Update the original list with characters of the modified string
    lst.clear()
    lst.extend(lst_str)


def on_press(key):
    space = False
    try:
        if str('{0}'.format(key)) == "Key.space": 
            text.append(" ")
            space = True 
        print(text)
            
        char = key.char
        if char.lower() not in ["-", "_"] and not space:  
            text.append(char)
        for file in files_list: 
            file_space = " " + file
            
            if file_space in "".join(list(text, 20)): 
                soundeffect(file + ".mp3")
                
                # Acquire the lock before modifying text
                remove(file, text)
            
    except AttributeError:
        print(text)
        if str('{0}'.format(key)) == "Key.backspace" and text:
            text.pop(-1)


key = keyboard.Listener(on_press=on_press)
key.start()
key.join() 
