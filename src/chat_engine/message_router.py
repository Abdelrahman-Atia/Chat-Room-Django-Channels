import json

from django.dispatch import receiver
from django.utils.module_loading import import_string

from channels import Channel

from . import conf


class MessageRouter:

#Check the Action Type and then call the requird engine function to handle the action
    def handle_receive(self, message):
        message, payload = self.decode_message(message)
        action = payload['type']

        if action == "connect":
            self.route('chat.connect', message)

        elif action == 'message':
                self.route('chat.message', message)

#call the disconnect function when the user leaves
    def handle_disconnect(self, message):
        self.route('chat.disconnect', message)

# parse the received massege
    def decode_message(self, message):
        payload = json.loads(message.content['text'])
        message.content['text'] = payload
        return message, payload

    def route(self, channel, message):
        Channel(channel).send(message.content)


def get_router(*args, **kwargs):
    return import_string(conf.CHAT_ROUTER)(*args, **kwargs)
