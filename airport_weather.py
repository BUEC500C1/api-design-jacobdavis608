import requests
import csv



# load api key from a file in the outer folder called weather_key.txt
key = ""
try:
    with open("../openweather_key.txt", "r") as fp:
        key = fp.read().split('\n')[0]
except: #if fails to read file, set key to None
    key = None


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
        if (self.name == None):
            return {}

        api_url = "http://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}"
        r = requests.get(api_url.format(self.lat, self.lon, key))
        
        if (r.status_code != 200):
            return {}

        conditions = {}
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
        print(conditions)

        return conditions

    def print_current_conditions(self, temp_units="C"):
        '''Retrieves current weather conditions and prints them nicely'''
        c = self.get_current_conditions(temp_units=temp_units)

        disp = "{0}\n".format(c["title"])
        disp += "\t{0}\n".format(c["description"].capitalize())
        disp += "\tCurrent Temperature: {0}\n".format(c["temperature"])
        disp += "\tFeels Like: {0}\n".format(c["feels_like"])
        disp += "\tHumidity: {0}\n".format(c["humidity"])
        disp += "\tPressure: {0}\n".format(c["pressure"])
        disp += "\tWind:\n"
        disp += "\t\tSpeed: {0}\n".format(c["wind"]["speed"])
        disp += "\t\tDirection: {0}\n\n".format(c["wind"]["direction"])

        print(disp)

if __name__ == "__main__":
    #examples

    # Heathrow
    #heathrow = "EGLL"
    #heathrow_airport = Airport(heathrow)
    #heathrow_airport.get_current_conditions()

    #print()
    # Boston Logan
    #logan = "KBOS"
    #logan_airport = Airport(logan)
    #conditions = logan_airport.print_current_conditions()

    #print()
    # Atlanta 
    #atlanta = "KATL"
    #atlanta_airport = Airport(atlanta)
    #atlanta_airport.print_current_conditions()

    # Random 
    random = "something"
    airport = Airport(random)
    print(airport.get_current_conditions())

# Figure out way to get last 24 hours of this data

# create a function that will graph it if user wants