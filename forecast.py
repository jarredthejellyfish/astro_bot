import pyowm, requests
from geopy.geocoders import Nominatim
import certifi, ssl, geopy.geocoders

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

#OpenWeatherMaps API key
owm = pyowm.OWM('79f7a1995bb5c8006f7f6ce7c542ce51')

#Get basic 3h data from Open Weather Maps
def basic_forecast_unform(usr_city):
    #Current forecast.
    loc = owm.weather_at_place(usr_city)
    weather = loc.get_weather()
    #Temperature 
    temperature = weather.get_temperature('celsius')['temp']
    #Humidity
    humidity = weather.get_humidity()
    #Wind Speed
    wind_speed = weather.get_wind()

    #Forecast over the next 3h.
    three_hour_forecast = owm.three_hours_forecast(usr_city)
    #Is it gonna rain?
    rain = three_hour_forecast.will_have_rain()
    #Are clouds gonna roll in?
    clouds = three_hour_forecast.will_have_clouds()

    #Return all collected values.
    return rain, clouds, temperature, humidity, wind_speed

#Gnerate simple forecast fro satellite.py images.
def basic_forecast(usr_city):
    #Get unformatted forecast from Open Weather Maps
    unf_forecasting = basic_forecast_unform(usr_city)
    #Conditionals to determine what message to send.
    if unf_forecasting[0] == True:
        return "Damn, it looks like there is gonna be some rain. I wouldn't recommend bringing out your telescope tonight."
    elif unf_forecasting[1] == True:
        return "Oh no, it looks like there are gonna be some clouds!"
    elif unf_forecasting[3] > 50:
        return "Careful, there are going to be no clouds or rain, but the humidity is going to be a little high."
    else:
        return "All clear! Looks like you'll be having some fun :)."

#Get coordinates from city input
def generate_coords(usr_city):
    #Log into nominatim (location database)
    geolocator = Nominatim(user_agent='domesticmexican')
    #Initialize location object with user input city as parameter
    location = geolocator.geocode(usr_city)
    #Get coordinates
    city_lat = round(location.latitude, 2)
    city_lon = round(location.longitude, 2)
    return city_lat, city_lon

def generate_link(usr_city):
    #Get lat and lon from Nominatim
    coords = generate_coords(usr_city)
    #Generate link with formatted coordinates for clearoutside.
    link = 'https://clearoutside.com/forecast_image_large/{}/{}/forecast.png'.format(coords[0], coords[1])
    return link