#!/usr/bin/env bash

DIR=/home/pi/bitcoin/calc/

function main(){
		python ${DIR}calc.py $1 --loop 900
}

DELAY=120

while true
do
	main $1
	msg="Waiting $DELAY s before restarting worker $0"
	echo $msg
	sleep $DELAY
done
