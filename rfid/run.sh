#!/bin/bash

cd ~/rfid/
while true; do
    python2 rfid_tunnel.py >> RFID.log 2>&1
done
