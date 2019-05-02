
import cv2
import numpy as np
from keras import models
from PIL import Image
from .api import send_notification

CLASSES = ['ASSAULT', 'BURGLARY', 'SHOOTING', 'ROBBERY', 'NORMAL']
DEFAULT_CLASS = 'Normal'
CONFIDENCE_THRESHOLD = 0.90
IMAGE_STACK_SIZE = 10


PREDICTION_FREQUENCY = 8  # 1-10
#Load the saved model
model = models.load_model('notifications/watcher/009-2.088-spatial.hdf5')

VID_FILE = 'notifications/watcher/Shooting050_x264.mp4'
video = cv2.VideoCapture(VID_FILE)
# video = cv2.VideoCapture(0)


def show_classification(cv2, frame, prediction):
    if prediction is None:
        return
    classes = ['Assault', 'Burglary', 'Shooting', 'Robbery', 'Normal']
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (0, 20)
    fontScale = 0.5
    fontColor = (0, 255, 0)
    lineType = 1
    ypos = 0
    ypos += 20
    cv2.putText(frame, "{}: {}".format(prediction[0], prediction[1]),
                (0, ypos),
                font,
                fontScale,
                fontColor,
                lineType)
    return
#     for klass in classes:
#         ypos += 20
#         cv2.putText(frame, "{}: {}".format(klass, prediction[classes.index(klass)]),
#                     (0, ypos),
#                     font,
#                     fontScale,
#                     fontColor,
#                     lineType)
#     return


def predict(input_data):
    prediction = model.predict(input_data)
    result = np.amax(prediction[0])
    index = np.where(prediction[0] == result)[0][0]
    klass = CLASSES[index]
    if result > CONFIDENCE_THRESHOLD:
        return prediction[0], klass, result
    else:
        return prediction[0], DEFAULT_CLASS, 1


def post_to_api(prediction):
    klass, confidence = prediction
    # post to api


def run_watcher():
    prediction_counts = [0, 0, 0, 0, 0]
    frame_count = 0
    stack = None
    last_prediction_matrix = None
    last_prediction = ('Normal', 1)
    skips = 3
    counter = 0
    while True:
        _, frame = video.read()
        im = Image.fromarray(frame, 'RGB')
        #Resizing into 128x128 because we trained the model with this image size.
        im = im.resize((224, 224))
        img_array = np.array(im)
        #Our keras model used a 4D tensor, (images x height x width x channel)
        #So changing dimension 128x128x3 into 1x128x128x3
        counter += 1
        if counter == skips:
            img_array = np.expand_dims(img_array, axis=0)
            if stack is None:
                stack = img_array
            else:
                stack = np.append(stack, img_array, axis=0)
            if stack.shape[0] == IMAGE_STACK_SIZE:
                prediction, predicted_class, confidence = predict(
                    stack)
                last_prediction_matrix = prediction
                last_prediction = predicted_class, confidence
                print(predicted_class, confidence)
                if predicted_class != 'Normal':
                        send_notification(last_prediction)
                stack = None
            counter = 0
        show_classification(cv2, frame, last_prediction)
        cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()


# plan stack up to 10 frames
# predict in the background while stacking frames
# show prediction if confidence average > 0.8 send notification
