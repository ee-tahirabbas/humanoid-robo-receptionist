import cv2
import numpy as np
import pandas as pd
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime

# Load the trained model
model = cv2.face.LBPHFaceRecognizer_create()
model.read('face_recognition_model.xml')  # Update this path if needed
print("Model loaded successfully.")

# Load the face classifier
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
print("Face classifier loaded successfully.")

# Function to map label number to person name
def label_to_name(label):
    names = {0: "tahir"}  # Update this mapping as needed
    return names.get(label, "Unknown")


# Updated Function to save attendance
def save_attendance(name):
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
            print(f"Attendance saved for {name} at {date_str} {time_str}")
        else:
            print(f"{name}'s attendance for today ({date_str}) is already recorded.")
    except FileNotFoundError:
        df = pd.DataFrame({'Name': [name], 'Date': [date_str], 'Time': [time_str]})
        df.to_excel(excel_file, index=False)
        print(f"Attendance saved for {name} at {date_str} {time_str}")

# Tkinter GUI functions
def attendance():
    global last_recognized_name
    if last_recognized_name != "Unknown":
        save_attendance(last_recognized_name)
    else:
        print("Unknown face. No attendance registered.")

def visitor():
    print("Visitor registered")

# Initialize last recognized name as Unknown
last_recognized_name = "Unknown"

# Function to detect face and return face with rectangle and name
def face_detector(img, size=0.5):
    global last_recognized_name
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0:
        last_recognized_name = "Unknown"
        return img, []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200, 200))
        try:
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            label, confidence = model.predict(roi_gray)
            if confidence < 65:  # Adjust threshold as needed
                name = label_to_name(label)
            else:
                name = "Unknown"

            last_recognized_name = name  # Update the last recognized name

            confidence_text = f"{confidence:.2f}%"
            text_x = x
            text_y = y + h + 20
            cv2.rectangle(img, (text_x, text_y + 5), (text_x + w, text_y - 35), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f"{name}", (text_x, text_y - 18), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(img, f"{confidence_text}", (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX, 0.55, (255, 255, 255), 1)
        except Exception as e:
            print(f"Face detection error: {e}")
            last_recognized_name = "Unknown"
    return img, roi

# Initialize the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("Could not open webcam")

# Create a window using Tkinter
root = Tk()
root.title("Face Recognition")

# Create a label in the main window to hold the video frames
video_label = Label(root)
video_label.pack()

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
button_frame.pack(side=BOTTOM, fill=X)

# Create Attendance and Visitor buttons
attendance_button = Button(button_frame, text="Attendance", command=attendance)
attendance_button.pack(side=LEFT, padx=10, pady=10)

visitor_button = Button(button_frame, text="Visitor", command=visitor)
visitor_button.pack(side=RIGHT, padx=10, pady=10)

print("GUI setup complete. Starting mainloop...")
root.mainloop()
print("Mainloop ended. Cleaning up...")

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
print("Resources released. Program ended.")

