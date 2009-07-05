"""
namespace.py
============

In a nutshell, namespace.py allows you to create composite namespace
packages without altering any submodule.

    >>> import namespace
    >>> ns = namespace.Namespace()
    >>> ns.proxy("ns.path", "os.path")
    >>> import ns.path
    >>> import sys
    >>> ns.path == sys.modules["os.path"]
    True

The general idea here is that you'd create a PyPI package for
the namespace and then attach the individual subpackages
to the namespace.

Something like::

    # mynamespace.py
    import namespace
    ns = namespace.Namespace()
    ns.proxy("mynamespace.web", "django")

And then client packages could use this namespace package as::

    import mynamespace.web.forms as forms

That's perhaps not the best example, but hopefully it gets the
idea across.

Other caveats is that this doesn't allow for magical addition to
the namespace if a package elects to be in it. I'm not feeling
creative enough to think of a good solution to this. I'm pretty
sure it could be done with a hook in setuptools though.

"""

import new
import os
import sys

class Namespace(object):
    def __init__(self):
        self.namespaces = set()
        self.proxied = {}
        sys.meta_path.append(self)

    def proxy(self, proxyas, originalmod):
        if proxyas in sys.modules:
            raise ValueError("Unable to proxy a loaded module: %s" % proxyas)
        self.proxied[proxyas] = originalmod
        bits = proxyas.split(".")
        for idx in range(1, len(bits)):
            newns = ".".join(bits[:idx])
            self.namespaces.add(newns)
            if newns not in sys.modules:
                continue
            if not hasattr(sys.modules[newns], "__path__"):
                sys.modules[newns].__path__ = []

    def find_module(self, fullname, path=None):
        if fullname in self.namespaces or fullname in self.proxied:
            return self

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        if fullname in self.namespaces:
            mod = new.module(fullname)
            mod.__loader__ = self
            mod.__file__ = '<namespace %r>' % fullname
            mod.__path__ = []
            return mod
        orig = self.proxied[fullname]
        if orig in sys.modules:
            return sys.modules[orig]
        mod = __import__(orig)
        for bit in orig.split(".")[1:]:
            mod = getattr(mod, bit)
        sys.modules[fullname] = mod
        return mod
