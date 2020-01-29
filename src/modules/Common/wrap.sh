#!/usr/bin/env bash

# ------------------------------------------------------------------------------
# Distributed Systems (TDDD25)
# ------------------------------------------------------------------------------
# Author: Sergiu Rafiliu (sergiu.rafiliu@liu.se)
# Modified: 24 January 2013
#
# Copyright 2012 Linkoping University
# ------------------------------------------------------------------------------

# Wrapper for client, server, and *peer scripts. This wrapper will not allow
# the terminal to close if the script exits with an error.
# The arguments to this script are supposed to be the script to run and its
# agruments.
# ------------------------------------------------------------------------------

errfile="error$1.tmp"
shift

./$@ 2> $errfile

if [[ -s $errfile ]] ; then
    cat $errfile
    echo -n 'Press any key to close this terminal ...'
    read
fi

rm -rf $errfile

