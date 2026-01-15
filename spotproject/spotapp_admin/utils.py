import requests

# 住所から緯度・経度を取得する関数
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

        res = requests.get(url, params=params, headers=headers, timeout=5).json()

        if res.status_code != 200:
            print('Nominatim status error:', res.status_code)
            return None, None
        
        if not res.text:
            print('Nominatim empty response')
            return None, None
        
        data = res.json()
    
    except Exception as e:
        print('get_latlng error:', e)
        return None, None
    
    if data:
        return float(data[0]['lat']), float(data[0]['lon'])
    
    return None, None