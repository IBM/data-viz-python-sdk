#!/bin/bash

# START THE STATIC SERVER
cd /opt/web/
serve -s build &

while :
do
	sleep 100
done




