#!/bin/bash
./server.py 38003 &
./server.py 38004 &
./server.py 38005 &
sleep 10
kill %1
kill %2
kill %3
