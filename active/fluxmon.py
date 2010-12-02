#!/usr/bin/env python

import os, sys

import config, domain_agent

if __name__ == "__main__":
	print "Starting up fluxmon ..."
	domain_db = config.storage_dir + "/" + config.domain_db;
	if (os.path.isdir(config.storage_dir)) == True:
		print "Found data storage directory \"" + config.storage_dir + "\"...";
	else:
		print "Directory ", config.storage_dir, " does not exist! Tyring to create the directory ..."
		try: 
			os.mkdir(config.storage_dir) 
		except OSError as e:
			print "Cannot create directory \"", config.storage_dir, "\": ", e.args;
			sys.exit(-1);

	agent = domain_agent.DomainAgent(domain_db, config.new_domain_file)
	print "\n\n"
	print "****************************************************\n"
	print "*     Startup completed. We are ready to go.       *\n"
	print "*        Starting fluxmon event loop ...           *\n"
	print "****************************************************\n"
	print "\n\n"
	agent.run()
