#!/bin/bash

# START THE nodemon SERVER
cd /opt/web/
nodemon server.js &

# START THE FLASK ENDPOINT
cd /opt/
python3 api.py &

sleep 10
wget http://0.0.0.0:8080/test

while :
do
	sleep 100
done




