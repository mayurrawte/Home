import json
import requests
from bs4 import BeautifulSoup
import datetime
import collections


def getStationsFromTrainNumber(trainNo,jDate=datetime.date.today().strftime('%d-%b-%Y'),jDateDay=str(datetime.date.today().strftime('%A')[:3]).upper()):
    data = {'trainNo': trainNo, 'jDate': jDate, 'jDateMap': jDate,'jDateDay': jDateDay}
    stationsList = collections.OrderedDict()
    r = requests.post('https://enquiry.indianrail.gov.in/mntes/q?opt=TrainRunning&subOpt=FindStationList',data=data)
    soup = BeautifulSoup(r.text,'html.parser')
    stations = soup.find(id='jStation').find_all('option')[1:]
    for station in stations:
        stationsList[station.get('value')] = station.text
    finaldata = {}
    finaldata['stations'] = stationsList
    finaldata['originalReq'] = data
    return json.dumps(finaldata)


def TrainRunningStatus(trainNo, jStation, jDate, jDateMap, jDateDay):
    data = {'trainNo': trainNo, 'jStation': jStation, 'jDate': jDate, 'jDateMap': jDate, 'jDateDay': jDateDay}
    r = requests.post('https://enquiry.indianrail.gov.in/mntes/q?opt=TrainRunning&subOpt=ShowRunC', data=data)
    soup = BeautifulSoup(r.text, 'lxml')
    print(soup.find(id='ResTab').text)



trainNo = raw_input('enter train number')
data = json.loads(getStationsFromTrainNumber(trainNo))
station = raw_input("Select any station from "+ data['stations'] )
TrainRunningStatus(data['originalReq']['trainNo'], station, data['originalReq']['jDate'], data['originalReq']['jDateMap'], data['originalReq']['jDateDay'])


