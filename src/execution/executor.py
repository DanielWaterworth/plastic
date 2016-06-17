from rpython.rlib.rarithmetic import r_ulonglong
from rpython.rlib.rstruct.runpack import runpack

import bytecode
import data

class ActivationRecord(object):
    def __init__(self, function, arguments):
        assert len(function.argument_sizes) == len(arguments)
        for i in xrange(len(arguments)):
            size = function.argument_sizes[i]
            argument = arguments[i]
            assert size == len(argument)

        self.function = function

        block_value_offsets = []
        n_values = 0
        for block in function.blocks:
            block_value_offsets.append(len(arguments) + n_values)
            n_values += len(block.instructions)

        self.values = arguments + ['' for i in xrange(n_values)]
        self.block_value_offsets = block_value_offsets
        self.next_value = len(arguments)
        self.last_block_index = 0
        self.current_block_index = 0
        self.current_block = function.blocks[0]
        self.pc = 0

    def resolve_variable(self, var):
        return self.values[var]

    def resolve_variable_list(self, variables):
        return [self.resolve_variable(var) for var in variables]

    def next_instruction(self):
        if len(self.current_block.instructions) <= self.pc:
            return None
        else:
            return self.current_block.instructions[self.pc]

    def terminator(self):
        return self.current_block.terminator

    def retire(self, value):
        self.values[self.next_value] = value
        self.next_value += 1
        self.pc += 1

    def goto(self, block):
        assert block < len(self.function.blocks)

        self.last_block_index = self.current_block_index
        self.current_block_index = block

        self.next_value = self.block_value_offsets[block]
        self.pc = 0
        self.current_block = self.function.blocks[block]

    def lookup_var(self, var):
        assert var < len(self.values)
        return self.values[var]

class Executor(object):
    def __init__(self, program):
        self.program = program
        self.memory = [0] * 1024**2
        self.stack = [ActivationRecord(program.functions['main'], [])]

    def run(self):
        while True:
            instr = self.stack[-1].next_instruction()
            if instr:
                if isinstance(instr, bytecode.Phi):
                    self.stack[-1].retire(self.stack[-1].resolve_variable(instr.inputs[self.stack[-1].last_block_index]))
                elif isinstance(instr, bytecode.Operation):
                    arguments = self.stack[-1].resolve_variable_list(instr.arguments)
                    if instr.operator == 'sub':
                        a, b = arguments
                        self.stack[-1].retire(data.sub(a, b))
                    elif instr.operator == 'add':
                        a, b = arguments
                        self.stack[-1].retire(data.add(a, b))
                    elif instr.operator == 'eq':
                        a, b = arguments
                        assert len(a) == len(b)
                        self.stack[-1].retire('\1' if a == b else '\0')
                    elif instr.operator == 'lt':
                        a, b = arguments
                        self.stack[-1].retire(data.lt(a, b))
                    elif instr.operator == 'and':
                        a, b = arguments
                        self.stack[-1].retire(data.and_(a, b))
                    elif instr.operator == 'pack':
                        self.stack[-1].retire(''.join(arguments))
                    elif instr.operator == 'slice':
                        start, stop, value = arguments
                        assert len(start) == 8
                        assert len(stop) == 8
                        self.stack[-1].retire(value[runpack('>Q', start):runpack('>Q', stop)])
                    else:
                        raise NotImplementedError('operator not implemented: %s' % instr.operator)
                elif isinstance(instr, bytecode.SysCall):
                    arguments = self.stack[-1].resolve_variable_list(instr.arguments)
                    if instr.function == 'exit':
                        return None
                    elif instr.function == 'print_num':
                        assert len(arguments) == 1
                        a = arguments[0]
                        assert len(a) == 8
                        print runpack('>Q', a)
                        self.stack[-1].retire('')
                    elif instr.function == 'print_bool':
                        assert len(arguments) == 1
                        a = arguments[0]
                        assert len(a) == 1
                        if a != '\0':
                            print 'True'
                        else:
                            print 'False'
                        self.stack[-1].retire('')
                    else:
                        raise NotImplementedError('sys_call not implemented: %s' % instr.function)
                elif isinstance(instr, bytecode.FunctionCall):
                    arguments = self.stack[-1].resolve_variable_list(instr.arguments)
                    self.stack.append(ActivationRecord(self.program.functions[instr.function], arguments))
                elif isinstance(instr, bytecode.Constant):
                    self.stack[-1].retire(instr.value)
                elif isinstance(instr, bytecode.Load):
                    address_bytes = self.stack[-1].resolve_variable(instr.address)
                    assert len(address_bytes) == 8
                    address = runpack('>Q', address_bytes)
                    dat = self.memory[address:address+instr.size]
                    self.stack[-1].retire(''.join([chr(i) for i in dat]))
                elif isinstance(instr, bytecode.Store):
                    address_bytes = self.stack[-1].resolve_variable(instr.address)
                    value = self.stack[-1].resolve_variable(instr.variable)
                    assert len(address_bytes) == 8
                    address = runpack('>Q', address_bytes)
                    for i in xrange(len(value)):
                        self.memory[address+i] = ord(value[i])
                    self.stack[-1].retire('')
                else:
                    raise NotImplementedError('missing instruction implementation')
            else:
                term = self.stack[-1].terminator()
                if isinstance(term, bytecode.Return):
                    value = self.stack[-1].lookup_var(term.variable)
                    assert len(value) == self.stack[-1].function.return_size
                    self.stack.pop()
                    if self.stack:
                        self.stack[-1].retire(value)
                    else:
                        return value
                elif isinstance(term, bytecode.Goto):
                    self.stack[-1].goto(term.block_index)
                elif isinstance(term, bytecode.Conditional):
                    v = self.stack[-1].resolve_variable(term.condition_variable)
                    assert len(v) == 1
                    if v != chr(0):
                        self.stack[-1].goto(term.true_block)
                    else:
                        self.stack[-1].goto(term.false_block)
                elif isinstance(term, bytecode.CatchFireAndDie):
                    raise Exception('catching fire and dying')
                else:
                    raise NotImplementedError('missing terminator implementation')
