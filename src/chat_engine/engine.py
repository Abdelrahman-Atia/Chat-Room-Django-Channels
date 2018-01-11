import json

from django.dispatch import receiver
from django.utils.translation import ugettext as _
from django.utils.module_loading import import_string
from channels.sessions import channel_session
from channels import Group

from . import messages
from . import conf


#when connect get the user for the seesion and then add it to the Room called 'Chat'
@channel_session
def on_connect(message):
    payload = message.content['text']
    message.channel_session['user'] = payload['username']
    message.reply_channel.send(messages.system(_('Welcome to the chat!')))
    Group('chat').send(messages.system(_('User %(username)s joined chat') % payload))
    Group('chat').add(message.reply_channel)

#when disconnect get the user for the seesion and then add it to the Room called 'Chat'
@channel_session
def on_disconnect(message):
    Group('chat').discard(message.reply_channel)
    Group('chat').send(messages.system(
        _('User %(user)s left chat') % message.channel_session))

#when send massege get the user for the seesion and then add it to the Room called 'Chat'
@channel_session
def on_message(message):
    payload = message.content['text']
    user = message.channel_session['user']
    message = messages.info(payload['text'], user)
    Group('chat').send(message)





def get_engine():
    return import_string(conf.CHAT_ENGINE)
