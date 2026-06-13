import cv2
import numpy as np
import pickle

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

# Function to detect face and return face with rectangle and name
def face_detector(img, size=0.5):
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = equalize_histogram(gray)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    # If no faces are detected, return the original img and an empty list
    if len(faces) == 0:
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
            else:
                name = "Unknown"

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

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Use the face_detector function to get the frame with the drawn rectangles and names
    image, _ = face_detector(frame)

    # Display the resulting frame
    cv2.imshow('Face Recognition', image)

    # Break the loop with the 'Enter' key
    if cv2.waitKey(1) == 13:
        break


# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()