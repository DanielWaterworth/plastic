from rpython.rlib.rstruct.runpack import runpack
from rpython.rlib.rarithmetic import r_ulonglong, r_int, intmask

MAGIC_START = r_ulonglong(17810926409145293181)

# Top level
SYMBOL = 1
FUNCTION_START = 2

# Instructions
PHI = 1

CONST = 8
CONST_UINT = 9
CONST_BYTE = 10
VOID = 11
OPERATION = 32
SYS_CALL = 33
FUN_CALL = 34
NEW_COROUTINE = 35
LOAD = 64
STORE = 65
RUN_COROUTINE = 66
YIELD = 67
RESUME = 68

RET = 129
GOTO = 130
CONDITIONAL = 131
CATCH_FIRE_AND_DIE = 132
