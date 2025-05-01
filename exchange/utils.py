import requests
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def get_dollar_price_from_nobitex():
    cached = r.get('usd_to_irr')
    if cached:
        return float(cached)
    try:
        url = 'https://api.nobitex.ir/market/stats'
        payload = {'srcCurrency': 'usdt', 'dstCurrency': 'rls'}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        rate = float(data['stats']['usdt-rls']['latest'])
        r.setex('usd_to_irr', 3600, rate)
        print("Fetched rate from API:", rate)
        return rate
    except Exception as e:
        print("❌ Error fetching dollar price:", e)
        return None
