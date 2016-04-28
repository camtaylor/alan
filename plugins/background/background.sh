#!/usr/bin/env bash


# This plugin demonstrates how to run in the background using the :release: command

echo ":speak:Starting the background task"
echo ":release:"

sleep 10
echo ":notify:Here is a notification"
sleep 3
# The following sentence will not be processed by alan because :speak: will not work in released plugin.
echo ":speak:Print statement from background process"
echo ":notify:This is the second notification"
sleep 60
echo ":notify: This is the third notification"
