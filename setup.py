from distutils.core import setup

import namespace

setup(
    name = "namespace",
    description = "Create composite namespace packages.",
    long_description = namespace.__doc__,
    author = "Paul J. Davis",
    author_email = "paul.joseph.davis@gmail.com",
    url = "http://github.com/davisp/namespace",
    version = "0.0.1",
    license = "MIT",
    keywords = "packaging namespace",
    platforms = ["any"],
    py_modules = ["namespace"]
)
