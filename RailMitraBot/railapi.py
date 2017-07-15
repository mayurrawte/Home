import json
import requests
from bs4 import BeautifulSoup
import datetime
import collections


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


def TrainRunningStatus(trainNo, jStation, jDate=datetime.date.today().strftime('%d-%b-%Y'),jDateDay=str(datetime.date.today().strftime('%A')[:3]).upper()):
    data = {'trainNo': trainNo, 'jStation': jStation, 'jDate': jDate, 'jDateMap': jDate, 'jDateDay': jDateDay}
    r = requests.post('https://enquiry.indianrail.gov.in/mntes/q?opt=TrainRunning&subOpt=ShowRunC', data=data)
    soup = BeautifulSoup(r.text, 'lxml')
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
    #print resultData
    return resultData


def post_facebook_message(fbid, btnarr):
    post_message_url = 'https://graph.facebook.com/v2.9/me/messages?access_token=EAAcQ73ZA7PfgBALIekJFW8zudPg9XKdG7oNGA2aR33sRqKEppHrVBY5UCGsxNHqe2PyI4qRy9yoJa3UoUJ9NCvoPl5t6SLxV5OYmEX4GnHtZACX0SBq6N29YdVQLDTqX0SE1FfhDNSdxbWGEk1ZB9l1MC6DxZCqygNaROQF3IZA4pJd69rqvj'
    #response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": "maakda nai chal raha"}})
    response_msg = json.dumps({"recipient":{"id": fbid }, "message":{"attachment":{"type":"template", "payload":{"template_type":"button", "text":"What do you want to do next?", "buttons":btnarr } } } })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    print(status.json())

