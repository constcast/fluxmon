var sys = require('sys');
var path = require('path');
var fs = require('fs');

var config = require('./config.js');
var dns_resolver = require('./dns-resolver.js');


// ###################################### functions

function check_for_new_input() {
	path.exists(config.domain_input_file, function (exists) {
		if (exists) {
			console.log(" ... found new domain input file!");
			var buff = fs.readFileSync(config.domain_input_file).toString();
			buff.split('\n').forEach(function(line) {
				if (line != '') {
					dns_resolver.new_domain(line);
				}
			});


			fs.unlink(config.domain_input_file);
		}
	});
}

// ##################################  main is starting here #################

console.log("FluxMon is starting up ...");

// check if the data_directory exists
path.exists(config.data_dir, function(exists) {
	if (!exists) {
		fs.mkdir(config.data_dir, 0700, function(err) {
			if (err) {
				throw err;
			}
		});
	}
});


// read old from last runs from  data from directory
fs.readdir(config.data_dir, function(err, files) {
	if (err) throw err;
	files.forEach(function(f) {
		dns_resolver.new_domain(f);
	});
});

// periodically check for new domain input list
setInterval(check_for_new_input, 1000);
