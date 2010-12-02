var dns    = require('dns');
var fs     = require('fs');
var config = require('./config.js');

var observed_domains = new Array();

function add_new_domain(domain) {
	// TODO: check if we already know the domain and have it in our active lookup list
	// this is important!!
	
	var proceed = true;
	observed_domains.forEach(function (d) {
		if (domain == d) {
			console.log('No need to add domain ' + domain + ' to list, already known');
			proceed = false;
		}
	});
	if (!proceed) {
		return;
	}

	observed_domains.push(domain);
	// immediate dns lookup
	lookup_domain(domain)	
}

function lookup_domain(domain) {
	dns.resolve(domain, rrtype='NS', function (err, addresses) {
		if (err) {
			console.log('Error looking up nameserver for "' + domain + '": ' + JSON.stringify(err));
			// TODO: or should we scheulde the new lookup??
			//setTimeout(lookup_domain, 3600 * 1000, domain);
			return;
		}
		dns_resolver_finished('NS', domain, addresses, 0);
	});

	dns.resolve(domain, rrtype='A', function (err, addresses, ttl) {
		// TODO: better error handling!
		if (err) {
			console.log('Error locking up "' + domain + '": ' + JSON.stringify(err));
			if (ttl == 0) {
				ttl = 3600 * 1000;
			}
			setTimeout(lookup_domain, ttl, domain);
			return;
		}
		console.log("Got TTL: " + ttl);
		dns_resolver_finished('A', domain, addresses, ttl);
		if (ttl == 0) {
			ttl = 1
		}
		
		//console
		setTimeout(lookup_domain, ttl * 1000, domain);
	});
}

function dns_resolver_finished(type, domain, addresses, ttl) {
	var timestamp = new Date();

	console.log("Got " + type + " resolution for " + domain + ". Rescheduling query in " + ttl + " seconds");

	fs.open(config.data_dir + '/' + domain, "a+", 0666, function (err, fd) {
		if (err) throw err;
		//console.log("Opened file: " + JSON.stringify(stat));
		addresses.forEach(function (a) {
			var line = type + " " + domain + " " + ttl + " " + a + " " + timestamp.getTime() + "\n";
			fs.write(fd, line, null, encoding='utf8', function (err, written) {
				if (err) throw err;
			});
		});
	});
	
};


exports.new_domain = add_new_domain;
