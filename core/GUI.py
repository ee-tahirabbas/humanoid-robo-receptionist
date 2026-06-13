import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk

# Load the trained model
model = cv2.face.LBPHFaceRecognizer_create()
model.read('face_recognition_model.xml')  # Make sure this is the correct path to your model

# Load the face classifier
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to map label number to person name
def label_to_name(label):
    # Update this mapping based on the names associated with your dataset labels
    names = {0: "sheri", 1: "Zubair"}  # Example mapping
    return names.get(label, "Unknown")

# Function to detect face and return face with rectangle and name
def face_detector(img, size=0.5):
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return img, []

    for (x, y, w, h) in faces:
        # Draw rectangle around the face
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Crop the face within the rectangle
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200, 200))

        try:
            # Convert the cropped face to grayscale
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            # Predict the label of the face
            label, confidence = model.predict(roi_gray)
            # Get the name of the person
            if confidence < 65:  # You may need to adjust this threshold
                name = label_to_name(label)
            else:
                name = "Unknown"

            confidence_text = f"{confidence:.2f}%"

            # Calculate position for the name and confidence text
            text_x = x
            text_y = y + h + 20
            # Draw filled rectangle for the text
            cv2.rectangle(img, (text_x, text_y + 5), (text_x + w, text_y - 35), (0, 255, 0), cv2.FILLED)
            # Put the name and confidence on the filled rectangle
            cv2.putText(img, f"{name}", (text_x, text_y - 18), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(img, f"{confidence_text}", (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX, 0.55, (255, 255, 255), 1)
        except Exception as e:
            print(str(e))

    return img, roi


# Tkinter GUI functions
def attendance():
    print("Attendance registered")

def visitor():
    print("Visitor registered")

# Create the main window
root = Tk()
root.title("Face Recognition")

# Create a frame for the buttons with a specified height
button_frame = Frame(root, height=150)  # Adjust the height as needed
button_frame.pack(side=BOTTOM, fill=X)

# Add padding inside the frame where buttons are packed to move them up
attendance_button = Button(button_frame, text="Staff Attendance", command=attendance)
attendance_button.pack(side=LEFT, padx=150, pady=5)  # Add padding as needed

visitor_button = Button(button_frame, text="Visitor section", command=visitor)
visitor_button.pack(side=RIGHT, padx=150, pady=20)  # Add padding as needed

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

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Start the video stream
video_stream()

# Start the Tkinter main loop
root.mainloop()

# When the mainloop of Tkinter ends (window is closed), release the resources
cap.release()
cv2.destroyAllWindows()
