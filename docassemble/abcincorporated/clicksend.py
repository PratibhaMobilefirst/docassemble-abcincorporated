from __future__ import print_function
import time
import base64
import clicksend_client
from clicksend_client.rest import ApiException
from pprint import pprint
from clicksend_client import PostRecipient
from docassemble.base.util import variables_snapshot_connection,get_config, user_info, json, url_of

def clicksend_post_return_adress(user_data):
  #__________code to add new Recipient in clicksend platform___________   
  
  
  # Configure HTTP basic authorization: BasicAuth
  configuration = clicksend_client.Configuration()
  configuration.username = 'willie@lexyalgo.com'
  configuration.password = '150E8868-E005-D4C9-39CB-B7797E269B50'

  # create an instance of the API class
  api_instance = clicksend_client.PostReturnAddressApi(clicksend_client.ApiClient(configuration))
  user_name = user_info().first_name + '' + user_data.get('user.name.middle') + '' + user_info().last_name
  return_address = clicksend_client.Address(address_name=user_name,
                              address_line_1=user_data.get('user.address.address'),
                              address_city=user_data.get('user.address.city'),
                              address_state=user_data.get('user.address.state'),
                              address_postal_code=user_data.get('user.address.zip_code'),
                              address_country="IN")# Address | Address model

  try:
    # Create post return address
    api_response = api_instance.post_return_addresses_post(return_address)
    return eval(api_response)
  except ApiException as e:
    print("Exception when calling PostReturnAddressApi->post_return_addresses_post: %s\n" % e)

def file_url(output_file):

  results=[]
  # Configure HTTP basic authorization: BasicAuth
  configuration = clicksend_client.Configuration()
  configuration.username = 'willie@lexyalgo.com'
  configuration.password = '150E8868-E005-D4C9-39CB-B7797E269B50'

  # Array of PDF file paths
  pdf_file_paths = output_file
    # Add more file paths as needed

  # Create an instance of the API class
  api_instance = clicksend_client.UploadApi(clicksend_client.ApiClient(configuration))
  convert = 'post'  # Specify the conversion type, e.g., 'post'
  for pdf_file_path in pdf_file_paths:
    # Base64 encode the PDF file
    with open(pdf_file_path, "rb") as file:
        base64_data = base64.b64encode(file.read()).decode('utf-8')

    # Create the upload_file dictionary with the content field containing the base64 data
    upload_file = clicksend_client.UploadFile(content=base64_data)

    try:
        # Upload File
        api_response = api_instance.uploads_post(upload_file, convert)
        results.append(eval(api_response))
    except ApiException as e:
        return f"Exception when calling UploadApi->uploads_post for {pdf_file_path}: {e}\n"
  return results

def file_url_single(output_file):

  # Configure HTTP basic authorization: BasicAuth
  configuration = clicksend_client.Configuration()
  configuration.username = 'willie@lexyalgo.com'
  configuration.password = '150E8868-E005-D4C9-39CB-B7797E269B50'

  # Array of PDF file paths
  pdf_file_paths = output_file
    # Add more file paths as needed

  # Create an instance of the API class
  api_instance = clicksend_client.UploadApi(clicksend_client.ApiClient(configuration))
  convert = 'post'  # Specify the conversion type, e.g., 'post'

  with open(pdf_file_paths, "rb") as file:
      base64_data = base64.b64encode(file.read()).decode('utf-8')

    # Create the upload_file dictionary with the content field containing the base64 data
  upload_file = clicksend_client.UploadFile(content=base64_data)

  try:
      # Upload File
      api_response = api_instance.uploads_post(upload_file, convert)
      return eval(api_response)
  except ApiException as e:
      return f"Exception when calling UploadApi->uploads_post for {pdf_file_path}: {e}\n"

def clicksend_send_post_letter(plan_sponsor_name,plan_sponsor_address_line_1,plan_sponsor_address_city,plan_sponsor_address_state,plan_sponsor_postal_code,return_address,url1):
  #     # Create a new configuration object within this function
  configuration = clicksend_client.Configuration()
  configuration.username = 'willie@lexyalgo.com'
  configuration.password = '150E8868-E005-D4C9-39CB-B7797E269B50'

  # Create an instance of the API class
  api_instance = clicksend_client.PostLetterApi(clicksend_client.ApiClient(configuration))

  # Define the common recipient information
  post_recipient = PostRecipient(address_name=plan_sponsor_name,
                              address_line_1=plan_sponsor_address_line_1,
                              address_city=plan_sponsor_address_city,
                              address_state=plan_sponsor_address_state,
                              address_postal_code=plan_sponsor_postal_code,
                              address_country="US",
                              return_address_id=return_address)

  # List of file URLs for PDF files

  post_letter = clicksend_client.PostLetter(
              file_url=url1,
              recipients=[post_recipient]) 
 

  try:
      # Send the post letter
      api_response = api_instance.post_letters_send_post(post_letter)
      print(f"Letter sent for PDF URL: {url1}")
      return eval(api_response)
  except ApiException as e:
       print(f"Exception when calling PostLetterApi->post_letters_send_post for PDF URL: {url1}\n{e}")
     
    
def url_test(demo):
  return url_of(demo)