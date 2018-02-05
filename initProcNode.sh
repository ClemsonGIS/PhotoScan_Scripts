#!/bin/bash
# initProcNode.sh
# Blake Lytle, Clemson Center for Geospatial Technologies, www.clemsongis.org
# December 2017
# This script will initiate an Agisoft PhotoScan processing node to run parallelized tasks.
# Make sure the PhotoScan server node is already running before attempting to run this script.

## ENTER IP ADDRESS OF SERVER NODE ##
addr=10.125.3.15

## ENTER YOUR PHOTOSCAN INSTALLATION DIRECTORY ##
psPath=/home/balytle/photoscan/photoscan-pro/

## ENTER THE ABSOLUTE PATH TO YOUR ACTIVE PHOTOSCAN PROJECT ##
# projPath= /scratch2/


# Start PhotoScan processing node. GPU's are enabled, output to screen is disabled, and absolute paths are used.
cd $psPath
./photoscan.sh --node --dispatch $addr --gpu_mask 1 --absolute_paths 1 --root /scratch2 -platform offscreen
