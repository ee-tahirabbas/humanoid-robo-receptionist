import cv2
import numpy as np
import pickle
from os import listdir
from os.path import isdir, join


# Function to get the images and labels from the dataset
def get_images_and_labels(data_path):
    face_samples = []
    labels = []
    label_dict = {}
    current_label = 0

    person_dirs = [d for d in listdir(data_path) if isdir(join(data_path, d))]

    for person_name in person_dirs:
        person_path = join(data_path, person_name)
        onlyfiles = [f for f in listdir(person_path) if f.endswith('.jpg')]

        for image_file in onlyfiles:
            image_path = join(person_path, image_file)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if image is not None:
                face_samples.append(np.asarray(image, dtype=np.uint8))

                # Assign a label to each person's name if it hasn't been assigned before
                if person_name not in label_dict:
                    label_dict[person_name] = current_label
                    current_label += 1
                labels.append(label_dict[person_name])

    return face_samples, np.asarray(labels, dtype=np.int32), label_dict


data_path = 'C:\\Users\\PMLS\\Desktop\\facedata\\'
faces, labels, label_dict = get_images_and_labels(data_path)

# Create a LBPH face recognizer model and train it with the faces and labels
model = cv2.face.LBPHFaceRecognizer_create()
model.train(faces, labels)

print("Dataset Model Training Completed")

# Save the trained model for later use
model.save('face_recognition_model.xml')

# Save label dictionary for later use
with open('labels.pickle', 'wb') as f:
    pickle.dump(label_dict, f)