import json
import requests
from bs4 import BeautifulSoup
import datetime
import collections

page_url_with_token = 'https://graph.facebook.com/v2.9/me/messages?access_token=EAAcQ73ZA7PfgBALIekJFW8zudPg9XKdG7oNGA2aR33sRqKEppHrVBY5UCGsxNHqe2PyI4qRy9yoJa3UoUJ9NCvoPl5t6SLxV5OYmEX4GnHtZACX0SBq6N29YdVQLDTqX0SE1FfhDNSdxbWGEk1ZB9l1MC6DxZCqygNaROQF3IZA4pJd69rqvj'

def getStationsFromTrainNumber(trainNo,jDate=datetime.date.today().strftime('%d-%b-%Y'),jDateDay=str(datetime.date.today().strftime('%A')[:3]).upper()):
    data = {'trainNo': trainNo, 'jDate': jDate, 'jDateMap': jDate,'jDateDay': jDateDay}
    stationsList = collections.OrderedDict()
    r = requests.post('https://enquiry.indianrail.gov.in/mntes/q?opt=TrainRunning&subOpt=FindStationList',data=data)
    soup = BeautifulSoup(r.text,'lxml')
    stations = soup.find(id='jStation').find_all('option')[1:]
    for station in stations:
        stationsList[station.get('value')] = station.text
    finaldata = {}
    finaldata['stations'] = stationsList
    finaldata['originalReq'] = data
    return json.dumps(finaldata)


def TrainRunningStatus(trainNo, jStation, jDate=datetime.date.today().strftime('%d-%b-%Y'), jDateMap=datetime.date.today().strftime('%d-%b-%Y'), jDateDay=str(datetime.date.today().strftime('%A')[:3]).upper()):
    data = {'trainNo': trainNo, 'jStation': jStation, 'jDate': jDate, 'jDateMap': jDate, 'jDateDay': jDateDay}
    r = requests.post('https://enquiry.indianrail.gov.in/mntes/q?opt=TrainRunning&subOpt=ShowRunC', data=data)
    soup = BeautifulSoup(r.text, 'lxml')
    resultData = {}
    try:
        table = soup.find(id='ResTab')
        trs = table.find_all('tr')
        trainName = trs[0].find_all('td')[1].text
        stationName = trs[1].find_all('td')[1].text
        schArTime = trs[3].find_all('td')[1].text
        actArTime = trs[4].find_all('td')[1].text
        delayTime = trs[5].find_all('td')[1].text
        lastLocation = (trs[9].find_all('td')[1].text)
        lastLocation = " ".join(lastLocation.split())
        resultData = {'trainName': trainName, 'schArTime': schArTime, 'actArTime': actArTime, 'delayTime': delayTime, 'lastLocation': lastLocation, 'stationName': stationName}
    except:
        #err = soup.find_all(class_='errorTextL11')[0].text
        resultData['err'] = 'some error in input please check that'
    return resultData




def post_facebook_message_normal(fbid, recevied_message):
    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": recevied_message}})
    status = requests.post(page_url_with_token, headers={"Content-Type": "application/json"}, data=response_msg)
    print(status.json())

def post_facebook_buttons(fbid, data):  #this receives a array of facebook button json
    print data
    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"attachment": {"type": "template", "payload": {"template_type": "button", "text": data['text'], "buttons": data['Buttons']}}}})
    status = requests.post(page_url_with_token, headers={"Content-Type": "application/json"}, data=response_msg)
    print(status.json())

def post_running_status_reply(fbid, data):
    data = json.loads(data)
    resultData = TrainRunningStatus(data['prevData']['trainNo'], data['jStation'], data['prevData']['jDate'], data['prevData']['jDateMap'], data['prevData']['jDateDay'])
    if "err" in resultData:
        post_facebook_message_normal(fbid, resultData['err'])
        return None
    else:
        rsData = {"recipient": {"id": fbid }, "message": {"attachment": {"type": "template", "payload": {"template_type": "generic", "elements": [{"title": resultData['trainName'] + " is "+ resultData['delayTime'] +" Arrival : "+ resultData['actArTime'][-5:] +" Actual : "+ resultData['schArTime'][-5:], "image_url": "http://toons.artie.com/gifs/arg-newtrain-crop.gif", "subtitle": resultData['lastLocation'] } ] } } } }
        status = requests.post(page_url_with_token, headers={"Content-Type": "application/json"}, data=json.dumps(rsData))
        print(status.json())


def post_generic_template(data):
    data = json.load(data)
    status = requests.post(page_url_with_token, headers={"Content-Type": "application/json"}, data = data)
    print status.json()


def defaultMessage(fbid):
    NormalMessage = "Hi! I am RailMitra. I help people to get there required train information"
    post_facebook_message_normal(fbid, NormalMessage)
    text = "For more information Reply with 'help' or click button below"
    data = {"Buttons": [{"type": "postback", "title": "Help", "payload": "help"}], "text" : text}
    post_facebook_buttons(fbid, data)
