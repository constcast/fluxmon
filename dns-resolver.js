var dns    = require('dns');
var fs     = require('fs');
var config = require('./config.js');

function add_new_domain(domain) {
	// TODO: check if we already know the domain and have it in our active lookup list
	// this is important!!


	// immediate dns lookup
	lookup_domain(domain)	
}

function lookup_domain(domain) {
	dns.resolve4(domain, function (err, addresses, ttl) {
		// TODO: better error handling!
		if (err) {
			console.log('Error locking up domain: ' + JSON.stringify(err));
			// try again in an hour!
			setTimeout(lookup_domain, 3600 * 1000, domain);
			return;
		}
		dns_resolver_finished(domain, addresses, ttl);
	});
}

function dns_resolver_finished(domain, addresses, ttl) {

	var timestamp = new Date();

	console.log("Got resolution for " + domain + ". Rescheduling query in " + ttl + " seconds");

	fs.open(config.data_dir + '/' + domain, "a+", 0666, function (err, fd) {
		if (err) throw err;
		//console.log("Opened file: " + JSON.stringify(stat));
		addresses.forEach(function (a) {
			var line = domain + " " + ttl + " " + a + " " + timestamp.getTime() + "\n";
			fs.write(fd, line, null, encoding='utf8', function (err, written) {
				if (err) throw err;
			});
		});
	});
	
	setTimeout(lookup_domain, ttl * 1000, domain);
};


exports.new_domain = add_new_domain;
