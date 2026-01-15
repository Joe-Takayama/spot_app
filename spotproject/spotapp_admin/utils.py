import requests

# 住所から緯度・経度を取得する関数
def get_latlng(address):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": address,
        "format": "json"
    }

    res = requests.get(url, params=params).json()

    # データが取れた場合
    if res:
        return float(res[0]['lat']), float(res[0]['lon'])

    # 取れなかった場合
    return None, None
