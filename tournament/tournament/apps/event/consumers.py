from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json


class EventConsumer(WebsocketConsumer):
    def connect(self):
        self.event_name = self.scope["url_route"]["kwargs"]["event_name"]
        self.event_group_name = "chat_%s" % self.event_name

        # Join event group
        async_to_sync(self.channel_layer.group_add)(
            self.event_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave event group
        async_to_sync(self.channel_layer.group_discard)(
            self.event_group_name, self.channel_name
        )

    def receive_json(self, content):
        command = content.get("command", None)

        if command == "event_updated":
            async_to_sync(self.channel_layer.group_send)(
                self.event_group_name, {"type": "event_updated"}
            )


