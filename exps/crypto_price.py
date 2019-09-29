import requests
import json

def get_price(coin):
    r = requests.get('https://api.coinranking.com/v1/public/coins?symbols='+coin)
    if r.status_code ==200:
        data = json.loads(r.text)
        return  data['data']['coins'][0]['price']
    else:
        return False

