#!/bin/bash
#initProcNode2.sh
# Justin Dowd, 01/30/2017 jmdowd@g.clemson.edu
# Contains edited code from initProcNode.sh created by
# Blake Lytle in December 2017


addr=$(python returnIP.py)

## ENTER YOUR PHOTOSCAN INSTALLATION DIRECTORY ##
psPath=~/photoscan/photoscan-pro/

## ENTER THE ABSOLUTE PATH TO YOUR ACTIVE PHOTOSCAN PROJECT ##
# projPath= /scratch2/


# Start PhotoScan processing node. GPU's are enabled, output to screen is disabled, and absolute paths are used.
cd $psPath
./photoscan.sh --node --dispatch $addr --gpu_mask 1 --absolute_paths 1 --root /scratch2 -platform offscreen
