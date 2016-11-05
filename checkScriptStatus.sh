#!bin/bash

#check if script is already running
if pidof python3 ./PlexToVera.py > /dev/null
then
	echo "Script is already running..."
else
	echo "Script is NOT running, starting script..."
	cd /opt/PlexToVera
	python3 ./PlexToVera.py
fi