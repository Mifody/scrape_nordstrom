#!/bin/bash

DAY=`date +%Y_%m_%d`
mkdir -p out
mkdir -p log
rm -f out/nordstrom_${DAY}.jsonlines
scrapy crawl nordstrom -o out/nordstrom_${DAY}.jsonlines --logfile log/nordstrom_${DAY}.log.txt
