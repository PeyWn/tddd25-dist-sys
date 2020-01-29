#!/usr/bin/env bash

# ------------------------------------------------------------------------------
# Distributed Systems (TDDD25)
# ------------------------------------------------------------------------------
# Author: Sergiu Rafiliu (sergiu.rafiliu@liu.se)
# Modified: 24 January 2013
#
# Copyright 2012 Linkoping University
# ------------------------------------------------------------------------------

# Assignment 2
#
# Script for testing the the functioning of the Object Request Broker.
# This script creates a number of peers. Each peer prints the list of peers
# existing at the time of its creation.
# The number of peers is given as an argument to the script, the default is 4.

no_peers=${1:-4}
term='xterm'
wrap='../modules/Common/wrap.sh'
peer='peer.py'

# Run peers.
for ((i=1; i <= $no_peers ; i++)) ; do
    $term -T "Peer $i" -e $wrap $i $peer &
done
