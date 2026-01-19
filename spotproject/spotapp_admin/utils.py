import requests

def get_latlng(address):
    if not address:
        return None, None

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json"
    }
    headers = {
        "User-Agent": "spotapp/1.0 (admin@example.com)"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)

        if response.status_code != 200:
            return None, None

        data = response.json()
        if not data:
            return None, None

    except Exception:
        return None, None

    return float(data[0]["lat"]), float(data[0]["lon"])
