#!/usr/bin/env python3

# -----------------------------------------------------------------------------
# Distributed Systems (TDDD25)
# -----------------------------------------------------------------------------
# Author: Sergiu Rafiliu (sergiu.rafiliu@liu.se)
# Modified: 31 July 2013
#
# Copyright 2012 Linkoping University
# -----------------------------------------------------------------------------

"""Client reader/writer for a fortune database."""

import sys
import argparse

sys.path.append("../modules")
from Common import orb
from Common.nameServiceLocation import name_service_address
from Common.objectType import object_type

# -----------------------------------------------------------------------------
# Initialize and read the command line arguments
# -----------------------------------------------------------------------------

description = """\
Client for a fortune database. It reads a random fortune from the database.\
"""

parser = argparse.ArgumentParser(description=description)
parser.add_argument(
    "-w", "--write", metavar="FORTUNE", dest="fortune",
    help="Write a new fortune to the database."
)
parser.add_argument(
    "-i", "--interactive", action="store_true", dest="interactive",
    default=False, help="Interactive session with the fortune database."
)
parser.add_argument(
    "-t", "--type", metavar="TYPE", dest="type", default=object_type,
    help="Set the client's type."
)
parser.add_argument(
    "-p", "--peer", metavar="PEER_ID", dest="peer_id", type=int,
    help="The identifier of a particular server peer."
)
opts = parser.parse_args()

server_type = opts.type
server_id = opts.peer_id
assert server_type != "object", "Change the object type to something unique!"

# -----------------------------------------------------------------------------
# The main program
# -----------------------------------------------------------------------------

# Connect to the name service to obtain the address of the server.
ns = orb.Stub(name_service_address)

if server_id is None:
    server_address = tuple(ns.require_any(server_type))
else:
    server_address = tuple(ns.require_object(server_type, server_id))

print("Connecting to server: {}".format(server_address))

# Create the database object.
db = orb.Stub(server_address)

if not opts.interactive:
    # Run in the normal mode.
    if opts.fortune is not None:
        print("Writing '{}' to the fortune database.".format(opts.fortune))
        db.write(opts.fortune)
    else:
        print(db.read())

else:
    # Run in the interactive mode.
    def menu():
        print("""\
Choose one of the following commands:
    r            ::  read a random fortune from the database,
    w <FORTUNE>  ::  write a new fortune into the database,
    h            ::  print this menu,
    q            ::  exit.\
""")

    command = ""
    menu()
    while command != "q":
        sys.stdout.write("Command> ")
        command = input()
        if command == "r":
            print(db.read())
        elif (len(command) > 1 and command[0] == "w" and
                command[1] in [" ", "\t"]):
            db.write(command[2:].strip())
        elif command == "h":
            menu()
