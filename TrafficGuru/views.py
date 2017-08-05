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

trafficData = {"trafficData": [{"signalName": "ALERT", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501315733/alert.png", "SignlaDescription": "This sign indicates the Alert during driving. When this signal comes, you've to be alert and drive safely. "}, {"signalName": "CROSS TRAFFIC", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501315785/cross.png", "SignlaDescription": "This  indicates cross traffic at the junctions. When this signal comes, you are supposed to drive slowly."}, {"signalName": "CROSSWALK", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501315805/crosswalk.png", "SignlaDescription": "This indicates the presence of crosswalk. You've to lower your speed as walkers may pass through the cross walk."}, {"signalName": "BICYCLE", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316033/cycle.png", "SignlaDescription": "This indicates that bicycle are used by people and we have to put our speed in control."}, {"signalName": "DANGER", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316087/danger.png", "SignlaDescription": "This sign indicates of Danger. You should not go further as there will be some risky areas."}, {"signalName": "DIRECTIONS", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316140/direction.png", "SignlaDescription": "These kind of signs indicate the directions for some particular destination."}, {"signalName": "ELECTRIC CURRENT", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316184/electricity.png", "SignlaDescription": "this sign indicates alertness as electric current is present or some kind of electric work is running nearby."}, {"signalName": "GIVE A WAY", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316245/giveaway.png", "SignlaDescription": "This sign indicates that each driver must prepare to stop if necassary to let a driver on another approach proceed."}, {"signalName": "MEDICAL FACILITIES NEARBY", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316302/medical.png", "SignlaDescription": "This sign indicates that there are some medical facilities nearby. This can be easily remembered as plus sign inidcaes Hospitals,medical stores etc."}, {"signalName": "NO PARKING", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316344/noparking.png", "SignlaDescription": "this indicates that Parking is prohibited. Here P inidcates Parking and Cut means it is not allowed."}, {"signalName": "NO SOUND", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316390/nosound.png", "SignlaDescription": "this sign indicates that blowing horn or using Loudspeakers are prohibited."}, {"signalName": "NO HIGH SPEED", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316441/nospeed.png", "SignlaDescription": "This sign indicates that your speed should not exceed the specified speed. This is used mostly in hilly areas."}, {"signalName": "NO SWIM", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316485/noswim.png", "SignlaDescription": "This sign indicates that swimming is not alllowed in that particular water body."}, {"signalName": "NO WALK", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316499/nowalk.png", "SignlaDescription": "This sign indicate that Walking is prohibited. This can normally be seen in rush places"}, {"signalName": "ONE WAY", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316516/oneway.png", "SignlaDescription": "This sign indicates that The road is one way , we can drive fast when the one way road is present."}, {"signalName": "PARKING", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316517/parking.png", "SignlaDescription": "This indicates that Parking is allowed. Here P inidcates Parking."}, {"signalName": "PHONEBOOTH", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316518/phonebooth.png", "SignlaDescription": "This indicates the phone call booth is nearby."}, {"signalName": "POSTOFFICE", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316518/postoffice.png", "SignlaDescription": "This sign indicates that post office is nearby."}, {"signalName": "ROUND ABOUT", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316520/roundabout.png", "SignlaDescription": "This sign indicate that traffic flows only in one direction."}, {"signalName": "SCHOOL NEARBY", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316520/school.png", "SignlaDescription": "this sign show that there is a school nearby"}, {"signalName": "SKATE ALLOWED", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316520/skate.png", "SignlaDescription": "This sign indicates the road is non-traffic and we might skate here."}, {"signalName": "SOUND ALLOWED", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316521/sound.png", "SignlaDescription": "This sign shows that horns are allowed."}, {"signalName": "SPEED LIMIT", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316522/speedlimit.png", "SignlaDescription": "This sign indicates the conventional speed limit."}, {"signalName": "STOP", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316522/stop.png", "SignlaDescription": "this sign indicates that the driver need to be stop. This is used where some work is in progress and we can't go further."}, {"signalName": "SWIM ALLOWED", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316523/swim.png", "SignlaDescription": "This sign indicate that Swimming is allowed."}, {"signalName": "U TURN", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316525/uturn.png", "SignlaDescription": "this indicates the U turn. It is compulsory as there’s no further destinations."}, {"signalName": "WALK", "SignalUrl": "http://res.cloudinary.com/meracloudtheonemachinearmy/image/upload/v1501316524/walk.png", "SignlaDescription": " This sign indicate that Walking is allowed. This can normally be seen in rush places."} ] }

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
                fbid = message['sender']['id']
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
                        post_facebook_message(message['sender']['id'], custresponse, 1)
                        custresponsebtn = {"recipient":{"id":fbid }, "message":{"attachment":{"type":"template", "payload":{"template_type":"button", "text":"So lets get ready !", "buttons":[{"type":"postback", "title":"READY", "payload":"Ready"} ] } } } }
                        post_facebook_message(fbid, custresponsebtn, 4)
                    elif text == 'Ready':
                        firstData = {"recipient": {"id": fbid}, "message": {"attachment": {"type": "template",
                                                                                           "payload": {
                                                                                               "template_type": "generic",
                                                                                               "elements": [{"title":
                                                                                                                 trafficData[
                                                                                                                     'trafficData'][
                                                                                                                     0][
                                                                                                                     'signalName'],
                                                                                                             "image_url":
                                                                                                                 trafficData[
                                                                                                                     'trafficData'][
                                                                                                                     0][
                                                                                                                     'SignalUrl']}]}}}}
                        post_facebook_message(fbid, firstData, 4)
                        firstDataText = trafficData['trafficData'][0]['SignlaDescription']
                        post_facebook_message(fbid, firstDataText, 1)
                        custresponsebtn = {"recipient": {"id": fbid}, "message": {"attachment": {"type": "template",
                                                                                                 "payload": {
                                                                                                     "template_type": "button",
                                                                                                     "text": "That was Great !",
                                                                                                     "buttons": [{
                                                                                                                     "type": "postback",
                                                                                                                     "title": "Next",
                                                                                                                     "payload": "1"}]}}}}
                        post_facebook_message(fbid, custresponsebtn, 4)
                    else:
                        nextData = {"recipient": {"id": fbid}, "message": {"attachment": {"type": "template",
                                                                                           "payload": {
                                                                                               "template_type": "generic",
                                                                                               "elements": [{"title":
                                                                                                                 trafficData[
                                                                                                                     'trafficData'][
                                                                                                                     int(text)][
                                                                                                                     'signalName'],
                                                                                                             "image_url":
                                                                                                                 trafficData[
                                                                                                                     'trafficData'][
                                                                                                                     int(text)][
                                                                                                                     'SignalUrl']}]}}}}
                        post_facebook_message(fbid, nextData, 4)
                        firstDataText = trafficData['trafficData'][int(text)]['SignlaDescription']
                        post_facebook_message(fbid, firstDataText, 1)
                        custresponsebtn = {"recipient": {"id": fbid}, "message": {"attachment": {"type": "template",
                                                                                                 "payload": {
                                                                                                     "template_type": "button",
                                                                                                     "text": "That was Great !",
                                                                                                     "buttons": [{
                                                                                                         "type": "postback",
                                                                                                         "title": "Next",
                                                                                                         "payload": int(text)}]}}}}
                        if text < len(trafficData['trafficData']):
                            post_facebook_message(fbid, custresponsebtn, 4)
                            post_facebook_message(fbid, custresponsebtn, 4)
                        else:
                            res = "You now have knowledge of some important traffic signals. I will update myself and get back to you. Thanks"
                            post_facebook_message(fbid, custresponsebtn, 1)
                        #custresponse = 'Ruko ! mujhe sikhne de fir tumhe sikhaata hu'
                        #post_facebook_message(message['sender']['id'], custresponse, 1)
        return HttpResponse()

