#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import datetime as dt

trv_api_key = '____Replace_IT____'

def date_minus_now(num_days):
    ''' Subtracts num_days from current date '''

    date_time_x_days = dt.datetime.now() + dt.timedelta(days=num_days)
    date_days = str(date_time_x_days.date())
    return date_days

def get_train_announcement_trv(api_key=''):
    ''' Gets train announce data from TRV '''

    url_trv = 'https://api.trafikinfo.trafikverket.se/v2/data.json'
    day_to_request = date_minus_now(-1)
    
    xml_request = '''
        <REQUEST>
            <LOGIN authenticationkey="{0}" />
            <QUERY objecttype="TrainAnnouncement" schemaversion="1.8">
                <FILTER>
                    <EQ name="InformationOwner" value="SJ" />
                    <EQ name="Advertised" value="true" />
                    <EQ name='DepartureDateOTN' value="{1}" />
                </FILTER>
            </QUERY>
        </REQUEST>'''.format(api_key, day_to_request)
    
    print(f'Request data: {xml_request}')
    headers = {'Content-Type': 'text/xml'}
    
    print('Retrieving train announcement from TRV API ...')
    response = requests.post(url_trv, data=xml_request, headers=headers)
    
    response_code = response.status_code
    if response.status_code >= 200 and response.status_code < 300:
        print(f'Valid Response received! Code: {response_code}')
        response_json = response.json()
        train_announcements = response_json.get('RESPONSE').get('RESULT')[0].get('TrainAnnouncement')
        return train_announcements
    else:
        print(f'Invalid response received! Response Code: {response_code}')
        response.raise_for_status()
        
if __name__ == '__main__':
    train_announcements = get_train_announcement_trv(trv_api_key)
    