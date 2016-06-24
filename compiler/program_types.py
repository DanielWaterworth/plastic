class Type(object):
    def method_signature(self, name):
        raise KeyError('no such method %s on %s' % (name, self))

    def resolve_type(self, modules, types):
        return self

    def is_subtype_of(self, other):
        return self == other

class Primitive(Type):
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods

    def method_signature(self, name):
        return self.methods[name][0]

    def method(self, basic_block, object_variable, name, arguments):
        operator = self.methods[name][1]
        return basic_block.operation(operator, [object_variable] + arguments)

    def match(self, _, other):
        assert isinstance(other, Primitive) and self.name == other.name

    def template(self, _):
        return self

void = Primitive('void', {})

bool_methods = {}
bool = Primitive('bool', bool_methods)

byte_methods = {}
byte = Primitive('byte', byte_methods)

bytestring_methods = {}
bytestring = Primitive('bytestring', bytestring_methods)

char_methods = {}
char = Primitive('char', char_methods)

string_methods = {}
string = Primitive('string', string_methods)

uint_methods = {}
uint = Primitive('uint', uint_methods)

socket = Primitive('socket', {})

class NamedType(Type):
    def __init__(self, module, name):
        self.module = module
        self.name = name

    def resolve_type(self, modules, types):
        if self.module:
            return modules[self.module].types[self.name]
        else:
            return types[self.name]

    def resolve_interface(self, modules, interface_types):
        if self.module:
            return modules[self.module].interface_types[self.name]
        else:
            return interface_types[self.name]

class Variable(Type):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name

    def match(self, quantified, other):
        if self.name in quantified:
            assert quantified[self.name] == other
        else:
            quantified[self.name] = other

    def template(self, quantified):
        return quantified[self.name]

class Coroutine(Type):
    def __init__(self, receive_type, yield_type):
        self.receive_type = receive_type
        self.yield_type = yield_type

    def __eq__(self, other):
        return isinstance(other, Coroutine) and self.receive_type == other.receive_type and self.yield_type == other.yield_type

    def __ne__(self, other):
        return not self.__eq__(other)

class Tuple(Type):
    def __init__(self, types):
        self.types = types

    def resolve_type(self, modules, types):
        self.types = [t.resolve_type(modules, types) for t in self.types]
        return self

    def __eq__(self, other):
        return isinstance(other, Tuple) and self.types == other.types

    def __ne__(self, other):
        return not self.__eq__(other)

    def match(self, quantified, other):
        assert isinstance(other, Tuple)
        assert len(self.types) == len(other.types)
        for a, b in zip(self.types, other.types):
            a.match(quantified, b)

    def template(self, quantified):
        return Tuple([t.template(quantified) for t in self.types])

    def __repr__(self):
        return '<Tuple (%s)>' % ', '.join([repr(t) for t in self.types])

class Record(Type):
    def __init__(self, name, attrs, constructor_signatures, methods):
        self.name = name
        self.attrs = attrs
        self.constructor_signatures = constructor_signatures
        self.methods = methods

    def method_signature(self, name):
        return self.methods[name]

    def method(self, basic_block, object_variable, name, arguments):
        self.methods[name]
        return basic_block.fun_call('%s#%s' % (self.name, name), [object_variable] + arguments)

    def match(self, _, other):
        assert self == other

    def template(self, _):
        return self

class Enum(Type):
    def __init__(self, name, constructors):
        self.name = name
        self.constructors = constructors

    def match(self, _, other):
        assert self == other

    def template(self, _):
        return self

class Interface(Type):
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods

    def method_signature(self, name):
        return self.methods[name]

    def method(self, basic_block, object_variable, name, arguments):
        return basic_block.fun_call("%s#%s" % (self.name, name), [object_variable] + arguments)

    def __repr__(self):
        return "<Interface %s>" % self.name

# Type used for self in a service context
class PrivateService(Type):
    def __init__(self, name, private_methods):
        self.private_methods = private_methods

class Service(Type):
    def __init__(self, name, dependencies, attrs, constructor_signatures, interfaces):
        self.name = name
        self.dependencies = dependencies
        self.attrs = attrs
        self.constructor_signatures = constructor_signatures
        self.interfaces = interfaces

    @property
    def all_attrs(self):
        all_attrs = dict(self.attrs)
        all_attrs.update(dict(self.dependencies))
        return all_attrs

    @property
    def dependency_types(self):
        return [t for _, t in self.dependencies]

    def is_subtype_of(self, other):
        if isinstance(other, Interface):
            return other in self.interfaces
        return self == other

    def __repr__(self):
        return "<Service %s>" % self.name

uint_methods.update({
    'to_string': (([], string), 'uint.to_string')
})

byte_methods.update({
    'to_bytestring': (([], bytestring), 'byte.to_bytestring'),
    'to_uint': (([], uint), 'byte.to_uint'),
})

char_methods.update({
    'to_string': (([], string), 'char.to_string')
})

bytestring_methods.update({
    'drop': (([uint], bytestring), 'bytestring.drop'),
    'take': (([uint], bytestring), 'bytestring.take'),
    'index': (([uint], byte), 'bytestring.index'),
    'slice': (([uint, uint], bytestring), 'bytestring.slice'),
    'length': (([], uint), 'bytestring.length'),
    'decode_utf8': (([], string), 'bytestring.decode_utf8')
})

string_methods.update({
    'head': (([], char), 'string.head'),
    'drop': (([uint], string), 'string.drop'),
    'encode_utf8': (([], bytestring), 'string.encode_utf8')
})
