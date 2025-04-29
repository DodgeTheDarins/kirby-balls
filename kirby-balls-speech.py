import os
import sys
import pygame
import subprocess
import glob
try:
    import speech_recognition as sr
except:
    subprocess.call(['python','-m','pip','install','SpeechRecognition','openai-whisper','pyaudio'])
    import speech_recognition as sr
from pynput import keyboard
import threading
import re

r = sr.Recognizer()
mic = sr.Microphone()
text = []
text_lock = threading.Lock()  # Lock for synchronizing access to text
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



def voice_recognition():
    print("Voice recognition started...")
    while True:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        print("done listening")
        response = r.recognize_whisper(audio)
        characters = [char for char in response]
        
        # Acquire the lock before modifying text
        with text_lock:
            text.extend(characters)
            print(response)
            print(text)
        
        print("".join(list(text, 200)).lower())
        for file in files_list: 
            file_space = " " + file
            if file_space in "".join(list(text, 200)).lower(): 
                soundeffect(file + ".mp3")
                print("yes")
                # Acquire the lock before modifying text
                with text_lock:    
                    remove(file, text)

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
                with text_lock:
                    remove(file, text)
            
    except AttributeError:
        print(text)
        if str('{0}'.format(key)) == "Key.backspace" and text:
            text.pop(-1)

# Create a thread for the keyboard listener
def keyboard_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Start both voice recognition and keyboard listener concurrently
voice_thread = threading.Thread(target=voice_recognition)
keyboard_thread = threading.Thread(target=keyboard_listener)

voice_thread.start()
keyboard_thread.start()

# Wait for both threads to finish kirby kirby
voice_thread.join()
keyboard_thread.join()
