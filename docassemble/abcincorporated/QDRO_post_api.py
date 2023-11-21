from docassemble.base.util import *
import requests


def submit_form_to_api(input_fields):
    # API endpoint
    api_url = "https://api.lawmatics.com/v1/forms/967aca55-a304-44e4-9ee3-27f68ed771d5/submit"

    # Input fields

    # Send a POST request with input fields
    response = requests.post(api_url, json=input_fields)

    # Check the response status
    if response.status_code == 200:
        return 'success!!'
    else:
        return input_fields,response.status_code

