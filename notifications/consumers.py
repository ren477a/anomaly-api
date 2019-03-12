from datetime import datetime
import time
import random

from channels.generic.websocket import JsonWebsocketConsumer

from .models import Notification


class NotifConsumer(JsonWebsocketConsumer):

    def notif_simulator(self):
        notif_types = Notification.TYPE_CHOICES
        cameras = [
            {"name": "lobby", "id": 1},
            {"name": "kitchen", "id": 2},
            {"name": "gate-1", "id": 3},
            {"name": "gate-2", "id": 4},
            {"name": "frontdoor", "id": 5},
        ]
        x=20
        while x>0:
            random_type = notif_types[random.randint(0, len(notif_types))-1]
            random_cam = cameras[random.randint(0, len(cameras))-1]
            self.send_json({
                "type": random_type[0],
                "timestamp": str(datetime.now()),
                "camera": random_cam
            })
            time.sleep(random.randint(0, 5))
            x -= 1

    def connect(self):
        self.accept()
        self.notif_simulator()

    def disconnect(self, close_code):
        pass

    def get_response(self, request, event_type):
        return {}

    # def log(self, log, log_type='debug'):
    #     debug(u'Consumer {}: {}'.format(
    #         self.__class__.__name__, log), websocket_request=self.get_websocket_request(), type=log_type)


    def receive_json(self, request):
        self.notif_simulator()
        self.send_json({"msg": "received"})
