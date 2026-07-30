import asyncio
from services.weather_api import get_weather_by_city

async def main():
    city = input('Введите название города')

    print(f'Ищем погоду для {city}')

    result = await get_weather_by_city(city)

    if result:
        print('Успешно!')
        print(f'Город: {result['city']}')
        print(f'Погода: {result['description']}')
        print(f'Температура: {result['temperature']}')
        print(f'Ветер: {result['windspeed']}')
    else:
        print('Город не найден. Попробуйте написать на английском')

if __name__ == '__main__':
    asyncio.run(main())