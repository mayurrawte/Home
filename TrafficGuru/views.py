# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import requests
from pprint import pprint
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

trafficSignals = {'1': {'image': 'url1.png', 'instruction': 'SomeRandomInstructions'}}


class TrafficGuruView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '2318934571':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    obj = open('traffictest.txt', 'w+')
                    obj.write(str(message))
                    if 'text' in message['message']:
                        data = 'heh'
                        #post_facebook_message(message['sender']['id'], message['message']['text'], 1)
                        post_facebook_message(message['sender']['id'], data, 1)
                    else:
                        post_facebook_message(message['sender']['id'], message['message']['attachments'], 2)
                elif 'postback' in message:
                    text = message['postback']['payload']
                    if text == 'GET_STARTED_PAYLOAD':
                        custresponse = 'Hi! Nice to see you here. I am TrafficGuru. Yeah Thats what my friends call me coz i know everything about traffic, and probably you are here to get some knowledge about traffic signals. No worries i will master you in that. So lets Start.'
                    else:
                        custresponse = 'Ruko ! mujhe sikhne de fir tumhe sikhaata hu'
                    post_facebook_message(message['sender']['id'], custresponse, 1)
        return HttpResponse()

def post_facebook_message(fbid, recevied_message,mtype):
    post_message_url = 'https://graph.facebook.com/v2.9/me/messages?access_token=EAAJrxDp25AwBALee6mEVe9k63GqJmZBzPaCKAPRZBJQ4lzrIbtVTWF4usMGvl77GciY2TmsMvUcyYgcM10NkaDdpn55EcYm47hz1ul4nVWsZBLGYw8RofX2WX46ZBxCHgbbfo0VS2asppm4HZBrlDv9gnmFJ7bavpPfIkoqouzdPWhztrOPlM'
    if mtype == 1:
        response_msg = json.dumps({"recipient":{"id":fbid}, "message": {"text":recevied_message}})
    elif mtype == 2:
        response_msg = json.dumps({"message": {"attachment": {"type": "image", "payload": {"url": "https://scontent.xx.fbcdn.net/v/t39.1997-6/p100x100/851587_369239346556147_162929011_n.png?_nc_ad=z-m&oh=ad2a1e37edd885afb4acd987ad8e33c6&oe=59DEDBB0"}}}, "recipient": {"id": "1346441788784848"}})
    elif mtype == 3:
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":"template", "payload":{"template_type":"button", "text":"I am so excited about this. ", "buttons":[{"type":"postback", "title":"So lets start..", "payload":"signal1"}]}}}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


def privacy(request):
    return render(request, 'privacypolicyaisha.html', context={})

