#!/bin/bash

qsub ./initServerNode2.sh

sleep 10s

qsub procNodeArray.sub

#qsub ./runScript.sh
