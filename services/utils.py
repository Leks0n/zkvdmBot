def clean_city_name(city_input: any) -> str:
    if isinstance(city_input, list):
        city_input = city_input[0] if city_input else ''
    clean_name = str(city_input).strip()
    clean_name = clean_name.strip("[]'\"")

    return clean_name