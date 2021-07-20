/**
  *
  * Takes the returned docs and reformats it w/ the info we need.
  * the map() array func will return a list after iterating over every doc obj
  * skipping on the short name.
  * 
  */
 function main(params) {
	//handle params from exec-query-find function
	if (params.docs) {
	    //grab the info right from the docs entry
	    return {
	        entries: params.docs.map( (doc) => { return { //a new obj
	            id: doc.id,
	            full_name: doc.full_name,
	            city: doc.city,
	            state: doc.state,
	            st: doc.st,
	            address: doc.address,
	            zip: doc.zip,
	            lat: doc.lat,
	            long: doc.long
	        }})
	    };
	} else {
	    //handle params from list-documents function, which stuffs the docs in an entry called "rows"
	    return {
    	    entries: params.rows.map( (row) => { return { //yet another obj
    	        id: row.doc.id,
    	        full_name: row.doc.full_name,
    	        city: row.doc.city,
    	        state: row.doc.state,
    	        st: row.doc.st,
    	        address: row.doc.address,
    	        zip: row.doc.zip,
    	        lat: row.doc.lat,
    	        long: row.doc.long
    	    }})
	    };
	}
}
