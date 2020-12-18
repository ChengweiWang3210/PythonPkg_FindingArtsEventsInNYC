# NYCArtsFinder -- Finding Art Events in New York City!

Hi, welcome to my package helping you finding Art Events near you within New York City. This is a package meant to help you effortlessly finding out useful information about art exhibitions near you, and it is built on the [ArtBeat API: New York](http://www.nyartbeat.com/resources/doc/api#event_searchNear_params).

### 1. Installation & Import

Here's the example showing how to install it:

```shell
pip install -i https://test.pypi.org/simple/ NYCArtsFinder
```

After the installation, please import the package before use it on your Python IDE. After that, build the finder. 

``` python
import nycartsfinder.main as main
finder = main.EventsNearMe()
```

### 2. Find Events Near You

To use this project, please have at least your NYC address at your disposal. The example will be "Harlem, NYC" (Please remember to add NYC at the end of the string to avoid ambiguity and stop the functions from working.) 

##### 2.1 Using Address Directly

Since the main method of this function calls for latitude and longitude, so if you are using address (string type), please call the ```input_address()``` first to convert your strings to geographic information. 

```python
finder.input_address('Harlem, NYC')
finder.get_event_near_me()
```

##### 2.2 Using Latitude and Longitude

Or if you have the latitude and longitude of your address directly, please feel free to use them directly on the ```get_event_near_me()``` method, like this: 

```python
finder.get_event_near_me(lat=40.816, lon=-73.947)
```

The method print out the result in pandas dataframe type for you, and are also stored in the class attribute ```results```, if you want to further manipulate it, call: 

```python
event_df = finder.results
```

### 3 View the Events On the Map

If the texts and tables are too much for you, maps are always here to help. **After you call the ```get_event_near_me()``` and get a valid data frame**, call:

```python
finder.view_on_map(save=False)
```

This will print the map for you. If you want to view the map in html, set the argument ```save=True``` so the map will be store to your current directory. 

### 4 Contact Author

Please feel free to try out my package and if you have further questions, doubts, or any ideas, please do not hesitate to contact me via email: chengwei.wendy.wang@gmail.com. Thank you for your use, Enjoy!

