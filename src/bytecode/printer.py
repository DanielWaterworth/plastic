class BasicBlockPrinter(object):
    def __init__(self, function, i):
        self.function = function
        self.i = i

    def __enter__(self):
        print "  BASIC BLOCK START %d" % self.i
        return self

    def __exit__(self, type, value, traceback):
        if not value:
            print "  BASIC BLOCK END %d" % self.i

    def instruction(self, t, *args):
        var = self.function.create_variable()
        print "    %s: %s(%s)" % (var, t, ', '.join([repr(arg) for arg in args]))
        return var

    def terminator(self, t, *args):
        print "    %s(%s)" % (t, ', '.join([repr(arg) for arg in args]))

    def phi(self, inputs):
        return self.instruction("PHI", inputs)

    def copy(self):
        return self.instruction("COPY")

    def move(self, variable):
        return self.instruction("MOVE", variable)

    def unpack(self):
        return self.instruction("UNPACK")

    def constant_bool(self, value):
        return self.instruction("CONST_BOOL", value)

    def constant_byte(self, value):
        return self.instruction("CONST_BYTE", value)

    def constant_char(self, value):
        return self.instruction("CONST_CHAR", value)

    def constant_bytestring(self, value):
        return self.instruction("CONST_BYTESTRING", value)

    def constant_string(self, value):
        return self.instruction("CONST_STRING", value)

    def constant_uint(self, value):
        return self.instruction("CONST_UINT", value)

    def constant_int(self, value):
        return self.instruction("CONST_INT", value)

    def constant_double(self, value):
        return self.instruction("CONST_DOUBLE", value)

    def void(self):
        return self.instruction("VOID")

    def operation(self, name, arguments):
        return self.instruction("OPERATION", name, arguments)

    def sys_call(self, name, arguments):
        return self.instruction("SYS_CALL", name, arguments)

    def fun_call(self, name, arguments):
        return self.instruction("FUN_CALL", name, arguments)

    def debug(self, value):
        return self.instruction("DEBUG", value)

    def new_coroutine(self, name, arguments):
        return self.instruction("NEW_COROUTINE", name, arguments)

    def load(self, address):
        return self.instruction("LOAD", address)

    def store(self, address, value):
        return self.instruction("STORE", address, value)

    def get(self):
        return self.instruction("GET")

    def put(self, variable):
        return self.instruction("PUT", variable)

    def run_coroutine(self, coroutine):
        return self.instruction("RUN_COROUTINE", coroutine)

    def yield_(self, value):
        return self.instruction("YIELD", value)

    def resume(self, coroutine, value):
        return self.instruction("RESUME", coroutine, value)

    def ret_multiple(self, variables):
        self.terminator("RET", variables)

    def ret(self, variable):
        return self.ret_multiple([variable])

    def goto(self, block):
        self.terminator("GOTO", block)

    def conditional(self, variable, true_block, false_block):
        self.terminator("CONDITIONAL", variable, true_block, false_block)

    def catch_fire_and_die(self):
        self.terminator("CATCH_FIRE_AND_DIE")

    def throw(self, exception):
        self.terminator("THROW", exception)

class FunctionPrinter(object):
    def __init__(self, name, num_arguments, num_return_values):
        self.name = name
        self.num_arguments = num_arguments
        self.num_return_values = num_return_values
        self.next_variable = num_arguments
        self.num_basic_blocks = 0

    def create_variable(self):
        i = self.next_variable
        self.next_variable += 1
        return i

    def __enter__(self):
        print ("FUNCTION START", self.name, self.num_arguments)
        return (self, [i for i in xrange(self.num_arguments)])

    def __exit__(self, type, value, traceback):
        if not value:
            print "FUNCTION END"

    def basic_block(self):
        i = self.num_basic_blocks
        self.num_basic_blocks += 1
        return BasicBlockPrinter(self, i)

class ProgramPrinter(object):
    def function(self, name, num_arguments, num_return_values=1):
        return FunctionPrinter(name, num_arguments, num_return_values)

class BytecodePrinter(object):
    def __enter__(self):
        print "PROGRAM START"
        return ProgramPrinter()

    def __exit__(self, type, value, traceback):
        if not value:
            print "PROGRAM END"
