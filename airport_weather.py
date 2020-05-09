import requests
import csv
import matplotlib.pyplot as plt
import time

# load api key from a file in the outer folder called weather_key.txt
KEY = "73464ce5711c1df0347ca111265e0401"


class Airport():
    '''
    This serves as a module that allows easy use of my API. The class
     initializes an airport with a specific id and is able to return 
     to the user the cleanly formatted weather conditions of the airport.
    This module also provides the option to display a graph of the last
    24 hours of weather data for the given airport.
    '''
    
    def __init__(self, airport_id):
        self.id = airport_id

        #initialize other parameters and populate if valid airport id
        self.name = None
        self.type = None
        self.country_abrev = None
        self.region = None
        self.city = None
        self.lat = None
        self.lon = None
        with open("./airport-codes.csv", "r") as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                if (row['ident'] == airport_id): #found the airport
                    self.name = row['name']
                    self.type = row['type']
                    self.country_abrev = row['iso_country']
                    self.region = row['iso_region'].split('-')[-1]
                    self.city = row['municipality']
                    self.lat = float(row['coordinates'].split(', ')[0])
                    self.lon = float(row['coordinates'].split(', ')[1])

        if (self.name == None):
            print("WARNING: Unable to identify provided airport: {0}". format(airport_id))

    def get_current_conditions(self, temp_units="C"):
        '''Get the current weather conditions for the airport, return a well formatted dict'''
        
        conditions = {
            "valid": False
        }

        if (self.name == None):
            return conditions

        api_url = "http://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}"
        r = requests.get(api_url.format(self.lat, self.lon, KEY))
        
        if (r.status_code != 200):
            return conditions
        
        conditions["title"] = "{0} in {1}, {2}, {3}".format(self.name, self.city, self.region, self.country_abrev)
        conditions["description"] = r.json()['weather'][0]['description']

        #parse weather values and store with units

        ##### Temperature and Feels Like #####
        if (temp_units == 'C'):
            temp = r.json()['main']['temp'] - 273
            feels_like = r.json()['main']['feels_like'] - 273
            
            conditions["temperature"] = "{:.2f} C".format(temp)
            conditions["feels_like"] = "{:.2f} C".format(feels_like)
        elif(temp_units == 'F'):
            temp = ((r.json()['main']['temp'] - 273) * (9.0/5.0)) + 32
            feels_like = ((r.json()['main']['feels_like'] - 273) * (9.0/5.0)) + 32
            
            conditions["temperature"] = "{:.2f} F".format(temp)
            conditions["feels_like"] = "{:.2f} F".format(feels_like)
        elif (temp_units == 'K'): 
            temp = r.json()['main']['temp']
            feels_like = r.json()['main']['feels_like']

            conditions["temperature"] = "{0} K".format(temp)
            conditions["feels_like"] = "{0} K".format(feels_like)
        else: #just use Celsius if no valid units provided
            temp = r.json()['main']['temp'] - 273
            feels_like = r.json()['main']['feels_like'] - 273
            
            conditions["temperature"] = "{:.2f} C".format(temp)
            conditions["feels_like"] = "{:.2f} C".format(feels_like)

        ##### Pressure and Humidity #####
        conditions['pressure'] = "{0} hPa".format(r.json()['main']['pressure'])
        conditions['humidity'] = "{0}%".format(r.json()['main']['humidity'])
        
        ##### Wind Speed #####
        try:
            wind_speed = "{0} m/s".format(r.json()['wind']['speed'])
        except:
            wind_speed = "unavailable"
        
        try:
            wind_direction = "{0} degrees".format(r.json()['wind']['deg'])
        except:
            wind_direction = "unavailable"

        conditions['wind'] = {
            "speed": wind_speed,
            "direction": wind_direction
        }
        
        conditions['valid'] = True

        return conditions

    def print_current_conditions(self, temp_units="C"):
        '''Retrieves current weather conditions and prints them nicely'''
        c = self.get_current_conditions(temp_units=temp_units)

        disp = "{0} (Current Weather Conditions)\n".format(c["title"])
        disp += "\t{0}\n".format(c["description"].capitalize())
        disp += "\tCurrent Temperature: {0}\n".format(c["temperature"])
        disp += "\tFeels Like: {0}\n".format(c["feels_like"])
        disp += "\tHumidity: {0}\n".format(c["humidity"])
        disp += "\tPressure: {0}\n".format(c["pressure"])
        disp += "\tWind:\n"
        disp += "\t\tSpeed: {0}\n".format(c["wind"]["speed"])
        disp += "\t\tDirection: {0}\n\n".format(c["wind"]["direction"])

        print(disp)

    def get_forecast(self, period=24, temp_units="C"):
        '''
        Display a graph of the hourly temperature in the time period (in 3 hour increments) provided. The
        default period is the past 24 hours from the present.
        '''
        
        api_url = "https://api.openweathermap.org/data/2.5/forecast?lat={0}&lon={1}&appid={2}"

        r = requests.get(api_url.format(self.lat, self.lon, KEY))
        
        if (r.status_code != 200):
            print("Invalid airport")
            return 
        
        if (period > 40):
            period = 40
        elif (period < 0):
            period = 2

        now = int(time.time())
        timestamps = [] #time from now in hours
        temperatures = []
        pressures = []
        humidities = []
        for i in range(period): #get all of the forecast data for provided period
            timestamps.append(int((r.json()['list'][i]['dt']-now)/(60*60)))
            if (temp_units == "C"):
                temperatures.append(r.json()['list'][i]['main']['temp']-273)
            elif(temp_units == "F"):
                temperatures.append(((r.json()['list'][i]['main']['temp']-273) * (9.0/5.0)) + 32)
            elif(temp_units == "K"):
                temperatures.append(r.json()['list'][i]['main']['temp'])
            else: #use celsius
                temperatures.append(r.json()['list'][i]['main']['temp']-273)
            pressures.append(r.json()['list'][i]['main']['pressure'])
            humidities.append(r.json()['list'][i]['main']['humidity'])

        total_hours = period * 3

        ### Ask user if they want to see each of the forecast graphs ###
        print("{0} in {1}, {2}, {3}".format(self.name, self.city, self.region, self.country_abrev))
        user_r = input("\tShow temperature forecast for {0} (y or n)? ".format(self.name))
        if (user_r == 'y'):
            plt.title("{0} Temperature Forecast: Next {1} hours".format(self.name, total_hours))
            plt.xlabel("Hours from now")
            plt.ylabel("Temperature forecast ({0})".format(temp_units))
            plt.plot(timestamps,temperatures)
            plt.show()

        user_r = input("\tShow pressures forecast for {0} (y or n)? ".format(self.name))
        if (user_r == 'y'):
            plt.title("{0} Pressure Forecast: Next {1} hours".format(self.name, total_hours))
            plt.xlabel("Hours from now")
            plt.ylabel("Pressure forecast (hPa)")
            plt.plot(timestamps,pressures)
            plt.show()

        user_r = input("\tShow humidity forecast for {0} (y or n)? ".format(self.name))
        if (user_r == 'y'):
            plt.title("{0} Humidity Forecast: Next {1} hours".format(self.name, total_hours))
            plt.xlabel("Hours from now")
            plt.ylabel("Humidity forecast (%)")
            plt.plot(timestamps,humidities)
            plt.show()
        print()

        return

if __name__ == "__main__":
    #examples

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