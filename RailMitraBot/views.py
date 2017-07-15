# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from pprint import pprint
import railapi
import requests
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic


# Create your views here.
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
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        obj = open('incomingpostmessage.txt', 'w+')
        obj.write(json.dumps(incoming_message))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                ob = open('lastlog.txt','w+')
                ob.write(json.dumps(message))
                command_type = 0
                if 'message' in message:
                    if 'text' in message['message']:
                        try:
                            trainNo, Station = str(message['message']['text']).split()
                            command_type = 1
                        except ValueError:
                            errmsg = "Hi! Main Hu tumhara RailMitra. Train ki jaankari ke liye reply with \n TrainNumber <space> StationName \n Eg. 11057 Bhopal"
                            command_type = 0
                        if command_type:
                            #data = json.loads(railapi.getStationsFromTrainNumber(trainNo))
                            #btnar = []
                            data = railapi.TrainRunningStatus(trainNo, Station)
                            ob = open('test.txt', 'w+')
                            ob.write(json.dumps(data))
                            postback_reply(message['sender']['id'], message['postback']['payload'])
                            #def pps(k, v):
                            #    payload = json.dumps({"jStation": k, "prevData": data['originalReq']})
                            #    btnar.append({"type": "postback", "title": v, "payload": payload})
                            #[pps(k, v) for k, v in data['stations'].iteritems() if Station.lower() in v.lower()]
                            #post_button(message['sender']['id'], btnar)
                            #post_facebook_message(message['sender']['id'], message['message']['text'], 1)
                        else:
                            post_facebook_message(message['sender']['id'], errmsg, 1)
                    else:
                        post_facebook_message(message['sender']['id'], message['message']['attachments'], 2)
                elif 'postback' in message:
                    #left work
                    postback_reply(message['sender']['id'], message['postback']['payload'])
        return HttpResponse()

#a = '{"jStation": "BAU#false", "prevData": {"jDateDay": "FRI", "trainNo": "11057", "jDate": "14-Jul-2017", "jDateMap": "14-Jul-2017"}}'

def postback_reply(fbid, data):
    data = json.loads(data)
    resultData = railapi.TrainRunningStatus(data['prevData']['trainNo'], data['jStation'], data['prevData']['jDate'], data['prevData']['jDateMap'], data['prevData']['jDateDay'])
    post_message_url = 'https://graph.facebook.com/v2.9/me/messages?access_token=EAAcQ73ZA7PfgBALIekJFW8zudPg9XKdG7oNGA2aR33sRqKEppHrVBY5UCGsxNHqe2PyI4qRy9yoJa3UoUJ9NCvoPl5t6SLxV5OYmEX4GnHtZACX0SBq6N29YdVQLDTqX0SE1FfhDNSdxbWGEk1ZB9l1MC6DxZCqygNaROQF3IZA4pJd69rqvj'
    rsData = {"recipient": {"id": fbid }, "message": {"attachment": {"type": "template", "payload": {"template_type": "generic", "elements": [{"title": resultData['trainName'] + " is "+ resultData['delayTime'] +" Arrival : "+ resultData['actArTime'][-5:] +" Actual : "+ resultData['schArTime'][-5:], "image_url": "http://toons.artie.com/gifs/arg-newtrain-crop.gif", "subtitle": resultData['lastLocation'] } ] } } } }
    #response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"attachment": {"type": "template", "payload": {"template_type": "button", "text": "What do you want to do next?", "buttons": btnarr}}}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=json.dumps(rsData))
    print(status.json())


def post_button(fbid, btnarr):
    post_message_url = 'https://graph.facebook.com/v2.9/me/messages?access_token=EAAcQ73ZA7PfgBALIekJFW8zudPg9XKdG7oNGA2aR33sRqKEppHrVBY5UCGsxNHqe2PyI4qRy9yoJa3UoUJ9NCvoPl5t6SLxV5OYmEX4GnHtZACX0SBq6N29YdVQLDTqX0SE1FfhDNSdxbWGEk1ZB9l1MC6DxZCqygNaROQF3IZA4pJd69rqvj'
    # response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": "maakda nai chal raha"}})
    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"attachment": {"type": "template", "payload": {"template_type": "button", "text": "Select the Station", "buttons": btnarr}}}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    print(status.json())


def post_facebook_message(fbid, recevied_message, mtype):
    post_message_url = 'https://graph.facebook.com/v2.9/me/messages?access_token=EAAcQ73ZA7PfgBALIekJFW8zudPg9XKdG7oNGA2aR33sRqKEppHrVBY5UCGsxNHqe2PyI4qRy9yoJa3UoUJ9NCvoPl5t6SLxV5OYmEX4GnHtZACX0SBq6N29YdVQLDTqX0SE1FfhDNSdxbWGEk1ZB9l1MC6DxZCqygNaROQF3IZA4pJd69rqvj'
    if mtype == 1:
        response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": recevied_message}})
    elif mtype == 2:
        response_msg = json.dumps({"message": {"attachment": {"type": "image", "payload": {"url": "https://scontent.xx.fbcdn.net/v/t39.1997-6/p100x100/851587_369239346556147_162929011_n.png?_nc_ad=z-m&oh=ad2a1e37edd885afb4acd987ad8e33c6&oe=59DEDBB0"}}}, "recipient": {"id": "1346441788784848"}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())

