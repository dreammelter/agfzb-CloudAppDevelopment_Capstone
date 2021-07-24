/**
  * Just return a query obj in the format exec-query-find should be able to use...
  * Uses MN or Dealership 13 since they only have one doc.
  * This only passes data to a Cloudant action so it can be repurposed however.
  * 
  */
 function main(params) {
	if (params.state) {
	    //create query for dealers by state
	    return {
	        query: {
	            "selector": {
	                "st": params.state
	            },
	            "fields": [
	                "id", "full_name", "city",
	                "address", "st", "zip",
	                "lat", "long", "short_name"
	                ]
	        },
	        "use_index": "dealersByState"
	    };
	} else if (params.dealerId) {
	    //create query for review by dealership
	    return {
	        query: {
	            "selector": {
	                "dealership": parseInt(params.dealerId) //is auto-converted to string when passed back
	            },
	            "fields": [
	                "id", "name", "review",
	                "dealership", "purchase", "purchase_date",
	                "car_make", "car_model", "car_year"
	                ]
	        },
	        "use_index": "reviewByDealership"
	    };
	} else {
	    //just return the docs
	    return {
	        params: {
	            include_docs: true
	        }
	    };
	}
}
