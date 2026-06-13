import tkinter as tk
from tkinter import *
from tkinter import font as tkFont  # Import the font module
from tkinter import Toplevel, Text, Scrollbar, RIGHT, Y
import pyttsx3
import threading
import speech_recognition as sr
from PIL import Image, ImageTk
import subprocess
from datetime import datetime

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def create_button(parent, text, command=None):
    return tk.Button(parent, text=text, padx=10, pady=5, bg='slate gray', fg='white', command=command)

def create_label(parent, text):
    return tk.Label(parent, text=text, padx=10, pady=5, bg='slate gray', fg='white')

def run_query_section():
    subprocess.Popen([python_executable, script_path_query_section], shell=True)

def run_enable_auto_detection():
    subprocess.Popen([python_executable, script_path_enable_auto_detection], shell=True)


# Initialize the text-to-speech engine outside the function to make it global
engine = pyttsx3.init()

# This flag will control the stopping of the speech
stop_speech = False

def onWord(name, location, length):
    global stop_speech
    # If stop_speech is True, stop the engine
    if stop_speech:
        engine.stop()

# Connect the event handler to the 'word' event
engine.connect('word', onWord)

def speak_text(text):
    global stop_speech
    stop_speech = False  # Reset the flag when starting to speak
    engine.say(text)
    engine.runAndWait()

