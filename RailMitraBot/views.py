# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render
import railapi
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import apiai

token = '5e47a85828a0400aa52a591ca95820f1'
ai = apiai.ApiAI(token)


def privacypolicy(request):
    return render(request, 'privacypolicyrailmitra.html', context={})

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
        obj = open("incomingpostmessage.txt", "w+") # message logging
        obj.write(json.dumps(incoming_message))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                fbid = message['sender']['id']
                if 'message' in message:
                    if 'text' in message['message']:
                        text = message['message']['text']
                        airequest = ai.text_request()
                        airequest.session_id = fbid
                        airequest.query = text
                        airesponse = airequest.getresponse()
                        airesponsetext = json.loads(airesponse.read())
                        try:
                            if airesponsetext['result']['metadata']['intentName'] == 'LiveStation':
                                if airesponsetext['result']['parameters']['sourceStation'] == '' or airesponsetext['result']['parameters']['DestinationStation'] == '':
                                    railapi.post_facebook_message_normal(fbid, "Something is missing ! Type 'help' for supported commands")
                                else:
                                    railapi.getStationNamesforliveStation(fbid, airesponsetext['result']['parameters']['sourceStation'], airesponsetext['result']['parameters']['DestinationStation'], 1)
                            elif airesponsetext['result']['metadata']['intentName'] == 'TrainStatus':
                                if airesponsetext['result']['parameters']['trainNumber'] == '' or airesponsetext['result']['parameters']['boardingStation'] == '':
                                    railapi.post_facebook_message_normal(fbid, "Something is missing ! Type 'help' for supported commands")
                                else:
                                    running_status(fbid, airesponsetext['result']['parameters']['trainNumber'], airesponsetext['result']['parameters']['boardingStation'])
                            elif airesponsetext['result']['metadata']['intentName'] == 'What Can I ask':
                                intentText = 'You can start asking me \n Who are you? \n Who is your boss? \n you are fired ? \n You are bad \n What\'s your birth date? \n are you busy? \n can you help me? \n you are good. \n are you happy? \n do you have a hobby? \n are you hungy? \n are we friends? \n where do you live? \n For more commands reply with More'
                                railapi.post_facebook_message_normal(fbid, intentText)
                                return HttpResponse()
                            elif airesponsetext['result']['metadata']['intentName'] == 'More Intents':
                                intentText = 'Some more Commands are \n I am very angry right now. \n I am back \n I am bored \n I am busy \n I can\'t sleep \n I am here \n I like you. \n I am so lonely \n what do i look like \n I love you. \n I need an advice \n I am sad \n I am sleepy. \n I am just testing you. \n Give me a hug. \n You are wrong. \n'
                                railapi.post_facebook_message_normal(fbid, intentText)
                                return HttpResponse()
                            elif airesponsetext['result']['metadata']['intentName'] == 'help':
                                i_need_help(fbid)
                            elif airesponsetext['result']['metadata']['intentName'] == 'introduction':
                                railapi.defaultMessage(fbid)
                            else:
                                print airesponsetext['result']['metadata']['intentName']
                                railapi.post_facebook_message_normal(fbid, airesponsetext['result']['fulfillment']['speech'])
                        except:
                            railapi.post_facebook_message_normal(fbid, airesponsetext['result']['fulfillment']['speech'])
                    elif 'attachments' in message['message']:
                        data = {"attachment": {"type": "image", "payload": {
                            "url": "https://scontent.xx.fbcdn.net/v/t39.1997-6/851557_369239266556155_759568595_n.png?_nc_ad=z-m&oh=dc20f0f3ab1494f22a217cdbbdd41561&oe=59FF76DC"}}}
                        railapi.sendAttachment(fbid, data)
                    else:
                        railapi.post_facebook_message_normal(message['sender']['id'], message['message']['attachments'])
                elif 'postback' in message:
                    if message['postback']['payload'].lower() == 'help':
                        i_need_help(fbid)
                    elif message['postback']['payload'].lower() == 'hi':
                        railapi.defaultMessage(fbid)
                    elif message['postback']['payload'].lower() == 'talk to me':
                        intentText = 'You can start asking me \n Who are you? \n Who is your boss? \n you are fired ? \n You are bad \n What\'s your birth date? \n are you busy? \n can you help me? \n you are good. \n are you happy? \n do you have a hobby? \n are you hungy? \n are we friends? \n where do you live? \n For more commands reply with More'
                        railapi.post_facebook_message_normal(fbid, intentText)
                    else:
                        data = json.loads(message['postback']['payload'])
                        if 'validStationFrom' in data and not 'validStationTo' in data:
                            railapi.getStationNamesforliveStation(fbid, data['validStationFrom'], data['stationTo'], 2)
                        elif 'validStationFrom' in data and 'validStationTo' in data:
                            railapi.getLiveStation(fbid, data['validStationFrom'], data['validStationTo'])
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
    #railapi.post_facebook_message_normal(fbid, "Ruk bhai karta hu teri madad")
    rsData = {"recipient": {"id": fbid}, "message": {"attachment": {"type": "template",
                                                                    "payload": {"template_type": "generic",
                                                                                "elements": [{"title": "I am here to help you !",
                                                                                              "image_url": "https://s-media-cache-ak0.pinimg.com/736x/1a/22/8a/1a228a1d771c36dbe7b301a5a1d608fa--cv-writing-service-writing-services.jpg",
                                                                                              "subtitle": "Below are some queries you can ask me"}]}}}}
    railapi.post_generic_template(rsData)

    #rsData = {"recipient": {"id": fbid}, "message": {"attachment": {"type": "template",
     #                                                               "payload": {"template_type": "generic",
     #                                                                           "elements": [{
     #                                                                                            "title": "FromStation <space> to <space> ToStation , Example : Bhopal to Burhanpur",
     ##                                                                                            "image_url": "https://ci.memecdn.com/9785823.jpg",
      #                                                                                           "subtitle": "For Train between these station in next 4 hours"}]}}}}
    #railapi.post_generic_template(rsData)
    railapi.post_facebook_message_normal(fbid, "For Running train status you can ask \n\nFind status for 11057 at bhopal \n\nGet me live status for 11057 at Bhopal \n\nI am at Bhopal station waiting for 11057 ")
    railapi.post_facebook_message_normal(fbid, "For Trains between status within next 4 hours \n\nLive station for bhopal to goa \n\nTrain between Bhopal to goa \n\nBhopal to goa or as you wish to ask me")
