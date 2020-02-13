# -----------------------------------------------------------------------------
# Distributed Systems (TDDD25)
# -----------------------------------------------------------------------------
# Author: Sergiu Rafiliu (sergiu.rafiliu@liu.se)
# Modified: 16 March 2017
#
# Copyright 2012-2017 Linkoping University
# -----------------------------------------------------------------------------

import threading
import socket
import json

"""Object Request Broker

This module implements the infrastructure needed to transparently create
objects that communicate via networks. This infrastructure consists of:

--  Strub ::
        Represents the image of a remote object on the local machine.
        Used to connect to remote objects. Also called Proxy.
--  Skeleton ::
        Used to listen to incoming connections and forward them to the
        main object.
--  Peer ::
        Class that implements basic bidirectional (Stub/Skeleton)
        communication. Any object wishing to transparently interact with
        remote objects should extend this class.

"""


class CommunicationError(Exception):
    pass


class Stub(object):

    """ Stub for generic objects distributed over the network.

    This is  wrapper object for a socket.

    """

    def __init__(self, address):
        self.address = tuple(address)

    def _rmi(self, method, *args):
        #
        # Your code here.
        #
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(self.address)
            worker = sock.makefile(mode="rw")
            worker.write(json.dumps(
                {"method": method, "args": args}) + '\n')
            worker.flush()
            data = json.loads(worker.readline())
            if not data:
                raise(Exception('No data received'))
            if 'error' in data:
                exception = type(data["error"]["name"], (Exception,), dict())
                raise exception(*data["error"]["args"])
            if 'result' in data:
                return data['result']
            else:
                print('Wrong format on server response')
        except Exception as e:
            return e
        finally:
            sock.close()

    def __getattr__(self, attr):
        """Forward call to name over the network at the given address."""
        def rmi_call(*args):
            return self._rmi(attr, *args)
        return rmi_call


class Request(threading.Thread):

    """Run the incoming requests on the owner object of the skeleton."""

    def __init__(self, owner, conn, addr):
        threading.Thread.__init__(self)
        self.addr = addr
        self.conn = conn
        self.owner = owner
        self.daemon = True

    def run(self):
        #
        # Your code here.
        #
        try:
            worker = self.conn.makefile(mode="rw")
            request = worker.readline()
            request = json.loads(request)
            if 'method' in request and 'args' in request and hasattr(self.owner, request['method']):
                method = getattr(self.owner, request['method'])
                if request['args']:
                    result = method(*request['args'])
                else:
                    result = method()
            msg = json.dumps({"result": result})
            worker.write(msg + '\n')
            worker.flush()
        except Exception as e:
            return e
        finally:
            self.conn.close()


class Skeleton(threading.Thread):

    """ Skeleton class for a generic owner.

    This is used to listen to an address of the network, manage incoming
    connections and forward calls to the generic owner class.

    """

    def __init__(self, owner, address):
        threading.Thread.__init__(self)
        self.address = address
        self.owner = owner
        self.daemon = True
        #
        # Your code here.
        #
        pass

    def run(self):
        #
        # Your code here.
        #
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(self.address)
        sock.listen(1)

        try:
            while self.daemon:
                try:
                    conn, addr = sock.accept() 
                    req = Request(self.owner, conn, addr)
                    req.start()
                except socket.error:
                    continue
        except Exception as e:
            print(e)
        finally:
            sock.close()



class Peer:

    """Class, extended by objects that communicate over the network."""

    def __init__(self, l_address, ns_address, ptype):
        self.type = ptype
        self.hash = ""
        self.id = -1
        self.address = l_address
        self.skeleton = Skeleton(self, ('', l_address[1]))
        self.name_service_address = ns_address
        self.name_service = Stub(self.name_service_address)

    # Public methods

    def start(self):
        """Start the communication interface."""
        self.skeleton.start()
        self.id, self.hash = self.name_service.register(self.type,
                                                        self.address)

    def destroy(self):
        """Unregister the object before removal."""

        self.name_service.unregister(self.id, self.type, self.hash)

    def check(self):
        """Checking to see if the object is still alive."""

        return (self.id, self.type)
