from os import name
from django.contrib.auth import authenticate
from django.db import reset_queries
import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core.api_exception import ApiException
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions


def get_request(url, **kwargs):
    """
    Utility function to make HTTP GET requests
    """
    print("\nGET from {} with paramaters {}".format(url,kwargs))
    try:
        if 'apikey' in kwargs:
            # ...separate apikey from kwargs to submit separately
            api_key = kwargs.pop('apikey')
            # ...verify we just have the parameters now
            print("Updated parameters: {}".format(kwargs))
            # ...call the get method in request lib
            response = requests.get(url, headers={'Content-type': 'application/json'}, 
                params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            # ...calling the request lib's get method with URL + params and store it
            response = requests.get(url, headers={'Content-type': 'application/json'},
                params=kwargs)
                # params = kwargs? //I mean i guess it's working.
    except:
        # ...if that fails leave a general note.
        print("Network exception occurred")
    # relay status code info to console
    status_code = response.status_code
    print("Response Final URL {}".format(response.url))
    print("Response status {} \n".format(status_code))
    # package and return json data
    json_data = json.loads(response.text)
    return json_data


def post_request(url, json_payload, **kwargs):
    """
    Utility function to make HTTP POST requests
    """
    print("POST to {} with paramaters {} \nIncludes payload: {}".format(url,kwargs, json_payload))
    try:
        # ...calling url with POST method from requests lib with payload
        response = requests.post(url, headers={'Content-type': 'application/json'}, 
            json=json_payload) # don't wanna include params, just the json.
    except:
        print("Network exception occurred.")
    
    # relay status code info to console and caller
    status_code = response.status_code
    print("Response Final URL {}".format(response.url))
    print("Response status {} \n".format(status_code))
    return status_code



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
            # Reincarnate each JSON obj as a CarDealerObj
            dealer_obj = CarDealer(dealer)
            #verify new obj
            #print(dealer_obj.full_name)
            results.append(dealer_obj)
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
    if 'state' in kwargs:
        json_result = get_request(url, state=kwargs['state']) # Auth suddenly needed?
    else:
        print('State (Abbrev.) not supplied in kwargs.')
        results.append('Could not execute request: missing state abbreviation')
    
    # Continue with business
    if 'entries' in json_result:
        dealers = json_result['entries']

        for dealer in dealers:
            # Reincarnate each JSON obj as a CarDealerObj
            dealer_obj = CarDealer(dealer)
            #verify new obj
            print(dealer_obj.full_name)
            results.append(dealer_obj)
    else:
        print('No entries received for State {}'.format(kwargs['state']))
        results = 'Could not retrieve Dealer data.'
    return results


def get_dealer_reviews_from_cf(url, **kwargs):
    """
    This function calls get_request() w/ the specified args (dealerId) then:
        1. Parses the json data returned from the request / "get-dealer-reviews" Cloud function
        2. Puts it into a proxy DealerReviews obj.
        3. Creates and returns a list of those proxies.
    
    For some reason, this requires authentication be sent with the request... but is a public api.
    """
    results =[]

    # Check for "required" kwargs then make request
    if 'dealerId' in kwargs:
        json_result = get_request(url, dealerId=kwargs['dealerId'])
    else:
        print('Dealer ID not supplied in kwargs.')
        results.append("Could not execute request: missing Dealer ID")
    
    # Continue with business
    if 'entries' in json_result:
        reviews = json_result['entries']

        for review in reviews:
            # take each review and pass the dict/JSON obj to the Dealer Review constructor
            review_obj = DealerReview(review)
            # verify new obj - this stuff should be going to the logger...
            #print(review_obj.review)
            # Analyze the review sentiment + set it as the property
            nlu_result = analyze_review_sentiments(review_obj.review)
            sentiment = ""
            if 'sentiment' in nlu_result:
                sentiment = nlu_result['sentiment']['document']['label']
            elif 'error' in nlu_result:
                sentiment = 'unknown'
            review_obj.sentiment = sentiment
            print("Review ID{} sentiment rating: {}".format(review_obj.id, review_obj.sentiment))
            results.append(review_obj)

    else:
        print('No entries received for Dealer Id {}'.format(kwargs['dealerId']))
        results = 'Could not retrieve review data: ' + json['error']
    return results


# #
# Watson NLU Service
# #

"""
#API_KEY = ''
#authenticator = IAMAuthenticator(API_KEY)

NLU_SVC_URL = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/30a70f1b-882f-424a-a8ed-78fa443eb84c'
NLU_SVC = NaturalLanguageUnderstandingV1(
    version='2021-03-25',
    #authenticator=authenticator
)
NLU_SVC.set_service_url(NLU_SVC_URL)
"""

def analyze_review_sentiments(text):
    """
    1. Calls get_request() with specified args to Watson NLU service
    2. Returns the sentiment label
    """
    # params = {}
    NLU_SVC_URL = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/51af308a-51f8-4cfb-9553-727d22394718'

    try: # Calling the analyze method
        """
        nlu_response = NLU_SVC.analyze(
            text=text,
            features=Features(
                sentiment=SentimentOptions(document=True)
            )
        ).get_result()
        """
        nlu_response = get_request(NLU_SVC_URL, text=text)
        #print(json.dumps(response, indent=2))
        return nlu_response
    except ApiException as ex:
        #print("Something broke (;u; ) {}".format(response.get_status_code()))
        error_msg = "Something broke (;u; ) [{}]: {}".format(ex.code, ex.message)
        print(error_msg)
        return {'error': error_msg}

