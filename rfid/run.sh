#!/bin/bash

cd ~/nfc/
while true; do
    python2 nfc_tunnel.py >> NFC.log 2>&1
done
