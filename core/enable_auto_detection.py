import cv2
import pyttsx3
import pickle
import pandas as pd
import speech_recognition as sr
from tkinter import *
from tkinter import Tk, Label, Frame, Button, BOTTOM, LEFT, RIGHT, X, Y
from PIL import Image, ImageTk
from datetime import datetime

# Initialize the text-to-speech engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Load the trained model
model = cv2.face.LBPHFaceRecognizer_create()
model.read('face_recognition_model.xml')  # Update the path if needed

# Load the label dictionary
with open('labels.pickle', 'rb') as f:
    label_dict = pickle.load(f)

# If the label_dict has names as keys, reverse it to have labels as keys
label_dict = {v: k for k, v in label_dict.items()}

# Print out the label dictionary to check its contents
print("Label Dictionary:", label_dict)

# Function to map label number to person name using the loaded label dictionary
def label_to_name(label):
    return label_dict.get(label, "Unknown")

# Load the face classifier
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def equalize_histogram(image):
    return cv2.equalizeHist(image)

spoken_greetings = set()  # This set will keep track of names that have been greeted

# Function to detect face and return face with rectangle and name
def face_detector(img, size=0.5):
    global last_recognized_name
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = equalize_histogram(gray)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    # If no faces are detected, return the original img and an empty list
    if len(faces) == 0:
        last_recognized_name = "Unknown"
        return img, []

    for (x, y, w, h) in faces:
        # Draw rectangle around the face
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Crop the face within the rectangle
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200, 200))
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        # Apply histogram equalization to the ROI as well
        roi_gray = equalize_histogram(roi_gray)

        try:
            label, confidence = model.predict(roi_gray)

            # Determine if the face is known based on the confidence score
            if confidence < 65.5:  # You may need to adjust this threshold
                name = label_to_name(label)
                if name not in spoken_greetings:
                    greeting_message = f"Hi {name}, good morning! Welcome to campus."
                    speak(greeting_message)
                    spoken_greetings.add(name)  # Remember that this name has been greeted
            else:
                name = "Unknown"
                if "Unknown" not in spoken_greetings:
                    greeting_message = "Hi! Welcome to campus, please press visitor button to tell purpose of coming and for any query you can visit Query Section."
                    speak(greeting_message)
                    spoken_greetings.add("Unknown")  # Remember that an unknown person has been greeted

            last_recognized_name = name  # Update the last recognized name

            confidence_text = f"{confidence:.2f}%"

            # Calculate position for the name and confidence text
            text_x = x
            text_y = y + h + 20
            # Draw filled rectangle for the text
            cv2.rectangle(img, (text_x, text_y + 5), (text_x + w, text_y - 35), (0, 255, 0), cv2.FILLED)
            # Put the name and confidence on the filled rectangle
            cv2.putText(img, f"{name}", (text_x, text_y - 18), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(img, f"{confidence_text}", (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        except Exception as e:
            print(str(e))

    return img, roi

# Updated Function to save attendance
def save_attendance(name):
    if name == "Unknown":
        speak("You can't take attendance.")
        return

    excel_file = 'attendance.xlsx'
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    try:
        df = pd.read_excel(excel_file)
        # Check if the person has already been marked today
        if not ((df['Name'] == name) & (df['Date'] == date_str)).any():
            new_data = pd.DataFrame({'Name': [name], 'Date': [date_str], 'Time': [time_str]})
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_excel(excel_file, index=False)
            speak(f"Attendance saved for {name}")
        else:
            speak(f"{name}'s attendance for today is already recorded.")
    except FileNotFoundError:
        df = pd.DataFrame({'Name': [name], 'Date': [date_str], 'Time': [time_str]})
        df.to_excel(excel_file, index=False)
        speak(f"Attendance saved for {name}")


# Function to save visitor information
def save_visitor_info(name, contact, purpose):
    excel_file = 'visitor_info.xlsx'
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    visitor_data = pd.DataFrame([[name, contact, purpose, date_time]], columns=['Name', 'Contact', 'Purpose', 'Date_Time'])
    try:
        df = pd.read_excel(excel_file)
        df = pd.concat([df, visitor_data], ignore_index=True)
    except FileNotFoundError:
        df = visitor_data
    df.to_excel(excel_file, index=False)
    print(f"Visitor information saved for {name} at {date_time}")


def capture_voice(name_entry, contact_entry, purpose_text):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak now, the microphone is listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Recognizing speech...")
            transcription = recognizer.recognize_google(audio)
            print(f"Transcription: {transcription}")

            # Insert the transcription into the 'Purpose' field regardless of content.
            # This does not require splitting into name and contact.
            purpose_text.delete("1.0", END)  # Clear the current content
            purpose_text.insert("1.0", transcription)  # Insert new content
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An exception occurred: {e}")

# Function to create and open the Visitor Information window
def open_visitor_window():
    visitor_window = Toplevel()
    visitor_window.title('Visitor Information')

    # Load your university logo image
    uni_logo_image = ImageTk.PhotoImage(Image.open('uni1.png'))  # Replace 'uni_logo.png' with your logo image path

    # University Logo Label
    uni_logo_label = Label(visitor_window, image=uni_logo_image)
    uni_logo_label.pack(side=TOP, fill=X)

    # Name Entry
    name_label = Label(visitor_window, text="Name:", font=('times new roman', 12))
    name_label.pack()
    name_entry = Entry(visitor_window, font=('times new roman', 12))
    name_entry.pack(pady=5)

    # Contact Entry
    contact_label = Label(visitor_window, text="CNIC/Contact:", font=('times new roman', 12))
    contact_label.pack()
    contact_entry = Entry(visitor_window, font=('times new roman', 12))
    contact_entry.pack(pady=5)

    # Purpose Entry
    purpose_label = Label(visitor_window, text="Purpose of Visit:", font=('times new roman', 12))
    purpose_label.pack()
    purpose_text = Text(visitor_window, height=4, width=40)
    purpose_text.pack(pady=5)

    # Save Visitor Information Function
    def save_visitor_data():
        name = name_entry.get().strip()
        contact = contact_entry.get().strip()
        purpose = purpose_text.get("1.0", END).strip()
        if name and contact and purpose:  # Check all fields are filled
            save_visitor_info(name, contact, purpose)
            name_entry.delete(0, END)
            contact_entry.delete(0, END)
            purpose_text.delete("1.0", END)
            status_message = "Information saved successfully."
            status_label.config(text=status_message, fg="green")
        else:
            status_message = "Please fill out all fields."
            status_label.config(text=status_message, fg="red")

        # Use the speak function to vocalize the status message
        speak(status_message)

    # Save Button
    save_button = Button(visitor_window, text="Save Information", command=save_visitor_data)
    save_button.pack(pady=5)

    # Voice Capture Button
    voice_button = Button(visitor_window, text="Capture Voice",
                          command=lambda: capture_voice(name_entry, contact_entry, purpose_text))
    voice_button.pack(pady=5)

    # Status Label
    status_label = Label(visitor_window, text="", fg="red")
    status_label.pack()

    # Prevent image garbage collection
    visitor_window.uni_logo_image = uni_logo_image

# Tkinter GUI functions
# Tkinter GUI functions
def attendance():
    global last_recognized_name
    if last_recognized_name != "Unknown":
        save_attendance(last_recognized_name)
    else:
        print("Unknown face. No attendance registered.")

def visitor():
    open_visitor_window()

# Initialize last recognized name as Unknown
last_recognized_name = "Unknown"

# Initialize the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("Could not open webcam")

# Function placeholders
# Tkinter GUI functions
def attendance():
    global last_recognized_name
    if last_recognized_name != "Unknown":
        save_attendance(last_recognized_name)
    else:
        print("Unknown face. No attendance registered.")

def visitor():
    open_visitor_window()

# Initialize last recognized name as Unknown
last_recognized_name = "Unknown"

# Initialize the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("Could not open webcam")


# GUI Code for Main Window
root = Tk()
root.geometry('463x295+463+215')  # Adjust the window size as necessary
root.title('Face Recognition')

# Configure the grid layout manager
root.grid_rowconfigure(0, weight=1)  # Give the video label row the ability to expand
root.grid_rowconfigure(1, weight=0)  # Prevent the button frame row from expanding
root.grid_columnconfigure(0, weight=1)  # Make sure the column expands with the window

# Create a label in the main window to hold the video frames
video_label = Label(root)
video_label.grid(row=0, column=0, sticky="nsew")  # Stick to all sides of the cell

# Function to update the video frames in the label
def video_stream():
    ret, frame = cap.read()
    if ret:
        cv_image, _ = face_detector(frame)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_image)
        imgtk = ImageTk.PhotoImage(image=pil_image)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    video_label.after(10, video_stream)

# Start the video stream
video_stream()

# Create a frame for the buttons
button_frame = Frame(root)
button_frame.grid(row=1, column=0, sticky="ew")  # Stick to east and west (left and right) sides of the cell

# Create Attendance and Visitor buttons and place them in the button frame
attendance_button = Button(button_frame, text="Attendance", command=attendance)
attendance_button.pack(side='left', padx=10, pady=2)

visitor_button = Button(button_frame, text="Visitor", command=visitor)
visitor_button.pack(side='right', padx=10, pady=2)

print("GUI setup complete. Starting mainloop...")
root.mainloop()
print("Mainloop ended. Cleaning up...")

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
print("Resources released. Program ended.")