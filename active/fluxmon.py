#!/usr/bin/env python

import os, sys

import config, domain_agent

def pull_domains_from_db(db):
	pass

if __name__ == "__main__":
	print "Starting up fluxmon ..."
	if (os.path.isdir(config.storage_dir)) == True:
		print "Found data storage directory \"" + config.storage_dir + "\"...";
		domain_db = config.storage_dir + "/" + config.domain_db;
		if (os.path.isfile(domain_db)):
			print "Found existing domain database. Reading domains ....";
			initial_domain_list = pull_domains_from_db(domain_db);
			
	else:
		print "Directory ", config.storage_dir, " does not exist! Tyring to create the directory ..."
		try: 
			os.mkdir(config.storage_dir) 
		except OSError as e:
			print "Cannot create directory \"", config.storage_dir, "\": ", e.args;
			sys.exit(-1);

	agent = domain_agent.DomainAgent(initial_domain_list, config.new_domain_list)
	agent.run()
