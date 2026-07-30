import aiohttp 

from services.weather_codes import get_weather_description, get_uv_description

async def get_weather_by_city(city: str) -> dict | None:
    geo_url = f'https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=ru'

    async with aiohttp.ClientSession() as session:
        async with session.get(geo_url) as response:
            geo_data = await response.json()

            if "results" not in geo_data:
                return None

            result = geo_data['results'][0]
            lat = result['latitude']
            lon = result['longitude']
            resolved_city_name = result['name']

        weather_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=uv_index_max&timezone=auto'

        async with session.get(weather_url) as weather_response:
            weather_data = await weather_response.json()

            current = weather_data['current_weather']
            weather_code = weather_data['current_weather']['weathercode']
            uv_index = weather_data['daily']['uv_index_max'][0]

            weather_desc = get_weather_description(weather_code)
            uv_desc = get_uv_description(uv_index)

            return {
                'city': resolved_city_name,
                'temperature': current['temperature'],
                'windspeed': current['windspeed'],
                'description': weather_desc,
                'uv_description': uv_desc
            }