#!/bin/bash

while true; do
    python2 nfc_tunnel.py 2>&1 | tee NFC.log
done
