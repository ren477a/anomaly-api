from asgiref.sync import async_to_sync
import json
import random
import time
from datetime import datetime

from channels.generic.websocket import JsonWebsocketConsumer

from .models import Notification


class Consumer(JsonWebsocketConsumer):
    pass

class NotifConsumer(Consumer):

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
        self.room_name = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = 'user_%s' % self.room_name
        # room
        print("{}".format(self.room_group_name))
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )


        self.accept()
        # self.notif_simulator()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def get_response(self, request, event_type):
        return {}

    # def log(self, log, log_type='debug'):
    #     debug(u'Consumer {}: {}'.format(
    #         self.__class__.__name__, log), websocket_request=self.get_websocket_request(), type=log_type)


    def receive_json(self, request):
        self.notif_simulator()
        self.send_json({"msg": "received"})


    def chat_message(self, event):
        message = event['message']
        print("MESSAGE RECEIVED!")
        # Send message to WebSocket
        self.send_json(message)
