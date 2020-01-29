#!/usr/bin/env bash

# ------------------------------------------------------------------------------
# Distributed Systems (TDDD25)
# ------------------------------------------------------------------------------
# Author: Sergiu Rafiliu (sergiu.rafiliu@liu.se)
# Modified: 24 January 2013
#
# Copyright 2012 Linkoping University
# ------------------------------------------------------------------------------

# Assignment 5
#
# Script for testing the the functioning of a distributed client-server systems
# with rendundant replicas. This distributed system is composed of:
#   --  a Name Service
#   --  a number of servers which replicate the database, they interract in a
#       peer-to-peer fashion
#   --  an number of clients, each connecting to one of the servers.
#
# Script usage :
#       test.sh [-s no] [-c no]
#   Optional arguments :
#       -s no   ::  number of servers, default 2
#       -c no   ::  number of clients, default 4
#
# This script creates a number of servers and clients, each in a different
# terminal.

no_clients=4
no_servers=2
term=xterm
wrap='../modules/Common/wrap.sh'
client='client.py -i'
server='serverPeer.py'

dbdir='dbs/'
dbext='.db'
database='fortune'

# Read arguments.
while [[ $# > 0 ]] ; do
	case $1 in
		-s) shift ; no_servers=$1 ; shift ;;
		-c) shift ; no_clients=$1 ; shift ;;
		*) break ;;
	esac
done

# Run servers.
for ((i=1; i <= $no_servers ; i++)) ; do
    dbfile="${dbdir}${database}_${i}${dbext}"
    cp "${dbdir}${database}${dbext}" $dbfile
    $term -T "Server $i" -e $wrap "s$i" $server -f $dbfile &
done

sleep 1

# Run clients.
for ((i=1; i <= $no_clients ; i++)) ; do
    $term -T "Client $i" -e $wrap $i $client &
done

