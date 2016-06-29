#!/bin/bash

echo $$ > /tmp/nfc_tunnel.pid
exec python2 nfc_tunnel.py >> NFC.log 2>&1
