from tkinter import *
from PIL import Image, ImageTk
import speech_recognition as sr
from datetime import datetime


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
        feedback_label.config(text="Thank you for your feedback!", fg="green")
    else:
        feedback_label.config(text="Please enter your name and feedback.", fg="red")


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


# GUI Code
root = Tk()
root.geometry('500x400')
root.title('Feedback Interface')

# Load the images
uni_building_image = ImageTk.PhotoImage(Image.open('uni1.png'))  # Ensure 'uni1.png' is in the correct directory

# University Building Label
uni_building_label = Label(root, image=uni_building_image)
uni_building_label.pack(side=TOP, fill=X)

# Name Entry
name_label = Label(root, text="Name:", font=('times new roman', 12))
name_label.pack()
name_entry = Entry(root, font=('times new roman', 12))
name_entry.pack(pady=5)

# Feedback Entry
feedback_label = Label(root, text="Feedback:", font=('times new roman', 12))
feedback_label.pack()
feedback_entry = Text(root, height=4, width=40)
feedback_entry.pack(pady=5)

# Save Button
save_button = Button(root, text="Save Feedback", command=save_feedback)
save_button.pack(pady=5)

# Voice Capture Button
voice_button = Button(root, text="Capture Voice", command=capture_voice)
voice_button.pack(pady=5)

# Status Label
feedback_label = Label(root, text="", fg="red")
feedback_label.pack()

# Prevent image garbage collection
root.uni_building_image = uni_building_image

root.mainloop()
