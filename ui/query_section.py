from tkinter import *
from PIL import Image, ImageTk
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import pyttsx3
import speech_recognition as sr
import threading

# Initialize the chatbot with a specific storage adapter to prevent untrained responses
bot = ChatBot('Bree',
              storage_adapter='chatterbot.storage.SQLStorageAdapter',
              database_uri='sqlite:///database.sqlite3')

# List of conversations
data_list = [
    'Hello Bree',
    'Hey! Welcome to UET Narowal',
    'How many departments in UET Narowal campus?',
    'There are five departments in UET Narowal campus which are: Electrical, Mechanical, Civil, Biomedical, Computer Science',
    'Who is campus coordinator?',
    'Professor Dr. Muhammad Shahbaz is the campus coordinator of UET Narowal',
    'Who is Chairperson of Electrical Department?',
    'Dr. Waqas Tariq Toor is the Chairperson of Electrical Department',
    'Ok bye',
    'Bye, take care'
]

# Train the chatbot
trainer = ListTrainer(bot)
trainer.train(data_list)

# Function to speak the response
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def botReply():
    question = questionField.get()
    question = question.capitalize()
    answer = bot.get_response(question)
    textarea.insert(END, 'You: ' + question + '\n')
    textarea.insert(END, 'Bree: ' + str(answer) + '\n\n')
    speak_thread = threading.Thread(target=speak, args=(str(answer),))
    speak_thread.start()
    questionField.delete(0, END)

voice_enabled = False  # Flag to control the state of voice recognition

def toggle_voice(state):
    global voice_enabled
    voice_enabled = state

def audioToText():
    global voice_enabled
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while voice_enabled:
            try:
                audio = r.listen(source)
                text = r.recognize_google(audio)
                root.after(0, questionField.insert, 0, text)
                root.after(0, botReply)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

# GUI Code
root = Tk()
root.geometry('650x450+275+70')
root.title('ChatBot created by Sheri')
root.config(bg='slate gray')

# Configure the grid layout for the root
root.grid_rowconfigure(0, weight=1)  # Gives vertical stretch to the TextArea
root.grid_rowconfigure(1, weight=0)  # Keeps QuestionField and ButtonFrame fixed
root.grid_columnconfigure(0, weight=1)  # Gives horizontal stretch

# Load the images
uni_building_image = ImageTk.PhotoImage(Image.open('uni1.png'))
uet_logo_image = ImageTk.PhotoImage(Image.open('uet.png'))

# University Building Label
uni_building_label = Label(root, image=uni_building_image)
uni_building_label.grid(row=0, column=0, sticky="nsew")

# UET Logo Label - overlay using place for precise positioning
uet_logo_label = Label(uni_building_label, image=uet_logo_image)
# Adjust the x and y offsets to position the logo as desired
uet_logo_label.place(relx=0.035, rely=0.24, anchor="center")

# Text Area Frame
centerFrame = Frame(root)
centerFrame.grid(row=1, column=0, sticky="ew")

# Text Area with Scrollbar
scrollbar = Scrollbar(centerFrame)
scrollbar.pack(side=RIGHT, fill=Y)
textarea = Text(centerFrame, font=('times new roman', 20, 'bold'), height=5, yscrollcommand=scrollbar.set, wrap='word')
textarea.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.config(command=textarea.yview)

# Question Field
questionField = Entry(root, font=('times new roman', 20, 'bold'))
questionField.grid(row=2, column=0, sticky="ew", pady=15)

# Button Frame
button_frame = Frame(root, bg='slate gray')
button_frame.grid(row=3, column=0, sticky="ew")

# Enable/Disable Voice Buttons and Ask Button
enable_voice_button = Button(button_frame, text="Enable Voice", command=lambda: toggle_voice(True), padx=20, pady=10)
disable_voice_button = Button(button_frame, text="Disable Voice", command=lambda: toggle_voice(False), padx=20, pady=10)
askPic = PhotoImage(file='ask.png')  # Make sure 'ask.png' is in the correct directory
askButton = Button(button_frame, image=askPic, command=botReply)

# Configure the grid layout for the button frame
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=2)
button_frame.grid_columnconfigure(2, weight=1)

enable_voice_button.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
askButton.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
disable_voice_button.grid(row=0, column=2, padx=10, pady=10, sticky='ew')

# Start and stop voice thread functions
def start_voice_thread():
    global voice_enabled
    if not voice_enabled:
        voice_enabled = True
        thread = threading.Thread(target=audioToText)
        thread.daemon = True
        thread.start()

def stop_voice_thread():
    global voice_enabled
    voice_enabled = False

enable_voice_button.config(command=start_voice_thread)
disable_voice_button.config(command=stop_voice_thread)

# Prevent image garbage collection
root.uni_building_image = uni_building_image
root.uet_logo_image = uet_logo_image

root.mainloop()

