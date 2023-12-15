import ast
import clicksend_client
from clicksend_client.rest import ApiException

def delete_return_addresses():
    # Configure HTTP basic authorization: BasicAuth
    configuration = clicksend_client.Configuration()
    configuration.username = 'willie@lexyalgo.com'
    configuration.password = '150E8868-E005-D4C9-39CB-B7797E269B50'

    # Create an instance of the API class
    api_instance = clicksend_client.PostReturnAddressApi(clicksend_client.ApiClient(configuration))

    try:
        # Initialize variables for pagination
        total_return_address_ids = 0
        address_id_count = {}

        # Starting page number
        page_number = 1

        while True:
            # Get list of post return addresses for the current page
            api_response = api_instance.post_return_addresses_get(page=page_number)

            # Convert string response to a Python dictionary
            response_dict = ast.literal_eval(api_response)

            # Access the 'data' element containing return address details
            return_addresses = response_dict.get('data', {}).get('data', [])

            if not return_addresses:
                # No more addresses, break the loop
                break

            # Increment total count
            total_return_address_ids += len(return_addresses)

            # Count occurrences of each return_address_id
            for address in return_addresses:
                return_address_id = address.get('return_address_id')
                if return_address_id in address_id_count:
                    address_id_count[return_address_id] += 1
                else:
                    address_id_count[return_address_id] = 1

            #print(f"Total Return Address IDs: {total_return_address_ids}")

            # Move to the next page
            page_number += 1

            # Check if total_return_address_ids is 80
            if total_return_address_ids > 69:
                excess_count = total_return_address_ids - 69
                print(f"Deleting the first {excess_count} Return Address IDs:")
              
                count = 0
                for address_id, _ in address_id_count.items():
                    print(f"Deleting Return Address ID: {address_id}")
                    
                    # Delete the return address by ID
                    api_response = api_instance.post_return_addresses_by_return_address_id_delete(address_id)
                    print(api_response)
                    
                    count += 1
                    if count >= excess_count:
                        break

                # Break out of the loop since we've reached 64 addresses
                break
        return total_return_address_ids
        # Print count for each return_address_id after deletion
        #print("Return Address ID Counts after Deletion:")
        #for address_id, count in address_id_count.items():
            #print(f"Return Address ID: {address_id}, Count: {count}")

    except ApiException as e:
        print("Exception when calling PostReturnAddressApi->post_return_addresses_get: %s\n" % e)



