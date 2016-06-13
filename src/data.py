from rpython.rlib.rstruct.runpack import runpack

def pack_uint(n):
    output = []
    for i in xrange(8):
        output.append(chr(n & 0xff))
        n = n >> 8
    output.reverse()
    return ''.join(output)

def pack_bool(b):
    if b:
        return chr(1)
    else:
        return chr(0)

def sub(a, b):
    assert len(a) == 8
    assert len(b) == 8
    return pack_uint(runpack('>Q', a) - runpack('>Q', b))

def add(a, b):
    assert len(a) == 8
    assert len(b) == 8
    return pack_uint(runpack('>Q', a) + runpack('>Q', b))

def lt(a, b):
    assert len(a) == 8
    assert len(b) == 8
    return pack_bool(runpack('>Q', a) < runpack('>Q', b))

def and_(a, b):
    assert len(a) == 1
    assert len(b) == 1
    return '\1' if (a != '\0') and (b != '\0') else '\0'
