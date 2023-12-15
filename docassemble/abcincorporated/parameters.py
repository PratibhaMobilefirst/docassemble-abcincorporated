from flask import request

__all__ = ['get_cookies']

def get_cookies():
  cookie_name = 'lexyalgoadsid'
  cookie_value = request.cookies.get(cookie_name, None)
  #return dict(request.cookies)
  return cookie_value