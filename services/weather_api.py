import aiohttp 

from services.weather_codes import get_weather_description

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

        weather_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true'

        async with session.get(weather_url) as weather_response:
            weather_data = await weather_response.json()

            current = weather_data['current_weather']
            weather_code = weather_data['current_weather']['weathercode']

            weather_desc = get_weather_description(weather_code)

            return {
                'city': resolved_city_name,
                'temperature': current['temperature'],
                'windspeed': current['windspeed'],
                'description': weather_desc
            }