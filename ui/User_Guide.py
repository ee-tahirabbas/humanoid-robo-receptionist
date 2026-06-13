import tkinter as tk
from tkinter import Toplevel, Text, Scrollbar, RIGHT, Y
import pyttsx3
import threading


engine = pyttsx3.init()
stop_speech = False

def onWord(name, location, length):
    global stop_speech
    if stop_speech:
        engine.stop()

engine.connect('word', onWord)

def speak_text(text):
    global stop_speech
    stop_speech = False
    engine.say(text)
    engine.runAndWait()

def run_user_guide():
    global stop_speech

    user_guide_window = Toplevel()
    # ... (window setup code)

    user_guide_window.bind("<u>", close_user_guide)
    user_guide_window.bind("<U>", close_user_guide)

    # ... (text widget and scrollbar code)

    speech_thread = threading.Thread(target=lambda: speak_text(user_guide_text), daemon=True)
    speech_thread.start()

    user_guide_window.focus_force()

def close_user_guide(event=None):
    global stop_speech
    stop_speech = True

    # Attempt to stop the speech thread gracefully
    speech_thread.join(timeout=0.5)  # Wait briefly for the thread to finish

    # If it's still running, forcefully terminate it
    if speech_thread.is_alive():
        engine.stop()  # Attempt to stop the engine directly
        try:
            speech_thread._stop()  # Forcefully stop the thread (use with caution)
        except Exception as e:
            print("Error stopping thread:", e)

    user_guide_window.destroy()