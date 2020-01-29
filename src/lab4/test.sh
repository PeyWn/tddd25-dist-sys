#!/usr/bin/env bash

# ------------------------------------------------------------------------------
# Distributed Systems (TDDD25)
# ------------------------------------------------------------------------------
# Author: Sergiu Rafiliu (sergiu.rafiliu@liu.se)
# Modified: 24 January 2013
#
# Copyright 2012 Linkoping University
# ------------------------------------------------------------------------------

# Assignment 4
#
# Script for testing the the functioning of distributed mutual exclusion.
# This script creates a number of mutexPeers that communicate with each other.
# The number of peers is given as an argument to the script, the default is 4.

no_peers=${1:-4}
term='xterm'
wrap='../modules/Common/wrap.sh'
peer='mutexPeer.py'

# Run peers.
for ((i=1; i <= $no_peers ; i++)) ; do
    $term -T "Mutex Peer $i" -e $wrap $i $peer &
done
