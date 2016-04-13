#!/usr/bin/perl
#
# Dummy program to show perl plugin
#
# Strict and warnings are recommended.
use strict;
use warnings;

print ":speak:This is a dummy plugin in perl.\n";
print "Counting down...";

for(my $i=3; $i >= 0; $i--){
  sleep(1);
  print ":speak:$i\n";
}