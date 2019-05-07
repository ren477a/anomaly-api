import requests
import datetime

BASE_URL = 'http://localhost:8000/'
NOTIF_URL = BASE_URL + 'notifications/'

def send_notification(prediction):
    klass, confidence = prediction
    user_id = 1
    camera_id = 1
    timestamp = str(datetime.datetime.now().isoformat())
    response = requests.post(
        NOTIF_URL, 
        data = 
            {
                "camera": 1,
                "_type": klass,
                "timestamp": str(datetime.datetime.now().isoformat())
            }
        )
