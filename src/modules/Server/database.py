# -----------------------------------------------------------------------------
# Distributed Systems (TDDD25)
# -----------------------------------------------------------------------------
# Author: Sergiu Rafiliu (sergiu.rafiliu@liu.se)
# Modified: 24 July 2013
#
# Copyright 2012 Linkoping University
# -----------------------------------------------------------------------------

"""Implementation of a simple database class."""

import random


class Database(object):

    """Class containing a database implementation."""

    def __init__(self, db_file):
        self.db_file = db_file
        self.rand = random.Random()
        self.rand.seed()
        self.fortunes = []
        with open(self.db_file, 'r') as DB:
            line = DB.readline()
            fortune = ''
            while line:
                if (line == '%\n'):
                    self.fortunes.append(fortune)
                    fortune = ''
                else:
                    fortune += line
                line = DB.readline()

    def read(self):
        """Read a random location in the database."""
        if self.fortunes == []: return
        return self.rand.choice(self.fortunes)

    def write(self, fortune):
        """Write a new fortune to the database."""
        with open(self.db_file, 'a') as DB:
            try:
                DB.write(fortune+'\n%\n')
            finally:
                self.fortunes.append(fortune)
