#!/bin/sh

if [ $# -ne 1 ]
then
  echo "Usage: `basename $0` <output_file>"
  exit -1;
fi

output_file=$1;

curl http://mirror1.malwaredomains.com/files/domains.txt | sed '/^\#/d' | awk '{print $1}' > $output_file
