#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import datetime as dt

class DataLoader:
    
    def __init__(self, api_key, num_days):
        self.api_key = api_key
        self.num_days = num_days
    
    def date_minus_now(self):
        ''' Subtracts num_days from current date '''
    
        date_time_x_days = dt.datetime.now() + dt.timedelta(days=-self.num_days)
        date_days = str(date_time_x_days.date())
        print(f'date_days: {date_days}')
        return date_days
    
    def get_train_announcement_trv(self):
        ''' Gets train announce data from TRV '''
    
        url_trv = 'https://api.trafikinfo.trafikverket.se/v2/data.json'
        day_to_request = self.date_minus_now()
                
        xml_request = '''
            <REQUEST>
                <LOGIN authenticationkey="{0}" />
                <QUERY objecttype="TrainAnnouncement" schemaversion="1.8">
                    <FILTER>
                        <EQ name="InformationOwner" value="SJ" />
                        <EQ name="Advertised" value="true" />
                        <EQ name='DepartureDateOTN' value="{1}" />
                        <EQ name="ActivityType"	value="Ankomst" />
                       
                    </FILTER>
                </QUERY>
            </REQUEST>'''.format(self.api_key, day_to_request)
        
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
    
    trv_api_key = 'adeac1acb7834c50a49f9710c3607625'
    data_loader = DataLoader(trv_api_key, 1)
    train_announcements = data_loader.get_train_announcement_trv()
    print(f'Announcement 1: {json.dumps(train_announcements[0], indent=2, ensure_ascii=False)}')
    
    data_loader_2 = DataLoader(trv_api_key, 2)
    train_announcements_2 = data_loader_2.get_train_announcement_trv()
    print(f'Announcement 1: {json.dumps(train_announcements_2[0], indent=2, ensure_ascii=False)}')
    
    
