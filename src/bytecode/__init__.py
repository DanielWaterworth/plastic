class Program(object):
    def __init__(self, functions):
        self.functions = functions

class Function(object):
    def __init__(self, name, num_arguments, num_return_values, blocks):
        self.name = name
        self.num_arguments = num_arguments
        self.num_return_values = num_return_values
        self.blocks = blocks

class BasicBlock(object):
    def __init__(self, instructions, terminator):
        self.instructions = instructions
        self.terminator = terminator

class Instruction(object):
    pass

class Phi(Instruction):
    def __init__(self, inputs):
        self.inputs = inputs

class Copy(Instruction):
    pass

class Move(Instruction):
    def __init__(self, variable):
        self.variable = variable

class Operation(Instruction):
    def __init__(self, operator, arguments):
        self.operator = operator
        self.arguments = arguments

class FunctionCall(Instruction):
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments

class SysCall(Instruction):
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments

class NewCoroutine(Instruction):
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments

class Debug(Instruction):
    def __init__(self, value):
        self.value = value

class ConstantBool(Instruction):
    def __init__(self, value):
        self.value = value

class ConstantByte(Instruction):
    def __init__(self, value):
        self.value = value

class ConstantChar(Instruction):
    def __init__(self, value):
        self.value = value

class ConstantByteString(Instruction):
    def __init__(self, value):
        self.value = value

class ConstantString(Instruction):
    def __init__(self, value):
        self.value = value

class ConstantInt(Instruction):
    def __init__(self, value):
        self.value = value

class ConstantUInt(Instruction):
    def __init__(self, value):
        self.value = value

class ConstantDouble(Instruction):
    def __init__(self, value):
        self.value = value

class Void(Instruction):
    pass

class Load(Instruction):
    def __init__(self, address):
        self.address = address

class Store(Instruction):
    def __init__(self, address, variable):
        self.address = address
        self.variable = variable

class Get(Instruction):
    pass

class Put(Instruction):
    def __init__(self, variable):
        self.variable = variable

class RunCoroutine(Instruction):
    def __init__(self, coroutine):
        self.coroutine = coroutine

class Yield(Instruction):
    def __init__(self, value):
        self.value = value

class Resume(Instruction):
    def __init__(self, coroutine, value):
        self.coroutine = coroutine
        self.value = value

class Terminator(object):
    pass

class Return(Terminator):
    def __init__(self, variables):
        self.variables = variables

class Goto(Terminator):
    def __init__(self, block_index):
        self.block_index = block_index

class Conditional(Terminator):
    def __init__(self, condition_variable, true_block, false_block):
        self.condition_variable = condition_variable
        self.true_block = true_block
        self.false_block = false_block

class CatchFireAndDie(Terminator):
    pass

class Throw(Terminator):
    def __init__(self, exception):
        self.exception = exception
