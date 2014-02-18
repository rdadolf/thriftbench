#!/bin/sh

PROT_TYPE="binary"
cd cpp
./server $PROT_TYPE &
PID=$!
time ./client $PROT_TYPE
kill $PID
