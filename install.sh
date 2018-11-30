#!/bin/sh

mkdir -p /opt/netscanner
cp -r netscanner.py /opt/netscanner
cp netscanner /usr/bin
chmod +x /usr/bin/netscanner