import cv2
import os

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def equalize_histogram(image):
    return cv2.equalizeHist(image)
def face_extractor(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = equalize_histogram(gray)  # Apply histogram equalization to the grayscale image
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0:
        return None
    for (x, y, w, h) in faces:
        cropped_face = img[y:y+h, x:x+w]
    return cropped_face

# Get user input for person's name or identifier
person_name = input("Enter the person's name: ")
# Get user input for the lighting condition
lighting_condition = input("Enter the lighting condition (day, night, indoors, outdoors): ")

# Create a directory for the person if it does not exist
data_path = 'C:\\Users\\PMLS\\Desktop\\facedata\\' + person_name
if not os.path.exists(data_path):
    os.makedirs(data_path)

cap = cv2.VideoCapture(0)
count = 0

while True:
    ret, frame = cap.read()
    if face_extractor(frame) is not None:
        count += 1
        face = cv2.resize(face_extractor(frame), (200, 200))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        face = equalize_histogram(face)  # Apply histogram equalization to the face image

        # Update file name to include the person's name and lighting condition
        file_name_path = data_path + '\\' + person_name + '' + lighting_condition + '' + str(count) + '.jpg'

        cv2.imwrite(file_name_path, face)

        cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Face Cropper', face)
    else:
        print("Face not found")
        pass

    if cv2.waitKey(1) == 13 or count == 100:  # Adjusted to 100 for quick testing, can be changed back to 200
        break

cap.release()
cv2.destroyAllWindows()
print(f'Samples Collection Completed for {person_name} under {lighting_condition} conditions.')