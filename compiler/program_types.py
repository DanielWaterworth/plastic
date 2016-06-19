class Type(object):
    def method_signature(self, name):
        raise KeyError('no such method %s on %s' % (name, self))

    def resolve_type(self, types):
        return self

    def is_subtype_of(self, other):
        return self == other

class Void(Type):
    @property
    def size(self):
        return 0

void = Void()

class Bool(Type):
    @property
    def size(self):
        return 1

    def method_signature(self, name):
        return bool_methods[name]

    def method(self, basic_block, object_variable, name, arguments):
        if name == 'and':
            return basic_block.operation('and', [object_variable] + arguments)
        else:
            raise KeyError('no such method %s on %s' % (name, self))

bool = Bool()

bool_methods = {
    'and': ([bool], bool)
}

class Byte(Type):
    @property
    def size(self):
        return 1

byte = Byte()

class UInt(Type):
    @property
    def size(self):
        return 8

uint = UInt()

class NamedType(Type):
    def __init__(self, name):
        self.name = name

    @property
    def size(self):
        raise Exception()

    def resolve_type(self, types):
        return types[self.name]

class Coroutine(Type):
    def __init__(self, receive_type, yield_type):
        self.receive_type = receive_type
        self.yield_type = yield_type

    @property
    def size(self):
        return 8

    def __eq__(self, other):
        return isinstance(other, Coroutine) and self.receive_type == other.receive_type and self.yield_type == other.yield_type

    def __ne__(self, other):
        return not self.__eq__(other)

class Array(Type):
    def __init__(self, ty, count):
        self.ty = ty
        self.count = count

    @property
    def size(self):
        return self.ty.size * self.count

    def resolve_type(self, types):
        self.ty = self.ty.resolve_type(types)
        return self

    def __eq__(self, other):
        return isinstance(other, Array) and self.ty == other.ty and self.count == other.count

    def __ne__(self, other):
        return not self.__eq__(other)

class Tuple(Type):
    def __init__(self, types):
        self.types = types

    @property
    def size(self):
        return sum([t.size for t in self.types])

    def resolve_type(self, types):
        self.types = [t.resolve_type(types) for t in self.types]
        return self

    def __eq__(self, other):
        return isinstance(other, Tuple) and self.types == other.types

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '<Tuple (%s)>' % ', '.join([repr(t) for t in self.types])

class Record(Type):
    def __init__(self, name, attrs, constructor_signatures, methods):
        self.name = name
        self.attrs = attrs
        self.constructor_signatures = constructor_signatures
        self.methods = methods
        self.size = sum([t.size for (_, t) in attrs])

    def method_signature(self, name):
        return self.methods[name]

    def method(self, basic_block, object_variable, name, arguments):
        self.methods[name]
        return basic_block.fun_call('%s#%s' % (self.name, name), [object_variable] + arguments)

class Interface(Type):
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods

    @property
    def size(self):
        raise NotImplementedError('interface object size')

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

    @property
    def size(self):
        raise NotImplementedError('private service object size')

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

    @property
    def size(self):
        raise NotImplementedError('service object size')

    def is_subtype_of(self, other):
        if isinstance(other, Interface):
            return other.name in self.interfaces
        return self == other

    def __repr__(self):
        return "<Service %s>" % self.name
