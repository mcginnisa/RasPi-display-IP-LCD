#!/bin/bash
cat temp.txt >> tcpdumplog.txt
rm temp.txt
touch temp.txt
tcpdump 'icmp[icmptype] = icmp-echo' -n -c 1 -i $1 >> temp.txt &
TASK_PID1=$!
sleep 1
ping -I $1 -c 1 -W 2 8.8.8.8 &
TASK_PID2=$!
sleep 1
kill $TASK_PID1
kill $TASK_PID2
