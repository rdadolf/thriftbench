#!/bin/sh

PROT_TYPE="binary"
cd py
python server.py $PROT_TYPE &
PID=$!
python client.py $PROT_TYPE
kill $PID
