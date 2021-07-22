import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs) # these are all the URL params to associate w/ call
    print("GET from {} ".format(url))
    try:
        # ...calling the request lib's get method with URL + params and store it
        response = requests.get(url, headers={'Content-type': 'application/json'},
            params=kwargs)
            # are we gonna need the auth info? we should, right?
    except:
        # ...if that fails leave a general note.
        print("Network exception occurred")
    # relay status code info to console
    status_code = response.status_code
    print("Response status {}".format(status_code))
    # package and return json data
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    """
    This function:
        1. Parses the json data returned from the request / "get-all-dealers" Cloud function
        2. Puts it into a proxy CarDealers obj.
        3. Creates and returns a list of those proxies.
    
    At this moment it takes kwargs (state filter), but doesn't do anything with it.
    """
    results = [] # we're gonna stuff each obj into a list
    json_result = get_request(url)
    if json_result:
        # Get the row list from the obj and save it as our dealers
        # dealers = json_result['rows']
        dealers = json_result['entries'] # this is a list of dicts

        #test_access = dealers[0]['address']
        #print(test_access) # success

        for dealer in dealers:
            i = 0
            for key in dealer: #Get KeyError without this...
                while i < 1: # prevent it from actually doing this for every key
                    # reincarnate it as a CarDealer obj
                    dealer_obj = CarDealer(address=dealer['address'], city=dealer["city"], full_name=dealer["full_name"],
                        db_id=dealer["id"], lat=dealer["lat"], long=dealer["long"], short_name=dealer["short_name"],
                        st=dealer["st"], db_zip=dealer["zip"])
                    results.append(dealer_obj)
                    i += 1 # i++ is not a thing in Python lol...

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



