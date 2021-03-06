import ply.lex as lex

tokens = [
    "CHAR",
    "NUMBER",
    "COLON",
    "SEMICOLON",
    "COMMA",
    "DOT",
    "PIPE",
    "ASSIGNMENT",
    "ARROW",
    "OPEN_PARENS",
    "CLOSE_PARENS",
    "OPEN_SQUARE",
    "CLOSE_SQUARE",
    "UPPER_NAME",
    "LOWER_NAME",
    "PROPERTY",
    "STRING",
    "PLUS",
    "MINUS",
    "MUL",
    "DIV",
    "EQ",
    "NE",
    "LT",
    "GT",
    "LE",
    "GE",
    "COMMENT",
    "WHITESPACE",
]
keywords = [
    'attr',
    'and',
    'constructor',
    'coroutine',
    'debug',
    'define',
    'do',
    'elsif',
    'else',
    'end',
    'entry',
    'enum',
    'false',
    'for',
    'if',
    'implements',
    'import',
    'in',
    'interface',
    'is_done',
    'match',
    'not',
    'op',
    'or',
    'private',
    'resume',
    'return',
    'run',
    'service',
    'sys',
    'throw',
    'true',
    'void',
    'while',
    'yield',
]
keywords = {keyword: keyword.upper() for keyword in keywords}
tokens += keywords.values()

def t_CHAR(t):
    r"'([^\\']|(\\(\\|a|b|f|n|r|t|v|'|(u[0-9a-f]{4})|(U[0-9a-f]{8}))))'"
    value = t.value
    if value[1] == '\\':
        if value[2] == 'a':
            t.value = '\a'
        elif value[2] == 'b':
            t.value = '\b'
        elif value[2] == 'f':
            t.value = '\f'
        elif value[2] == 'n':
            t.value = '\n'
        elif value[2] == 'r':
            t.value = '\r'
        elif value[2] == 't':
            t.value = '\t'
        elif value[2] == 'v':
            t.value = '\v'
        elif value[2] == '\'':
            t.value = '\''
        elif value[2] == '\\':
            t.value = '\\'
        elif value[2] == 'u':
            t.value = unichr(int(value[3:7], 16))
        elif value[2] == 'U':
            t.value = unichr(int(value[3:11], 16))
        else:
            raise Exception()
    else:
        t.value = value[1]
    return t

t_NUMBER = r'\d+'
t_COLON = r':'
t_SEMICOLON = r';'
t_DOT = r'\.'
t_COMMA = r','
t_PIPE = r'\|'
t_ASSIGNMENT = r':='
t_ARROW = r'->'
t_OPEN_PARENS = r'\('
t_CLOSE_PARENS = r'\)'
t_OPEN_SQUARE = r'\['
t_CLOSE_SQUARE = r'\]'
t_UPPER_NAME = r'[A-Z][a-zA-Z0-9]*'

def t_LOWER_NAME(t):
    r'[a-z][a-z0-9_]*'
    if t.value in keywords:
        t.type = keywords[t.value]
    return t

t_PROPERTY = r'@[a-z][a-z0-9_]*'
t_STRING = r'"(\\.|[^"])*"'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MUL = r'\*'
t_DIV = r'\\'
t_EQ = r'=='
t_NE = r'!='
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='

def t_COMMENT(t):
    r'\#[^\n]*\n'
    pass

def t_WHITESPACE(t):
    r'\s'
    pass

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

lexer = lex.lex()
