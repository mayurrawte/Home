# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
key = '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'
url = 'https://api.sendgrid.com/v3/mail/send'
header = {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'}

@csrf_exempt
def sendResultUrl(request):
    data = {
        "personalizations":
            [
                {"to":
                     [
                         {"email": str(request.POST.get('to'))}
                     ]
                }
            ],
        "from":
            {"email": "no-reply@zingur.me"},
            "subject": "Zingur Challange Result Link",
        "content":
            [
                {"type": "text/plain", "value": "Hey " + str(request.POST.get('name')) + "\n Your quiz successfully created and ready to be shared with your friends.\n Result this quiz can be accessed by using this link \n " + str(request.POST.get('resulturl')) + "\n Thank You"}
            ]
    }
    r = requests.post(url, data=json.dumps(data), headers=header)
    return HttpResponse(r.status_code)

def contactMe(request):
    data = {"personalizations": [{"to": [{"email": "m.r.rawte7@gmail.com"}]}], "from": {"email": "contactme@zingur.me"},
            "subject": "ContactMe from zingur", "content": [{"type": "text/plain", "value": "Name" + str(request.POST.get('name')) + "Email :" + str(request.POST.get('email')) + "Message : " + str(request.POST.get('message'))}]}
    r = requests.post(url, data=json.dumps(data), headers=header)
    return HttpResponse(r.status_code)