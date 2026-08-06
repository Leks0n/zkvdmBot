def clean_city_name(city_input: str) -> str:
    clean_name = ' '.join(city_input.split()).capitalize()
    return clean_name