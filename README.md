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
to the namespace. Something like:

    # mynamespace.py
    import namespace
    ns = namespace.Namespace()
    ns.proxy("mynamespace.web", "django")

And then client packages could use this namespace package as:

    import mynamespace.web.forms as forms

That's perhaps not the best example, but hopefully it gets the
idea across.

Other caveats is that this doesn't allow for magical addition to
the namespace if a package elects to be in it. I'm not feeling
creative enough to think of a good solution to this. I'm pretty
sure it could be done with a hook in setuptools though.