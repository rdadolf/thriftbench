#!/bin/sh

NUM_CLIENTS=1000
NUM_REQUESTS=30000

cd py
python server.py &
PID=$!
disown %1
sleep 0.05

REQUESTS=`expr $NUM_REQUESTS / $NUM_CLIENTS`
for i in `seq 1 $NUM_CLIENTS`
do
    python client.py $REQUESTS &
done

wait
kill $PID
