# EC500 Homework 2: Weather API study

## Assignment
* Let’s study the Weather.gov [API](https://www.weather.gov/documentation/services-web-api)
* Let’s study OpenWeatherMAP [API](https://openweathermap.org/api)
* For all USA Airports, Develop an API and module where we can get current conditions for the airport asked by the API and we can get current weather graphs (for example, the temperature for the last 24 hours) for specific period.  It does not have to be graphs but the data needed.
Github location of HW:  https://classroom.github.com/a/93ZDS2Ht, which is empty
* I am expecting to use CB and CI in the exercise
* I am also expecting you to developing examples using your API

## My API Documentation
I have created a class called Airport that takes a valid airport ID input. Valid airport IDs are listed in the spreadsheet provided in the assignment corresponding with airports around the world. I provide some example codes below to make it easier to test.

### Airport Class ###

#### Constructor
Initializes the class with the airport ID and other parameters describing the airport that are present in airport-codes.csv. This includes the airport name, type, country abbreviation, region, city, latitude, and longitude. These are useful fields I use in other portions of the class. If the airport ID provided is invalid (not present in airport-codes.csv), then all of the aforementioned parameters are initialized to None.

#### Get Current Conditions
This function gets the current weather conditions for the airport using the Open Weather Map API and formats them nicely in a dictionary format. The api request url used has the following format:
http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API Key}"

This function has one optional keyword argument:
* `temp_units`: The desired units of the temperature data. Options are `'C'`, `'F'`, and `'K'`. Defaults to Celsius (C).

This is useful for printing these statistics nicely or using my API for other purposes without having to worry about accessing the api url properly. See usage instructions for how this can be used.

#### Print Current Conditions
Displays the current weather conditions of the airport in standard output. This allows for easy display of current results for the provided airport ID. This function has one optional keyword argument:
* `temp_units`: The desired units of the temperature data. Options are `'C'`, `'F'`, and `'K'`. Defaults to Celsius (C).

#### Get Forecast
This function uses the Open Weather Map API to get the forecast for the period defined in the arguments of the function. The format of the API request used is:
https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={API Key}"
There are multiple optional keyword arguments:
* `period`: The number of 3-hour increments from now to fetch data for.
* `temp_units`: The desired units of the temperature data. Options are `'C'`, `'F'`, and `'K'`. Defaults to Celsius (C).
* `temp`: A boolean indicating whether or not to display the graph of temperature data.
* `hum`: A boolean indicating whether or not to display the graph of humidity data.
* `pres`: A boolean indicating whether or not to display the graph of pressure data.


## Usage instructions
In order to use this API, find the airport for which you would like to know about the weather in airport-codes.csv. Locate the "ident" field for the airport and copy it. To use the package, clone the repository. To import the API:
```python
from airport_weather import Airport
```
The following shows examples of how to use the API for Heathrow, Boston, and Atlanta airports:
```python
# Heathrow
heathrow = "EGLL"
heathrow_airport = Airport(heathrow)
heathrow_airport.get_forecast()
heathrow_airport.print_current_conditions()

# Boston Logan
logan = "KBOS"
logan_airport = Airport(logan)
logan_airport.get_forecast()
logan_airport.print_current_conditions()

# Atlanta 
atlanta = "KATL"
atlanta_airport = Airport(atlanta)
atlanta_airport.get_forecast()
atlanta_airport.print_current_conditions()
```

The following example for Heathrow shows how to toggle keyword arguments:
```python
# Heathrow
heathrow = "EGLL"
heathrow_airport = Airport(heathrow)
heathrow_airport.get_forecast(period=10, temp_units='K', pres=False, hum=False)
heathrow_airport.print_current_conditions(temp_units='F')
```