def post_facebook_message(fbid, recevied_message,mtype):
    post_message_url = 'https://graph.facebook.com/v2.9/me/messages?access_token=EAAJrxDp25AwBALee6mEVe9k63GqJmZBzPaCKAPRZBJQ4lzrIbtVTWF4usMGvl77GciY2TmsMvUcyYgcM10NkaDdpn55EcYm47hz1ul4nVWsZBLGYw8RofX2WX46ZBxCHgbbfo0VS2asppm4HZBrlDv9gnmFJ7bavpPfIkoqouzdPWhztrOPlM'
    if mtype == 1:
        response_msg = json.dumps({"recipient":{"id":fbid}, "message": {"text":recevied_message}})
    elif mtype == 2:
        response_msg = json.dumps({"message": {"attachment": {"type": "image", "payload": {"url": "https://scontent.xx.fbcdn.net/v/t39.1997-6/p100x100/851587_369239346556147_162929011_n.png?_nc_ad=z-m&oh=ad2a1e37edd885afb4acd987ad8e33c6&oe=59DEDBB0"}}}, "recipient": {"id": "1346441788784848"}})
    elif mtype == 3:
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":"template", "payload":{"template_type":"button", "text":"I am so excited about this. ", "buttons":[{"type":"postback", "title":"So lets start..", "payload":"signal1"}]}}}})
    elif mtype == 4: #send as it is
        response_msg = json.dumps(recevied_message)
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

'''
def privacy(request):
    return render(request, 'privacypolicyaisha.html', context={})
'''
