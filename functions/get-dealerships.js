/**
  *
  * Takes the returned docs and reformats it w/ the info we need.
  * the map() array func will return a list after iterating over every obj
  * all the docs are also stored in an array in an entry called "row"
  * 
  * ...why we aren't including the full/short name of dealerships? i'm not sure.
  */
 function main(params) {
	return { 
	    entries: params.rows.map( (row) => { return { //yet another obj
	        id: row.doc.id,
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
