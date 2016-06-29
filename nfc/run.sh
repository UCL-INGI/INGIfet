#!/bin/bash

echo $$ > /tmp/nfc_tunnel.pid
exec python2 nfc_tunnel.py 2>&1 | tee NFC.log
