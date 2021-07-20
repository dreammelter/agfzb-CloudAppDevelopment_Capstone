/**
  * Just return a query obj in the format exec-query-find should be able to use...
  * Uses MN since it only has one doc.
  */
 function main(params) {
	if (params.state) {
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
	} else {
	    //just return the docs
	    return {
	        params: {
	            include_docs: true
	        }
	    };
	}
}
