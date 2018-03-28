#!/bin/bash
#PBS -N procNodeArray
#PBS -l select=1:ncpus=16:ngpus=2:mem=120gb,walltime=72:00:00
#PBS -j oe
#PBS -J 1-3

## procNodeArray.sub
## Blake Lytle, Clemson Center for Geospatial Technologies, www.clemsongis.org
## December 2017
## Edits made by Justin Dowd, March 2018
## This is an example job array script which will start 8 GPU nodes as PhotoScan processing nodes.
## The hardware requirements above are very effective for large processing jobs (100's+ photos).
## Refer to the Palmetto documentation for details on selecting hardware (www.palmetto.clemson.edu)


## CHANGE TO YOUR DIRECTORY CONTAINING initProcNode.sh ##
networkPath=`sed -n '6 p' ~/arguments.txt`

# Initialize as a PhotoScan processing node.
cd $networkPath
./initProcNode.sh
