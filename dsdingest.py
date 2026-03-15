import requests 
import os 
import time 
import csv 
import calendar 

urltoken = os.environ.get('TOKEN_API') 
timerh1 = time.localtime().tm_hour 
timerh2 = time.localtime().tm_hour 
timerm1 = time.localtime().tm_min 
timerm2 = time.localtime().tm_min + 1 
format_string_1 = "%Y-%m-%d %H:%M:%S"
session = requests.Session()
response1 = session.get(urltoken) 
jsonresponse1 = response1.json() 
access_token = jsonresponse1['result']['token'] 
print(access_token) 
currentcsv = 'newdsd.csv' 
arbitrarycounter = 1 
daysi = True 
response_list = []
fieldnames = ['speedBefore', 'speedAt','description','schedule','responseId']
linecounter = 0

try:
    #Make first file
    with open(currentcsv, 'w', newline='') as inrixcsv: 
        writer = csv.DictWriter(inrixcsv, fieldnames=fieldnames, extrasaction='ignore') 
        writer.writeheader() 
    while daysi == True: 
        #Refresh token
        if timerh1 == timerh2 and timerm1 == timerm2: 
            response = session.get(urltoken) 
            jsonresponse = response.json() 
            access_token = jsonresponse['result']['token']
            print(access_token) 
            print(timerh2, timerm2)  
        time.sleep(61) 
        #Ingest DSD data
        urldsd = os.environ.get('DSD_API').format(access_token) 
        dsdresponse = session.get(urldsd, timeout=5)
        print(dsdresponse.status_code)
        dsdjsonresponse = dsdresponse.json()
        print(dsdjsonresponse)
        timerh2 = time.localtime().tm_hour 
        timerm2 = time.localtime().tm_min + 1 
        if not dsdjsonresponse['result']['dangerousSlowdowns'] == []: 
            dsdtime = dsdjsonresponse['result']['dangerousSlowdowns'][0]['schedule']['occurrenceStartTimeUTC'][:10] + " " + dsdjsonresponse['result']['dangerousSlowdowns'][0]['schedule']['occurrenceStartTimeUTC'][11:19] 
            dsdtime = time.strptime(dsdtime, format_string_1) 
            dsdtimetoepoch = calendar.timegm(dsdtime) 
            dsdtimetomst = time.asctime(time.localtime(dsdtimetoepoch)) 
            dsdjsonresponse['result']['dangerousSlowdowns'][0]['schedule']['occurrenceStartTimeUTC'] = dsdtimetomst 
            dsdjsonresponse['result']['dangerousSlowdowns'][0]['responseId'] = dsdjsonresponse['responseId'] 
            response_list.append(dsdjsonresponse['result']['dangerousSlowdowns'][0]) 
            print(dsdjsonresponse)
            #Write to CSV
            if linecounter == 10:
                currentcsv = "newdsd" + str(arbitrarycounter) + ".csv"
                with open(currentcsv, 'w', newline='') as inrixcsv: 
                    writer = csv.DictWriter(inrixcsv, fieldnames=fieldnames, extrasaction='ignore') 
                    writer.writeheader() 
                    writer.writerows(response_list) 
                    arbitrarycounter += 1 
                    linecounter = 0
                    response_list = []
            else:
                with open(currentcsv, 'a', newline='') as inrixcsv: 
                    writer = csv.DictWriter(inrixcsv, fieldnames=fieldnames, extrasaction='ignore') 
                    writer.writerows(response_list) 
                    linecounter += 1
                    response_list = []
except Exception as e:
    print(e)
            