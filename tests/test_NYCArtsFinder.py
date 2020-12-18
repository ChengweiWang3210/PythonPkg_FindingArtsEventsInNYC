from ..NYCArtsFinder.__init__ import __version__
from ..NYCArtsFinder.main import EventsNearMe
import folium

# check for the package version
def test_version():
    assert __version__ == '0.3.0'

# check for the situation when user type in address outside of NYC
def test_notNYC_address():
    notNYC_address = "Texas"
    expected = "Please choose an address within New York City, thank you!"
    actual = EventsNearMe().input_address(notNYC_address)
    assert actual == expected

# check for the situation when user used an invalid address
def test_invalid_address():
    invalid_address = 'xixixihahaha'
    expected = "Please type in a valid (and New York City's) address, thank you!"
    actual = EventsNearMe().input_address(invalid_address)
    assert actual == expected

# check for the situation when there are zero results returned by the API
def test_zero_return():
    possible_zero_loc = {'lat': 40.8737750042313,
                         'lon': -73.9169572637484}
    expected = "It seems there's no art event near your location. Maybe try it later or change to another " \
               "location. Thank you! "
    actual = EventsNearMe().get_event_near_me(**possible_zero_loc)
    assert actual == expected

# check for the situation when user used view_on_map before getting any dataset
def test_view_without_fetch():
    expected = False
    actual = isinstance(EventsNearMe().view_on_map(), folium.folium.Map)
    assert actual == expected
