import aiohttp
import logging

from config import OWM_API_KEY
from services.weather_codes import get_weather_description, get_uv_description

logger = logging.getLogger(__name__)

async def get_weather_by_city(city: str) -> dict | None:

    geo_url = f'https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={OWM_API_KEY}'

    async with aiohttp.ClientSession() as session:
        async with session.get(geo_url) as response:
            if response.status != 200:
                logger.error(f'Ошибка геокодинга. Статус: {response.status}')
                return None

            geo_data = await response.json()

            if not geo_data:
                return None

            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']
            resolved_city_name = geo_data[0]['name']

        weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OWM_API_KEY}&units=metric&lang=ru'

        async with session.get(weather_url) as weather_response:

            if weather_response.status != 200:
                logger.error(f'Ошибка при получении погоды:{weather_response.status}')
                return None

            weather_data = await weather_response.json()

            temperature = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']

            weather_code = weather_data['weather'][0]['id']

            windspeed = weather_data['wind']['speed']

            weather_desc = get_weather_description(weather_code)

            return {
                'city': resolved_city_name,
                'temperature': temperature,
                'feels_like': feels_like,
                'windspeed': windspeed,
                'description': weather_desc,
            }