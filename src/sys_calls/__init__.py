import data
import sys_calls.ffi
import sys_calls.stdout
import sys_calls.socket
import sys_calls.epoll
import sys_calls.file
from rpython.rlib.rstruct.runpack import runpack
from rpython.rlib.rarithmetic import r_longlong, r_ulonglong, r_int, intmask

class SysCallInterface(object):
    def sys_call(self, name, arguments):
        raise NotImplementedError()

class Perform(SysCallInterface):
    def __init__(self, program):
        self.program = program

    def sys_call(self, name, arguments):
        if name == 'bytecode_file':
            assert len(arguments) == 0
            return [data.ByteString(self.program)]
        else:
            return data.sys_calls[name].call(arguments)

class TraceProxy(SysCallInterface):
    def __init__(self, target, fd):
        self.target = target
        self.fd = fd

    def sys_call(self, name, arguments):
        values = self.target.sys_call(name, arguments)

        self.fd.write(data.pack_uint(len(name)))
        self.fd.write(name)

        self.fd.write(data.pack_uint(len(arguments)))
        for arg in arguments:
            arg.persist(self.fd)

        self.fd.write(data.pack_uint(len(values)))
        for value in values:
            value.persist(self.fd)

        return values

class EofFd(object):
    def __init__(self, fd):
        self.fd = fd

    def read(self, n):
        chunk = self.fd.read(n)
        if len(chunk) < n:
            raise EOFError()
        return chunk

class Replay(SysCallInterface):
    def __init__(self, fd):
        self.fd = EofFd(fd)

    def sys_call(self, name, arguments):
        n = intmask(runpack('>Q', self.fd.read(8)))
        expected_name = self.fd.read(n)

        n = intmask(runpack('>Q', self.fd.read(8)))
        expected_arguments = [data.load(self.fd) for i in xrange(n)]

        n = intmask(runpack('>Q', self.fd.read(8)))
        return_values = [data.load(self.fd) for i in xrange(n)]

        assert expected_name == name
        assert len(expected_arguments) == len(arguments)
        for i in xrange(len(expected_arguments)):
            expected = expected_arguments[i]
            arg = arguments[i]
            if not expected.eq(arg):
                raise Exception('expected %s to equal %s' % (expected, arg))
        return return_values

def read_trace(fd):
    trace = []
    try:
        while True:
            b = fd.read(8)
            if not b:
                break
            n = runpack('>Q', b)
            name = fd.read(n)

            n = runpack('>Q', fd.read(8))
            arguments = [data.load(fd) for i in xrange(n)]

            n = runpack('>Q', fd.read(8))
            return_values = [data.load(fd) for i in xrange(n)]

            trace.append((name, arguments, return_values))
    except:
        pass
    return trace
