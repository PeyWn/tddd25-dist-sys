#!/usr/bin/env bash

# ------------------------------------------------------------------------------
# Distributed Systems (TDDD25)
# ------------------------------------------------------------------------------
# Author: Sergiu Rafiliu (sergiu.rafiliu@liu.se)
# Modified: 24 January 2013
#
# Copyright 2012 Linkoping University
# ------------------------------------------------------------------------------

# Assignment 1

# Script for testing the client-server database system.
# This script creates one server and a number of clients that connect to it.
# The number of clients is given as an argument to the script, the default is 3.

no_clients=${1:-3}
term='xterm'
wrap='../modules/Common/wrap.sh'
server='./server.py'
client='client.py -i '

# Run the server.
$term -T 'Server' -e $server &

sleep 1

# Get the server address.
addr=$(sed -e 's/\n//' srv_address.tmp)
rm srv_address.tmp

# Run clients.
for ((i=1; i <= $no_clients ; i++)) ; do
    $term -T "Client $i" -e $wrap $i $client $addr &
done
