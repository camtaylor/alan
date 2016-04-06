#!/usr/bin/env bash
echo ":speak:What is the ticker?"
echo ":listen:"
read ticker
PRICE=$(curl -s "http://download.finance.yahoo.com/d/quotes.csv?s=$ticker&f=l1")
ALAN=":speak:$ticker is trading at $ "
OUTPUT=$ALAN$PRICE
echo $OUTPUT