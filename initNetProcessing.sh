#!/bin/bash

# initNetProcessing.sh
# Justin Dowd, Clemson Center for Geospatial Technologies, www.clemsongis.org
# March 2018 
# Email: jmdowd@g.clemson.edu
# This script will submit all the necessary jobs in order to set up a PhotoScan parallel processing network, submit data for processing, and process
# the submitted data 

chmod u=rwx ~/arguments.txt
cwd=$(pwd)

#Gets the 5th line of arguments.txt
photoscanVar=`sed -n '5 p' ~/arguments.txt`
#Gets the 6th line of arguments.txt
dir=`sed -n '6 p' ~/arguments.txt`

#Submit a job that will start a PhotoScan server node using the script written in initServerNode2.sh
#Walltime is 72 hours, meaning the server node will remain active for up to 72 hours  or until the user kills it
qsub ./initServerNode.sh -l walltime=72:00:00
#Sleep allows time for initServerNode2.sh to write the IP Address to a file and allow the server to start running prior to moving on
sleep 30s

#Submit a job that currently creates 8 parallel PhotoScan processing nodes 
qsub procNodeArray.sub
#Sleep Allows the array of processing nodes to be created and connect to the server node
sleep 20s

#Prints the IP Address of the server node to the console, so the user can use it to view the progress of processing through the Network Monitor GUI
cat $dir/address.txt
sleep 10s

#Each job sumbits a script with a matching task name to conduct the various tasks in proper order (E.g. submitMatchPhotos.sh runs the Python Script MatchPhotos.py)
qsub submitMatchPhotos.sh
qsub submitAlignCameras.sh
qsub submitBuildDepthMaps.sh
qsub submitBuildDenseCloud.sh

