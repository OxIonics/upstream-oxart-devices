""" Driver for Prologix GPIB adapters. """


class GPIB:
    """ Simple pySerial-compatible wrapper for GPIB devices connected to a
    Prologix ethernet/USB <-> GPIB  adapter.

    NB this implementation does not auto-escape data sent to the GPIB
    controller. As a result, any lines beginning with "++" are interpreted as
    commands for the GPIB controller itself instead of being passed on to a
    GPIB device.
    """
    def __init__(self, stream, gpib_addr=0):
        """"
        :param stream: pySerial-compatible interface to the GPIB
          controller. Ethernet <-> GPIB adapters use port 1234
        :param gpib_addr: initial GPIB addr to read/write from/to
        """
        self.stream = stream

        self.stream.write("++savecfg 0\n".encode())
        self.stream.write("++auto 0\n".encode())

        self.gpib_addr = None
        self.set_addr(gpib_addr)

    def set_addr(self, gpib_addr=None):
        """ Sets the controller to address the device at a given GPIB address.
        If gpib_addr is None we keep the current address. """
        if self.gpib_addr == gpib_addr or gpib_addr is None:
            return

        self.gpib_addr = gpib_addr
        self.sock.write("++addr {:d}\n".format(gpib_addr).encode())

    def get_version(self):
        """ Returns a hardware/firmware version string for the GPIB controller.
        """
        self.sock.write("++ver\n".encode())
        return self.sock.readline().decode()

    def read(self, size=1, gpib_addr=None):
        """ Read up to size bytes from the GPIB device at gpib_addr.

        If gpib_addr is None, we write to the last address set.

        If a timeout is set it may return fewer characters than requested,
        otherwise it blocks until the requested number of bytes have been read.
        """
        self.set_addr(gpib_addr)
        self.stream.write("++read_eoi\n".encode())
        return self.stream.read(size)

    def readline(self, gpib_addr=None):
        """ Returns a line terminated with a single '\n' character from the
        GPIB device at gpib_addr.

        If gpib_addr is None, we write to the last address set.

        The final '\n' character and any immediately preceding '\r's are
        trimmed.

        This implementation is dumb and slow. We could (should?) use
        sock.makefile.readline instead, however that has some potential
        compatibility issues.
        """
        self.set_addr(gpib_addr)
        self.stream.write("++read_eoi\n".encode())
        return self.stream.readline()

    def write(self, data, gpib_addr=None):
        """ Sends data to the GPIB device at gpib_addr.
        If gpib_addr is None, we write to the last address set.

        - data must be a bytes-compatible type.
        - Returns the number of bytes written.
        """
        self.set_addr(gpib_addr)
        return self.stream.write(data)

    def get_stream(self, gpib_addr):
        """ Create an interface to the device at a given GPIB address. """
        return self.stream(self, gpib_addr)

    def ping(self):
        """" Returns True if it receives a non-empty version string from the
        controller """
        return bool(self.get_version())

    class Stream:
        """ pySerial-compatible interface to a single GPIB device. """

        def __init__(self, bus, addr):
            """ :param bus: a GPIB controller """
            self.bus = bus
            self.addr = addr

        def read(self, size=1):
            """ Read up to size bytes from the GPIB device.

            If a timeout is set it may return fewer characters than requested,
            otherwise it blocks until the requested number of bytes have been
            read.
            """
            return self.bus.read(size, self.addr)

        def readline(self, gpib_addr=None):
            """ Returns a line terminated with a single '\n' character from the
            GPIB device .

            The final '\n' character and any immediately preceding '\r's are
            trimmed.

            This implementation is dumb and slow. We could (should?) use
            sock.makefile.readline instead, however that has some potential
            compatibility issues.
            """
            return self.stream.readline(self.addr)

        def write(self, data, gpib_addr=None):
            """ Sends data to the GPIB device.

            - data must be a bytes-compatible type.
            - Returns the number of bytes written.
            """
            return self.bus.write(data, self.addr)