#!/usr/bin/env bash

# This is a plugin for controlling a roku device from alan.


# List ip addresses on local network
IP_LIST=$(arp -a | tail -r | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
# tail -r only works on bsd. replace with tac for gnu
if [[ -z $IP_LIST ]]; then
IP_LIST=$(arp -a | tac | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
fi
echo ":speak:Finding and connecting to your Roku."
# Walk IP addresses and check port 8060
for IP in $IP_LIST; do
  echo $IP
  # Check if the port is open to identify roku.
  STATUS=$(nc -v -z $IP 8060 &> /dev/null && echo "Online" || echo "Offline")
  if [ "$STATUS" == "Online" ]; then
        ROKU_IP=$IP
        break
  fi
done
# Check if ROKU_IP has been found.
if [[ $ROKU_IP ]] ; then
  echo "The roku ip is " $ROKU_IP
  echo ":speak: Successfully connected to your Roku"
  echo ":listen:"
  read CONTROLLER
  while [[ $CONTROLLER && "$CONTROLLER" != "exit" ]]
  do
    # Fixed an issue where multiple params were passed. Take last param only
    CONTROLLER=$(echo $CONTROLLER | awk {'print $NF'})
    curl -d "" -s $ROKU_IP:8060/keypress/$CONTROLLER
    echo $CONTROLLER
    read CONTROLLER
  done
  echo $CONTROLLER
else
  echo ":speak:Could not connect to your Roku."
fi