def run_user_guide():
    global stop_speech

    # Create a new top-level window
    user_guide_window = Toplevel()
    user_guide_window.title("User Guide")
    user_guide_window.geometry("500x400+445+110")

    # Function to close the window and stop speaking
    def close_user_guide(event=None):
        global stop_speech
        stop_speech = True  # Signal the speech to stop
        user_guide_window.destroy()
        engine.stop()  # Explicitly stop the engine when closing the window

    # Bind the 'u' key to the close_user_guide function
    user_guide_window.bind("<u>", close_user_guide)
    user_guide_window.bind("<U>", close_user_guide)  # Bind uppercase 'U' if needed

    # Create a text widget with a scrollbar
    text_widget = Text(user_guide_window, wrap= "word")
    text_widget.pack(side="left", fill="both", expand=True)
    scrollbar = Scrollbar(user_guide_window, command=text_widget.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    # Insert the user guide text into the text widget
    user_guide_text = """
    == ChatBot User Guide ==

    Starting a Conversation:
    - Click on the 'New Conversation' button on the home screen.

    Saving a Conversation:
    - After finishing your chat, click 'File' and select 'Save Conversation'.

    Changing Settings:
    - Click on 'Tools' and select 'Options' to access settings.

    For more information, contact our support team.
    """
    text_widget.insert("end", user_guide_text)
    text_widget.config(state="disabled")  # Make the text read-only

    # Start the speech in a separate thread
    speak_thread = threading.Thread(target=lambda: speak_text(user_guide_text), daemon=True)
    speak_thread.start()

    # Focus on the new window to ensure it receives the key press
    user_guide_window.focus_force()

def run_feedback_integrated():
    feedback_window = Toplevel(root)
    feedback_window.geometry('460x380+465+130')
    feedback_window.title('Feedback Interface')

    # Ensure the 'uni1.png' image path is correct and accessible from your main application directory
    uni_building_image = ImageTk.PhotoImage(Image.open('uni1.png'))  # Load the image
    uni_building_label = Label(feedback_window, image=uni_building_image)
    uni_building_label.pack(side=tk.TOP, fill=tk.X)
    uni_building_label.image = uni_building_image  # Keep a reference to prevent garbage collection

    # Name Entry
    name_label = Label(feedback_window, text="Name:", font=('times new roman', 12))
    name_label.pack()
    global name_entry  # Make it global to access it outside this function
    name_entry = Entry(feedback_window, font=('times new roman', 12))
    name_entry.pack(pady=5)

    # Feedback Entry
    global feedback_entry, feedback_label  # Make them global to access outside this function
    feedback_label = Label(feedback_window, text="Feedback:", font=('times new roman', 12))
    feedback_label.pack()
    feedback_entry = Text(feedback_window, height=4, width=40)
    feedback_entry.pack(pady=5)

    def capture_voice():
        user_name = name_entry.get().strip()
        if user_name:
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                feedback_label.config(text="Listening...", fg="blue")
                audio = recognizer.listen(source)
                feedback_label.config(text="")

                try:
                    feedback = recognizer.recognize_google(audio)
                    feedback_entry.insert(END, feedback + "\n")
                except sr.UnknownValueError:
                    feedback_label.config(text="Sorry, I did not understand that.", fg="red")
                except sr.RequestError:
                    feedback_label.config(text="Service is unavailable; try again later.", fg="red")
        else:
            feedback_label.config(text="Please enter your name before capturing voice.", fg="red")

    def save_feedback():
        user_name = name_entry.get().strip()
        feedback = feedback_entry.get("1.0", END).strip()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current date and time

        if user_name and feedback:  # Check if user name and feedback are not empty
            feedback_text = f"Name: {user_name}\nDate/Time: {current_time}\nFeedback: {feedback}\n\n"
            feedback_file = "user_feedback.txt"
            with open(feedback_file, "a") as file:
                file.write(feedback_text)
            feedback_entry.delete("1.0", END)  # Clear the feedback entry after saving
            name_entry.delete(0, END)  # Clear the name entry after saving
            feedback_message = "Thank you for your feedback!"
            feedback_label.config(text=feedback_message, fg="green")
        else:
            feedback_message = "Please enter your name and feedback."
            feedback_label.config(text= feedback_message, fg="red")

            # Use the speak function to vocalize the status message
        speak(feedback_message)

    # Save Button
    save_button = Button(feedback_window, text="Save Feedback", command=save_feedback)
    save_button.pack(pady=5)

    # Voice Capture Button
    voice_button = Button(feedback_window, text="Capture Voice", command=capture_voice)
    voice_button.pack(pady=5)

    # Status Label
    feedback_label = Label(feedback_window, text="", fg="red")
    feedback_label.pack()

    # Ensure the feedback_window has a reference to uni_building_image to prevent garbage collection
    feedback_window.uni_building_image = uni_building_image

#def run_feedback():
    #subprocess.Popen([python_executable, script_path_feedback], shell=True)

# Define the Python executable and script paths
python_executable = "C:\\Users\\PMLS\\AbuZarProjects\\error\\.venv\\Scripts\\python.exe"
script_path_query_section = "C:\\Users\\PMLS\\AbuZarProjects\\error\\query_section.py"
script_path_user_guide = "C:\\Users\\PMLS\\AbuZarProjects\\error\\User_Guide.py"
script_path_enable_auto_detection = "C:\\Users\\PMLS\\AbuZarProjects\\error\\enable_auto_detection.py"

root = tk.Tk()
root.geometry('700x550+250+30')
root.title('ChatBot created by Sheri')
root.config(bg='slate gray')


# Load the images
uni_building_photo = Image.open('uni1.png')
uni_building_image = ImageTk.PhotoImage(uni_building_photo)

# Create a label for the university building image
uni_building_label = tk.Label(root, image=uni_building_image)
uni_building_label.pack()

# Load the transparent UET logo
uet_logo_photo = Image.open('uet.png')
uet_logo_image = ImageTk.PhotoImage(uet_logo_photo)

# Create a label for the UET logo and position it over the university building image
uet_logo_label = tk.Label(uni_building_label, image=uet_logo_image, bd=0)
uet_logo_label.place(x=5, y=5)

# Left panel
left_panel = tk.Frame(root, bg='darkgray', width=190)  # Adjust the width as needed
left_panel.pack(side=tk.LEFT, fill=tk.Y, expand=False)
left_panel.pack_propagate(False)  # Prevent the frame from resizing to fit its children

# "Chatbot" label at the top of the left panel
chatbot_label = create_label(left_panel, "Chatbot")
chatbot_label.pack(fill=tk.X, padx=10, pady=5)

# Define button texts and their corresponding functions
button_texts = ["User Guide", "Query Section", "Feedback"]
button_functions = [run_user_guide, run_query_section, run_feedback_integrated]

# Create the buttons and pack them into the left_panel
for text, command in zip(button_texts, button_functions):
    button = create_button(left_panel, text, command)
    button.pack(fill=tk.X, padx=10, pady=5)

# Load the new PNG image that you want to display below the buttons of the left panel
robo_png_photo = Image.open('robo.png')  # Update the path to your new image file
robo_png_image = ImageTk.PhotoImage(robo_png_photo)

# Create a label for the new PNG image within the left panel below the buttons
robo_png_label = tk.Label(left_panel, image=robo_png_image, bd=0)
robo_png_label.pack(pady=2)  # Add some padding to space it out from the buttons

# Set the central content area with more control over the text appearance
customFont = tkFont.Font(family="Verdana", size=14, weight="bold")  # Customize the font

content_area = tk.Label(root, text="For Face Recognition Click Enable Auto Detection Button",
                        borderwidth=2, relief="solid",
                        font=customFont,  # Apply the custom font
                        fg="red",  # Set the text color to blue
                        bg="white",  # Set the background color to white
                        width=50, height=10, wraplength=450, justify='center')  # Set the width and height
content_area.pack(pady=20, padx=20, fill="both", expand=True)  # Center the content_area

# Set the bottom panel for the "Enable Auto Detection" button
bottom_panel = tk.Frame(root, bg='white', height=45)
bottom_panel.pack(side=tk.BOTTOM, fill=tk.X)

# Add "Enable Auto Detection" button to the bottom panel
auto_detect_button = create_button(bottom_panel, "Enable Auto Detection", command=run_enable_auto_detection)
auto_detect_button.place(relx=0.5, rely=0.5, anchor='center')

# Keep a reference to the images to prevent garbage collection
root.uni_building_image = uni_building_image
root.uet_logo_image = uet_logo_image

root.mainloop()
