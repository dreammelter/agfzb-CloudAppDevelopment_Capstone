#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys

def main(dict):
    # check for data? or will Django handle that?
    
    # strip the review from the dictionary
    # could stick this in a check but may not be necessary...
    #   if 'review' in dict.keys():
    review = {}
    for key, value in dict['review'].items():
        review[key] = value
    
    # return dictionary/JSON obj to store in db
    return { 
        "doc":
            {
                "id": review['id'],
                "name": review['name'],
                "dealership": review['dealership'],
                "review": review['review'],
                "purchase": review['purchase'],
                "another": review['another'],
                "purchase_date": review['purchase_date'],
                "car_make": review['car_make'],
                "car_model": review['car_model'],
                "car_year": review['car_year']
            }
    }
