#!/bin/bash

# initServerNode.sh
# Blake Lytle, Clemson Center for Geospatial Technologies, www.clemsongis.org
# December 2017
# This is an example script to start an Agisoft PhotoScan server node.
# Once initiated, the server node will distribute parallel processing tasks amongst any active processing nodes.
# Use this script as the executable in a PBS job script.

# Print host IP address to command line. ## NOTE THE OUTPUT AND ENTER IN initProcNode.sub AND PhotoScan GUI ##
addr=$(hostname -i)
echo $addr

## CHANGE LINE BELOW TO YOUR PHOTOSCAN INSTALLATION PATH ##
cd ~/photoscan/photoscan-pro/

# Start PhotoScan network server
./photoscan.sh --server --control $addr --dispatch $addr

