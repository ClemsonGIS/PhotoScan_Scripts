#!/bin/bash


# initServerNode.sh
# Justin Dowd, Clemson Center for Geospatial Technologies, www.clemsongis.org
# March 2018
# This scipt starts a PhotoScan network server and writes its IP address 
# to address.txt to be used by other scripts
# Contains previous code created by Blake Lytle in December 2017

addr=$(hostname -i)
## Get path to script directory from arguments.txt and write IP address to address.txt ##
dir=`sed -n '6 p' ~/arguments.txt`
echo $addr > $dir/address.txt
chmod u=rwx $dir/address.txt

## Get path to PhotoScan installation directory and change to it ##
pDir=`sed -n '5 p' ~/arguments.txt`
cd $pDir

# Start PhotoScan network server
./photoscan.sh --server --control $addr --dispatch $addr
