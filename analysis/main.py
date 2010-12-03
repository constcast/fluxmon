#!/usr/bin/env python

import sys, os

import ASNTree

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage: " , sys.argv[0], " <data-dir> <asn-file>"
		sys.exit(-1)

	data_dir = sys.argv[1]
	asn_file = sys.argv[2]
	if not os.path.isdir(data_dir):
		print data_dir, " is not a directory. What are you doing?"
		sys.exit(-1);

	asnTree = ASNTree.ASNTree(asn_file)
