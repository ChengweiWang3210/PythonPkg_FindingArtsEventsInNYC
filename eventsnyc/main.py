import requests
import numpy as np
import pandas as pd
import os
from xml.dom import minidom
import xml.etree.ElementTree as ET


class eventsNearMe():

    def __init__(self):
        self.location = 'New York City'
        self.results = None
        self.lat = 40.7581
        self.lon = -73.9855

    def get_event_near_me(self,
                          lat=40.7581,
                          lon=-73.9855,
                          current_only=False,
                          free_only=False,
                          description_only=False,
                          distance_range=3000,
                          display_language='en',
                          num_results=10,
                          sort_by="distance"):
        """
        This function will return events in NYC around the location users put in the function.

        PARAMETERS
        --------
        lat: string. latitude
        lon: string. longitude
        current_only: boolean. if True, return only events that have already opened
        free_only: boolean. if Ture, return events only if they are free of charge
        description: boolean. if True, return events only if they have description
        distance_range: integer. How far in meters does the event happen from the location put in
        display_language: 'en' or 'ja'. choose between english and japanese to show the results
        num_results: integer. how many events you want to retrieve
        sort_by: 'distance', 'closingsoon', or 'mostpopular'


        RETURNS
        --------
        a data frame containing all the information about the events holding
        near the location you input.

        EXAMPLES
        --------

        """
        self.lat = lat
        self.lon = lon

        # set parameters
        params = {'Latitude': lat,
                  'Longitude': lon,
                  'Schedule': current_only,
                  'SearchRange': str(distance_range) + 'm',
                  'Description': "" if description_only == True else "all",
                  'Free': int(free_only),
                  'Language': display_language,
                  'MaxResults': num_results}

        # request get
        r = requests.get('http://www.nyartbeat.com/list/event_searchNear', params=params)

        # check status
        status = r.status_code
        if status >= 100 & status < 200:
            print('informational responses')
        elif status >= 200 & status < 300:
            pass
        elif status >= 300 & status < 400:
            print('redirected')
        elif status >= 400 & status < 500:
            print('client errors')
        elif status >= 500 & status < 600:
            print('sever errors')

        # parse the response
        with open('returned.xml', 'w') as f:
            f.write(r.text)

        tree = ET.parse('returned.xml')
        root = tree.getroot()
        results = []

        for event in root:
            info = {}
            for detail in event:
                if detail.tag == 'Venue':
                    for item in detail:
                        info['Venue_' + item.tag] = item.text
                elif detail.tag in ['Image']:
                    pass
                else:
                    info[detail.tag] = detail.text

            results.append(info)

        self.results = pd.DataFrame(results)

        return self.results

    def view_on_map(self):
        '''

        :return:
        '''

        if self.results is None:
            print('Please use the **get_event_near_me** method first to get events near your location!')
        else:
            import folium
            base_map = folium.Map(
                location=[self.lat, self.lon],
                zoom_start=15,
                tiles='Stamen Terrain',
                width=1024,
                height=600
            )

            for _, row in self.results.iterrows():
                folium.Circle(
                    location=[row['Latitude'], row['Longitude']],
                    radius=20,
                    color='red'
                ).add_to(base_map)

            return base_map
