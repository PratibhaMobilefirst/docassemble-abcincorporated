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


stripe.api_key = get_config('stripe tsecret key')
# Get the current date and time

# Convert the current time to the Eastern Standard Time (EST) timezone
#est_timezone = pytz.timezone('US/Eastern')
#converted_time = current_time.astimezone(est_timezone)
# Format the converted time as a string with timezone
#conversion_time = converted_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')


def retrieve_product_price():
    product = stripe.Price.retrieve("price_1MW2ZeBOgpkiH8jqbVSi8t9W")
    return product.unit_amount / 100 

def addUrl(url, mainid):
  conn = variables_snapshot_connection()
  cur = conn.cursor()
  cur.execute("UPDATE interview SET url_with_args = %s WHERE id = %s AND user_id = %s", (url, mainid, user_info().id))
  conn.commit()
  cur.close()
  return ''

def printUrl(initialUrl,interview_id,url_args):
    currUrl = 'http://doc.lexyalgo.com/interview?i=' + initialUrl + '&id=' + str(interview_id)
    if 'session' in url_args:
      del url_args['session']
    for key in url_args:
      currUrl += '&' + key +'='+ url_args[key]
    #parsed_url = urlparse(interview_url() )
    return currUrl
    
def yml_veriables(interview_id,initialUrl,args):
  
  current_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " America/New_York"
  
  parsed_url = printUrl(initialUrl,interview_id,args)
  
  addUrl(parsed_url,interview_id)
  
  if 'id' in args:
    del args['id']
  
  if 'gclid' in args or 'gbraid' in args or 'wbraid' in args:
    if 'gclid' in args:
      result = args['gclid']
    elif 'gbraid' in args:
      result = args['gbraid']
    else:
      result = args['wbraid']
    params = {
      'Google Click ID': result,
      'Conversion Name': "QDROgenerated",
      'Conversion Time': current_time,
      'Conversion Value': retrieve_product_price(),
      'Conversion Currency': 'USD',
      }
    response = requests.get('https://script.google.com/macros/s/AKfycbz4YKL3XeNCuQswv80VCuM-kLR-VDJuKP5Pj2psYBy97x09QG2pSG_SLA9Zmig-lcrH/exec?gid=0',params=params,)
    log("Response",response)
    if response.status_code != 200:
      sys.exit(response.text)
      info = response.json()
    else:
      return ''

  elif 'msclkid' in args:						
    params = {
      'Microsoft Click ID': args['msclkid'],
      'Conversion Name': "QDROgenerated",
      'Conversion Time': current_time,
      'Adjustment Value': retrieve_product_price(),
      'Adjustment Currency': 'USD',
      'Adjustment Type': '',
      'Adjustment Time': current_time,
      }
    response = requests.get('https://script.google.com/macros/s/AKfycbzSkMLhY4XxoWlLGBa2cFiJFAsihpuQy5jzqaGq5wnwwLeZUIwG7Xi3hXvuky2y_uvuqg/exec?gid=0',params=params,)
    if response.status_code != 200:
      sys.exit(response.text)
      info = response.json()
    else:
      return '' 
    
  elif args:
    params = {
      'Others Click ID': next(iter(args.values())),
      'Conversion Name': "QDROgenerated",
      'Conversion Time': current_time,
      'Adjustment Value': retrieve_product_price(),
      'Adjustment Currency': 'USD',
      'Adjustment Type': '',
      'Adjustment Time': current_time,
      }
    response = requests.get('https://script.google.com/macros/s/AKfycby63B0W7W4MtlJqxia3HHctt4uDgdsgAaA4tGpbQVBqmFXCubOUAF1h9fOPyoefT77rSw/exec?gid=0',params=params,)
    if response.status_code != 200:
      sys.exit(response.text)
      info = response.json()
    else:
      return ''
  else:
      return ''