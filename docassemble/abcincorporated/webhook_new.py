import requests
import sys
import time
import datetime
import pytz
import stripe
from docassemble.base.util import log
from urllib.parse import urlparse, parse_qs
from docassemble.base.util import variables_snapshot_connection,get_config, user_info, json
import psycopg2

stripe.api_key = get_config('stripe secret key')

def retrieve_product_price():
    product = stripe.Price.retrieve("price_1MW2ZeBOgpkiH8jqbVSi8t9W")
    return product.unit_amount / 100 

def addUrl(url, mainid):
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    cur.execute("UPDATE interview SET url_with_args = %s WHERE id = %s AND user_id = %s", (url, mainid, user_info().id))
    log('url_args', url_args)
    conn.commit()
    cur.close()
    return ''

def printUrl(initialUrl, interview_id, url_args):
    currUrl = 'http://doc.lexyalgo.com/interview?i=' + initialUrl + '&id=' + str(interview_id)
    if 'session' in url_args:
        del url_args['session']
    for key in url_args:
        currUrl += '&' + key +'='+ url_args[key]
    return currUrl
    
def yml_variables(interview_id, initialUrl, args):
    try:
        current_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " America/New_York"
        parsed_url = printUrl(initialUrl, interview_id, args)
        addUrl(parsed_url, interview_id)
        
        click_id = ''
        if 'gclid' in args:
            click_id = args['gclid']
        elif 'gbraid' in args:
            click_id = args['gbraid']
        elif 'wbraid' in args:
            click_id = args['wbraid']
        elif 'msclkid' in args:
            click_id = args['msclkid']
        elif args:
            click_id = next(iter(args.values()))
        
        if click_id:
            params = {
                'Conversion Name': "QDROgenerated",
                'Conversion Time': current_time,
                'Conversion Value': retrieve_product_price(),
                'Conversion Currency': 'USD',
            }
            
            if 'gclid' in args:
                params['Google Click ID'] = click_id
                response = requests.get('https://script.google.com/macros/s/AKfycbz4YKL3XeNCuQswv80VCuM-kLR-VDJuKP5Pj2psYBy97x09QG2pSG_SLA9Zmig-lcrH/exec?gid=0', params=params)
            elif 'gbraid' in args:
                params['Google Click ID'] = click_id
                response = requests.get('https://script.google.com/macros/s/AKfycbz4YKL3XeNCuQswv80VCuM-kLR-VDJuKP5Pj2psYBy97x09QG2pSG_SLA9Zmig-lcrH/exec?gid=0', params=params)
            elif 'wbraid' in args:
                params['Google Click ID'] = click_id
                response = requests.get('https://script.google.com/macros/s/AKfycbz4YKL3XeNCuQswv80VCuM-kLR-VDJuKP5Pj2psYBy97x09QG2pSG_SLA9Zmig-lcrH/exec?gid=0', params=params)
            elif 'msclkid' in args:
                params['Microsoft Click ID'] = click_id
                response = requests.get('https://script.google.com/macros/s/AKfycbzSkMLhY4XxoWlLGBa2cFiJFAsihpuQy5jzqaGq5wnwwLeZUIwG7Xi3hXvuky2y_uvuqg/exec?gid=0', params=params)
            else:
                params['Others Click ID'] = click_id
                response = requests.get('https://script.google.com/macros/s/AKfycby63B0W7W4MtlJqxia3HHctt4uDgdsgAaA4tGpbQVBqmFXCubOUAF1h9fOPyoefT77rSw/exec?gid=0', params=params)
            
            log("Response", response)
            if response.status_code != 200:
                sys.exit(response.text)
            else:
                return ''
        
    except Exception as e:
        log(str(e))
        return ''
