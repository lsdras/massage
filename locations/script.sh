#!/bin/bash

dirname=$(date '+%Y_%m_%d')
declare -i lastpage=89

# read dirname
if [ ! -d "$dirname" ]
then
	mkdir ./$dirname
fi


for i in $(seq 1 $lastpage)
do
	curl http://www.anmawon.com/FindShop/List?Page=$i -o ./$dirname/$i.txt
done
