from geopy.geocoders import Nominatim

import requests

def find_location_coordinates(address, featuretype=None):
    nomination = Nominatim(user_agent="http://127.0.0.1:8000/")
    localization = nomination.geocode(address, exactly_one=False, extratags=True, featuretype=featuretype)

    if localization is None:
        return None
    
    localization = localization[0]

    return {"latitude": localization.latitude,
            "longitude": localization.longitude,
            "address": localization.address}

def different_days_in_db(db, days):
    if db.start_date == days.cleaned_data["start_date"] and db.end_date == days.cleaned_data["end_date"]:
        return False
    
    return True

def get_cleared_url(url):
    if "vm.tiktok.com" in url:
        response = requests.get(url)
        if response.status_code == 200:
            url = response.url

    parts = url.split("?")[0]
    return parts