import parse
import os.path

def load_imports(filename):
    dir, name = filename.rsplit('/', 1)
    assert name.endswith('.plst')
    name = name[:-5]

    def load_module(module_name):
        with open(os.path.join(dir, module_name) + '.plst', 'r') as fd:
            source = fd.read()
        return parse.parser.parse(source)

    modules = {}
    to_load = [name]
    while to_load:
        module = to_load.pop()
        if not module in modules:
            m = load_module(module)
            modules[module] = m
            to_load.extend(m.imports)

    decls = []
    for module in modules.itervalues():
        for decl in module.decls:
            decls.append(decl)

    return decls