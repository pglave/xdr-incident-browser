import json
import requests
from datetime import datetime, date, timedelta

# XDR Region
REGION = 'EU'

# Domain names for API endpoints
XDR_API_DOMAIN = f'visibility.{REGION}.amp.cisco.com'
CONURE_API_DOMAIN = f'conure.{REGION}.security.cisco.com'

def format_iso_date_to_readable(iso_date_string):
    """
    Formats an ISO 8601 date string (e.g., "2025-07-22T18:03:41.000Z")
    into a "YYYY-MM-DD HH:MM:SS" format.

    Args:
        iso_date_string (str): The input date string in ISO 8601 format.

    Returns:
        str: The formatted date string, or the input string if parsing fails.
    """
    # Define the input format for strptime
    # %Y: Year (e.g., 2025)
    # %m: Month (e.g., 07)
    # %d: Day (e.g., 22)
    # T: Literal 'T'
    # %H: Hour (24-hour clock, e.g., 18)
    # %M: Minute (e.g., 03)
    # %S: Second (e.g., 41)
    # .%f: Microseconds (e.g., .000)
    # Z: Literal 'Z' (indicating UTC)
    input_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    # Define the desired output format for strftime
    output_format = "%Y-%m-%d %H:%M:%S"

    try:
        # 1. Parse the input string into a datetime object
        dt_object = datetime.strptime(iso_date_string, input_format)

        # 2. Format the datetime object into the desired output string
        formatted_date = dt_object.strftime(output_format)
        return formatted_date
    except ValueError as e:
        return iso_date_string

def get_iso_date_n_days_ago(n_days):
    """
    Calculates a date N days earlier than today and returns it in ISO 8601 format (YYYY-MM-DD).

    Args:
        n_days (int): The number of days to go back from today.

    Returns:
        str: The date string in 'YYYY-MM-DD' format.
    """
    today = date.today()
    past_date = today - timedelta(days=n_days)
    return past_date.isoformat()


def authenticate(client_id, client_password):

    url = f'https://{XDR_API_DOMAIN}/iroh/oauth2/token'
    headers = {
            'Content-Type':'application/x-www-form-urlencoded',
            'Accept':'application/json'
    }
    payload = {
                'grant_type':'client_credentials'
    }


    auth_data = {
        'status_code' : 0,
        'access_token' : '',
        'scope' : '',
        'expires_in' : ''
    }

    response = requests.post(url, headers=headers, auth=(client_id, client_password), data=payload)
    #print(response.text)

    auth_data['status_code'] = response.status_code

    if response.status_code == 200:
        # convert the response to a dict object
        response_json = json.loads(response.text)

        # get the access token
        auth_data['access_token'] = response_json['access_token']

        # get the scope of the token
        auth_data['scope'] = response_json['scope']

        # get the duration that the token is valid
        auth_data['expires_in'] = response_json['expires_in']
    
    return auth_data
    

def load_incidents(token, limit, days_ago):

    url = f'https://{CONURE_API_DOMAIN}/v2/incident/search'
    bearer_token = 'Bearer ' + token
    headers = {
                'Authorization': bearer_token,
                'Content-Type':'application/json',
                'Accept':'application/json'
    }
    params = {
                'limit': limit
    }
    params['from'] = get_iso_date_n_days_ago(days_ago)

    return_data = {
        'status_code' : 0,
        'incident_data' : []
    }

    response = requests.get(url, headers=headers, params=params)

    return_data['status_code'] = response.status_code

    if response.status_code == 200:
        # convert the response to a dict object
        response_json = json.loads(response.text)

        for incident in response_json:
            # Save incident data into an array.
            item = {}
            item['title'] = incident['title']
            item['created'] = format_iso_date_to_readable(incident['created'])
            item['id'] = incident['id']
            return_data['incident_data'].append(item)
        
        #print(return_data['incident_data'])
    
    return return_data

def load_incident_details(token, inc_id):

    url = f'https://{CONURE_API_DOMAIN}/v2/incident/{inc_id}'
    bearer_token = 'Bearer ' + token
    headers = {
                'Authorization': bearer_token,
                'Content-Type':'application/json',
                'Accept':'application/json'
    }
    params = {
    }
    return_data = {
        'status_code' : 0,
        'incident_details' : {}
    }

    response = requests.get(url, headers=headers, params=params)

    return_data['status_code'] = response.status_code

    if response.status_code == 200:
        # convert the response to a dict object
        response_json = json.loads(response.text)
        return_data['incident_details'] = response_json
        #print(return_data['incident_details'])
    
    return return_data



