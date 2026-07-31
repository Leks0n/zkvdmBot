from services.utils import clean_city_name

favourites_db = {}

def add_city(user_id: int, city: str) -> bool:
    if user_id not in favourites_db:
        favourites_db[user_id] = []

    clean_city = clean_city_name(city)

    if clean_city not in favourites_db[user_id]:
        favourites_db[user_id].append(clean_city)
        return True
    return False

def remove_city(user_id: int, city: str) -> list:
    clean_city = clean_city_name(city)

    if user_id in favourites_db and clean_city in favourites_db[user_id]:
        favourites_db[user_id].remove(clean_city)
        return True
    return False

def get_user_city(user_id) -> list:
    return favourites_db.get(user_id, [])