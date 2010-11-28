#!/usr/bin/env python

import config

if __name__ == "__main__":
	print "Starting up fluxmon ..."
	if (os.path.isdir(config.storage_dir)) == True:
		print "Found Dir"
	else:
		print "Directory " . config.storage_dir . " does not exist!"
