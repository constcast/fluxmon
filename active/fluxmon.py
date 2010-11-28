#!/usr/bin/env python

import os, sys

import config

if __name__ == "__main__":
	print "Starting up fluxmon ..."
	if (os.path.isdir(config.storage_dir)) == True:
		print "Found Dir"
	else:
		print "Directory ", config.storage_dir, " does not exist! Tyring to create the directory ..."
		try: 
			os.mkdir(config.storage_dir) 
		except OSError as e:
			print "Cannot create directory \"", config.storage_dir, "\": ", e.args;
			sys.exit(-1);
