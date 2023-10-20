# Copyright © William Adams 2023, licensed under Mozilla Public License Version 2.0

import aiohttp
import json
from dotenv import load_dotenv
import os


load_dotenv()
weather_token = os.getenv('WEATHER_API_KEY')


# gets the coordinates of the location
async def getCoords(city):
    # sends a request to the weather api
    async with aiohttp.request('GET', f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={weather_token}") as response:
        # if the request is successful, it returns the coordinates of the city, otherwise it returns the error code
        if response.status == 200:
            data = await response.json()
            if data == []:
                return False, 400
            else:
                lat = data[0]['lat']
                lon = data[0]['lon']
                city = data[0]['name']
                return True, lat, lon, city
        else:
            return False, response.status

# gets the weather data based on the coordinates
async def getWeather(lat, lon):
    # sends a request to the weather api with the coordinates
    async with aiohttp.request('GET', f"https://api.openweathermap.org/data/2.5/weather?lat={str(lat)}&lon={str(lon)}&units=metric&appid={weather_token}") as response:
        # if the request is successful, it returns the weather data, otherwise it returns the error code
        if response.status == 200:
            data = await response.text()
            general = data['weather'][0]['main']
            temp = data['main']['temp']
            wind = data['wind']['speed']
            icon = data['weather'][0]['icon']
            return True, general, temp, wind, icon
        else:
            return False, response.status