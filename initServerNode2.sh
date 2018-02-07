#!/bin/bash

#initServerNode2.sh
# Justin Dowd, 01/30/2018 jmdowd@g.clemson.edu
# Contains edited code created by Blake Lytle in December 2017

#initServerNode.sh
addr=$(hostname -i)
echo $addr


#python getIP.py

#python sendIP.py

## CHANGE LINE BELOW TO YOUR PHOTOSCAN INSTALLATION PATH ##
cd ~/photoscan/photoscan-pro/

# Start PhotoScan network server
./photoscan.sh --server --control $addr --dispatch $addr

cd ~/photoscan/networkScripts

python getIP.py
python sendIP.py
