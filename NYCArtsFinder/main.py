import pandas as pd
import requests
import xml.etree.ElementTree as ET
from geopy.geocoders import Nominatim
import re


class EventsNearMe:

    # predefine attributes
    def __init__(self):
        self.location = 'New York City'
        self.results = None
        self.lat = 40.7581
        self.lon = -73.9855
        self.use_input = False

    # help method: convert address to geolocation (latitude and longitude)
    # in case users do not have them at their disposal
    def input_address(self, address=''):
        try:
            locator = Nominatim(user_agent="finding_events_in_NYC")
            location = locator.geocode(address)
            check = check_address(location.address)
            if check is None:
                self.lat = location.latitude
                self.lon = location.longitude
                self.use_input = True  # used in major methods for reminder of the default lat&lon
            else:
                return check
        except AttributeError:
            return "Please type in a valid (and New York City's) address, thank you!"

    # the major methods using API to fetch recent and future Art events around the
    # input NYC location
    def get_event_near_me(self,
                          lat=None,
                          lon=None,
                          current_only=False,
                          free_only=False,
                          description_only=False,
                          distance_range=3000,
                          display_language='en',
                          num_results=50,
                          sort_by="distance"):
        """
        This method will return art events in NYC around the location users put in the function.

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

        """

        # check for the validation of the input location
        if (lat is None or lon is None) and self.use_input:
            # if user does not put in lat, lon but used input_address() before
            lat = self.lat
            lon = self.lon
        elif (lat is None or lon is None) and not self.use_input:
            # if user doesn't give lat, lon, and have not use input_address() before,
            # use the default lat and lon, and send a reminder.
            lat = self.lat
            lon = self.lon
            return "*" \
                   "Reminder: You do not input any address or geographic information, " \
                   "this app will use the default midtown NYC location to return results for you." \
                   "*"
        else:
            # check for the scope of user input lat & lon,
            # if no problem, store the user's input lat, lon for further usage.
            locator = Nominatim(user_agent="finding_events_in_NYC")
            location = locator.reverse(str(lat) + ', ' + str(lon))
            check = check_address(location.address)
            if check is None:
                self.lat = lat
                self.lon = lon
                pass
            else:
                return check

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

        if len(results) == 0:
            self.results = None
            return "It seems there's no art event near your location. Maybe try it later or change to another " \
                   "location. Thank you! "
        else:
            self.results = pd.DataFrame(results)
            return self.results

    def view_on_map(self, save=False):
        """
        This method helps visualize the returned events on map.

        PARAMETERS
        --------
        save: boolean. If True, will store the map object to local folder

        RETURNS
        --------
        a map object

        """

        # check if the get_event_near_me() is used or returned more than 0 results.
        if self.results is None:
            return 'Please use the **get_event_near_me** method first to get enough events near your location!'
        else:
            # import necessary package
            import folium

            # build base layer
            map = folium.Map(
                location=[self.lat, self.lon],
                zoom_start=15,
                tiles='Stamen Terrain'
            )

            # add in dots as events
            for i, row in self.results.iterrows():
                folium.Circle(
                    location=[row['Latitude'], row['Longitude']],
                    radius=15,
                    color='red'
                ).add_to(map)

            # see if need to store the object to folder
            if save:
                map.save('./events_near_me_NYC.html')

            return map


# helper function
# check if the address is within NYC
def check_address(address):
    temp = re.findall('new york city|nyc|new york county',
                      address,
                      re.IGNORECASE)
    if len(temp) > 0:
        pass
    else:
        return "Please choose an address within New York City, thank you!"
