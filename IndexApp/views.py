# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render
import sendgrid
import os

from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from sendgrid.helpers.mail import *
# Create your views here.

def index(request):
    return render(request, 'indexPage.html', context={})

@csrf_exempt
def sendMail(request):
    if request.is_ajax():
        sg = sendgrid.SendGridAPIClient(apikey='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')
        name = request.POST['name']
        email = request.POST['email']
        type = request.POST['type']
        message = request.POST['message']
        if type == 'help':
            from_email = Email("helpme@some-one.me")
            subject = name + "is seeking for the help !"
        elif type =='hire':
            from_email = Email("hire@some-one.me")
            subject = 'I want to hire you'
        else:
            from_email = Email("dontknow@some-one.me")
            subject = " !!!!!!"
        to_email = Email("rawte.mayur@gmail.com")
        content = Content("text/plain", message + " \n email " + email)
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        resData = {'status': response.status_code, 'body': response.body}
        return JsonResponse(resData, safe=False)