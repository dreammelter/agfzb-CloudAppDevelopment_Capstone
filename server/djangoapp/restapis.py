from os import name
from django.contrib.auth import authenticate
import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


def get_request(url, **kwargs):
    """
    Utility function to make HTTP GET requests
    Currently doesn't need/use authenticate kwarg in get method... auth=HTTPBasicAuth('apikey',api_key)
    """
    print(kwargs) # these are all the URL params to associate w/ call
    print("GET from {} ".format(url))
    try:
        # ...calling the request lib's get method with URL + params and store it
        response = requests.get(url, headers={'Content-type': 'application/json'},
            params=kwargs)
            # params = kwargs?
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


# Not 100% sure if I'll repurpose this to include ability to filter by state
# Or if I'll create a separate function for it...
# separate sounds better for testing / compartmentalizing.
def get_dealers_from_cf(url):
    """
    This function calls get_request() w/ the specified args then:
        1. Parses the json data returned from the request / "get-all-dealers" Cloud function
        2. Puts it into a proxy CarDealers obj.
        3. Creates and returns a list of those proxies.
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
    else:
        results = 'Could not pull dealers from database: ' + json_result['error']

    return results


def get_dealer_by_state_from_cf(url, **kwargs):
    """
    This function calls get_request() w/ the specified args (state) then:
        1. Parses the json data returned from the request / "get-state-dealers" Cloud function
        2. Puts it into a proxy CarDealer obj
        3. Creates and returns a list of those proxies.
    """
    results = []
    # CHeck for "required" kwargs then make request
    if kwargs['state']:
        json_result = get_request(url, state=kwargs['state']) # Auth suddenly needed?
    else:
        print('State (Abbrev.) not supplied in kwargs.')
        results.append('Could not execute request: missing state abbreviation')
    
    # Continue with business
    if json_result['entries']:
        dealers = json_result['entries']
        
        for dealer in dealers:
            i = 0
            for key in dealer: # Still get KeyError without this.
                while i < 1:
                    #reincarnate as DealerReview obj
                    dealer_obj = CarDealer(address=dealer['address'], city=dealer["city"], full_name=dealer["full_name"],
                        db_id=dealer["id"], lat=dealer["lat"], long=dealer["long"], short_name=dealer["short_name"],
                        st=dealer["st"], db_zip=dealer["zip"])
                    results.append(dealer_obj)
                    i += 1
    else:
        print('No entries received for State {}'.format(kwargs['state']))
        results = 'Could not retrieve Dealer data.'
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    """
    This function calls get_request() w/ the specified args (dealerId) then:
        1. Parses the json data returned from the request / "get-dealer-reviews" Cloud function
        2. Puts it into a proxy DealerReviews obj.
        3. Creates and returns a list of those proxies.
    
    For some reason, this requires authentication be sent with the request... but is a public api.
    """
    results =[]
    API_KEY = ""

    # Check for "required" kwargs then make request
    if kwargs['dealerId']:
        json_result = get_request(url, dealerId=kwargs['dealerId'], auth=HTTPBasicAuth('apikey', API_KEY))
    else:
        print('Dealer ID not supplied in kwargs.')
        results.append("Could not execute request: missing Dealer ID")
    
    # Continue with business
    if json_result['error']:
        print('Error returned')
        results = json_result['error']
    elif json_result['entries']:
        reviews = json_result['entries']
        
        # test access
        test_access = reviews[0]['review']
        print(test_access)

        for review in reviews:
            i = 0
            for key in review: # Still get KeyError without...
                #reincarnate as DealerReview obj
                while i < 1:
                    review_obj = DealerReview(dealership=review['dealership'], name=review['name'], 
                        purchase=review['purchase'], review=review['review'], purchase_date=review['purchase_date'],
                        car_make=review['car_make'], car_model=review['car_model'], car_year=review['car_year'],
                        sentiment=review['sentiment'], r_id=review['id'])
                    results.append(review_obj)
                    i += 1
    else:
        print('No entries received for Dealer Id {}'.format(kwargs['dealerId']))
        results = 'Could not retrieve review data.'
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



