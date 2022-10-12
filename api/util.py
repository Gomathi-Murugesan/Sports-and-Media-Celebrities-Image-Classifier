import pickle
import json
import numpy as np
import base64
import cv2
from api.wavelet import w2d

__class_name_to_number = {}
__class_number_to_name = {}

__model = None ### private variable to the python file..used to store model

def classify_image(base64_image_data, file_path=None):
    load_saved_artifacts()
    images = get_cropped_image_if_2_eyes(file_path, base64_image_data)

    result = []
    for image in images:
        scaled_raw_image = cv2.resize(image, (32, 32))
        image_har = w2d(image, 'db1', 5)
        scaled_image_har = cv2.resize(image_har, (32, 32))
        combined_image = np.vstack((scaled_raw_image.reshape(32 * 32 * 3, 1), scaled_image_har.reshape(32 * 32, 1)))

        len_image_array = 32*32*3 + 32*32

        final = combined_image.reshape(1,len_image_array).astype(float)
        ### normally to a model we will send 2d array.. but here we are going to send only one image..
        ### so we are reshaping to (1, len_image_array)

        ### we send the final image to predict method of our model..
        ### model gives array as output.. we need only first element from the array
        ### our model gives number, so we use number_to_name function to get name from the number
        ### result.append(class_number_to_name(__model.predict(final)[0]))
        result.append({
            'class': class_number_to_name(__model.predict(final)[0]),
            'class_probability': np.around(__model.predict_proba(final) * 100, 2).tolist()[0],
            'class_dictionary': __class_name_to_number ## this we need to send to our website
        })

        ## predict_proba method gives probability of all classification
    return result

def class_number_to_name(class_num):
    return __class_number_to_name[class_num]

### this function is to load model and output_class_dict from artifacts
### our output_class_dict has both number and name.. we are using both number_to_name conversion and name_to_number_conversion
def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __class_name_to_number
    global __class_number_to_name

    with open("./api/artifacts/class_dictionary.json", "r") as f:
        __class_name_to_number = json.load(f)
        __class_number_to_name = {v:k for k,v in __class_name_to_number.items()}

    global __model
    if __model is None:
        with open('./api/artifacts/svm_classifier_model.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")

def get_cv2_image_from_base64_string(b64str):
    '''
    This code takes base64 string of a image and decodes them and give cv2 image.
    we use that cv2 image to crop if two eyes are present
    '''
    encoded_data = b64str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def get_cropped_image_if_2_eyes(image_path, base64_image_data):
    face_cascade = cv2.CascadeClassifier('./api/opencv/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('./api/opencv/haarcascades/haarcascade_eye.xml')

    if image_path:
        img = cv2.imread(image_path)
    else:
        img = get_cv2_image_from_base64_string(base64_image_data)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    cropped_faces = []
    for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            if len(eyes) >= 2:
                cropped_faces.append(roi_color)
    return cropped_faces

def get_base64_test_image():
    with open("b64.txt") as f:
        return f.read()

if __name__ == '__main__':
    load_saved_artifacts()
    print(classify_image(get_base64_test_image(), None))