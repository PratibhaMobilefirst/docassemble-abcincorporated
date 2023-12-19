import requests
import sys
import datetime
import stripe
from docassemble.base.util import log, get_config
from urllib.parse import parse_qs

stripe.api_key = get_config('stripe secret key')

def retrieve_product_price():
    product = stripe.Price.retrieve("price_1MW2ZeBOgpkiH8jqbVSi8t9W")
    return product.unit_amount / 100

def check_cookie_value(cookie_value):
    if cookie_value is None:
        return ''
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " America/New_York"
    split_cookie = cookie_value.split('=')
    
    if len(split_cookie) == 2:
        key, value = split_cookie[0], split_cookie[1]
        if key == 'gclid' or key == 'wbraid' or key == 'gbraid':
            params = {
                'Google Click ID': value,
                'Conversion Name': "QDROgenerated",
                'Conversion Time': current_time,
                'Conversion Value': retrieve_product_price(),
                'Conversion Currency': 'USD',
            }
            response = requests.get('https://script.google.com/macros/s/AKfycbz4YKL3XeNCuQswv80VCuM-kLR-VDJuKP5Pj2psYBy97x09QG2pSG_SLA9Zmig-lcrH/exec?gid=0', params=params)
            if response.status_code != 200:
                sys.exit(response.text)
                

        elif key == 'msclkid':
            params = {
                'Microsoft Click ID': value,
                'Conversion Name': "QDROgenerated",
                'Conversion Time': current_time,
                'Adjustment Value': retrieve_product_price(),
                'Adjustment Currency': 'USD',
                'Adjustment Type': '',
                'Adjustment Time': current_time,
            }
            response = requests.get('https://script.google.com/macros/s/AKfycbzSkMLhY4XxoWlLGBa2cFiJFAsihpuQy5jzqaGq5wnwwLeZUIwG7Xi3hXvuky2y_uvuqg/exec?gid=0', params=params)
            if response.status_code != 200:
                sys.exit(response.text)

        elif key:  # For other keys
            params = {
                'Others Click ID': value,
                'Conversion Name': "QDROgenerated",
                'Conversion Time': current_time,
                'Adjustment Value': retrieve_product_price(),
                'Adjustment Currency': 'USD',
                'Adjustment Type': '',
                'Adjustment Time': current_time,
            }
            response = requests.get('https://script.google.com/macros/s/AKfycby63B0W7W4MtlJqxia3HHctt4uDgdsgAaA4tGpbQVBqmFXCubOUAF1h9fOPyoefT77rSw/exec?gid=0', params=params)
            if response.status_code != 200:
                sys.exit(response.text)
    else:
        return ''
