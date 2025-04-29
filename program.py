import os
import sys
import pygame
import glob
from pynput import keyboard

text = []
pygame.init()

def mrbeast(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.\\assets')

    return os.path.normpath(os.path.join(base_path, relative_path))

files_list_with_ext = glob.glob(mrbeast(".\\*.mp3"))
files_list = []

for file in files_list_with_ext:
    filenew = os.path.basename(file)
    filenew, extension = os.path.splitext(filenew)
    files_list.append(filenew)

def soundeffect(file):
    """plays sound effect"""
    effect = pygame.mixer.Sound(mrbeast(file))
    effect.play()
    
def list(input_list, x):
    return input_list[-x:]


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
                # remove(file, text)
            
    except AttributeError:
        print(text)
        if str('{0}'.format(key)) == "Key.backspace" and text:
            text.pop(-1)

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()