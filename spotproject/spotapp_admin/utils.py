import requests

def get_latlng(address):
    if not address:
        return None, None

    address = address.strip()

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1,
        "countrycodes": "jp",
        "accept-language": "ja",
        "addressdetails": 1
    }
    headers = {
        "User-Agent": "spotapp/1.0 (admin@example.com)"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)

        print("request url:", response.url)

        if response.status_code != 200:
            print("status error:", response.status_code)
            return None, None

        data = response.json()
        print("response data:", data)

        if not data:
            return None, None

        return float(data[0]["lat"]), float(data[0]["lon"])

    except Exception as e:
        print("error:", e)
        return None, None
