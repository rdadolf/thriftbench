#!/bin/bash
./server.py 38003 &
./server.py 38004 &
./server.py 38005 &
./server.py 38006 &
./server.py 38007 &
sleep 1
./client.py localhost:38003 localhost:38004 localhost:38005 localhost:38006 localhost:38007
kill %1
kill %2
kill %3
kill %4
kill %5
