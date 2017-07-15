# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import railapi
import requests
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

class RailMitraView(generic.View):
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
        #obj = open('incomingpostmessage.txt', 'w+') message loggin off
        #obj.write(json.dumps(incoming_message))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                ob = open('lastlog.txt', 'w+') #logging message
                ob.write(json.dumps(message))
                fbid = message['sender']['id']
                command_type = 0
                if 'message' in message:
                    if 'text' in message['message']:
                        text = message['message']['text']
                        messageArgs = str(text).split()
                        messageArgsLen = len(messageArgs)
                        if messageArgsLen == 1:
                            if messageArgs.strip().lower() == 'help':
                                i_need_help(fbid)
                        elif messageArgsLen == 2:
                            trainNo, station = messageArgs[0], messageArgs[1]
                            running_status(fbid, trainNo, station)
                        elif messageArgs == 3:
                            railapi.post_facebook_message_normal(fbid,'Mayur is working hard to get you live station status')
                        else:
                            railapi.defaultMessage(fbid)
                    else:
                        railapi.post_facebook_message_normal(message['sender']['id'], message['message']['attachments'])
                elif 'postback' in message:
                    pass
                    #left work
                    #railapi.postback_reply(message['sender']['id'], message['postback']['payload'])
        return HttpResponse()

def running_status(fbid, trainNo, station):
    data = json.loads(railapi.getStationsFromTrainNumber(trainNo))
    btnar = []
    ob = open('test.txt', 'w+')
    ob.write(json.dumps(data))

    def pps(k, v):
        payload = json.dumps({"jStation": k, "prevData": data['originalReq']})
        btnar.append({"type": "postback", "title": v, "payload": payload})

    [pps(k, v) for k, v in data['stations'].iteritems() if station.lower() in v.lower()]
    if not btnar:
        railapi.post_facebook_message_normal(fbid,"We did not find any related station with this train. Did you spell it correctly. Please try again ")
    else:
        railapi.post_running_status_reply(fbid, btnar[0]['payload'])


def i_need_help(fbid):
    railapi.post_facebook_message_normal(fbid, "Ruk bhai karta hu teri madad")
