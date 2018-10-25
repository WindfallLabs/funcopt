# -*- coding: utf-8 -*-
"""
Simple self-documenting commandline interfaces with encapsulated execution
logic powered by docopt.

funcopt uses `inspect` to create docopt docstrings that
in-turn create simple commandline interfaces. With docopt, the user must write
the documentation that exactly matches docopt's requirements and then the
execution logic to match. With funcopt, users write their functions. That's it.

 * Licensed under the terms of the MIT license (see LICENSE)
 * Copyright (c) 2018 Garin Wally, garwall101@gmail.com
"""

import os
import re
import sys
import inspect

import docopt
from pprint import pprint


__version__ = "1.0.0"

_default_docstring = """
Usage:
    {usage}

Options:
    -h, --help        Show this help message and exit
    -v, --verbose     Print status messages (WIP)
    -q, --quiet       Write all messages to the void
    --version         Show program's version number and exit
    --debug           Show the docopt dictionary of parameters passed
    --docstring       Shows the docstring for the given function and exit
"""


def type_parser(str_val):
    if not isinstance(str_val, str) or str_val == "":
        return str_val
    elif re.sub("\d", "", str_val) == "":
        return int(str_val)
    elif re.sub("\d", "", str_val) == ".":
        return float(str_val)
    elif re.sub("True", "", str_val) == "":
        return True
    elif re.sub("False", "", str_val) == "":
        return False
    elif re.sub("None", "", str_val) == "":
        return None
    return str_val
    

class FunctionCallError(NameError):
    pass


class CLI(object):
    def __init__(self, _file, module, docstring=None, version=None, _all=True):
        """Commandline Interface.
        Args:
            _file (str): name of current script; e.g. '__file__'
            module (str): current module; e.g. '__name__'
            docstring (str): docstring to add docopt reqs to; e.g. '__doc__'
            version (str): version number
            _all (bool, list): provide API to all public functions (default: True)
                can also be list, e.g. '__all__'
        """
        self._file = _file
        self._module = module
        self._all = _all
        if docstring:
            self.doc = docstring + _default_docstring.format(
                usage=self._make_usage())
        self.version = version

        # Use the magic of docopt here
        try:
            self.args = docopt.docopt(self.doc, version=self.version)
            for arg, val in self.args.items():
                self.args[arg] = type_parser(val)
        except (docopt.DocoptExit):
            self.args = {}
            if sys.argv[1].startswith("_"):
                raise FunctionCallError(
                    "private function '{}' is ignored".format(sys.argv[1]))
            else:
                raise FunctionCallError("Function not found in current module")

        # Global Quiet Mode -- Writes all output to null buffer
        self._void = open(os.devnull, "w")

    def run(self):
        """Process command line arguments and run the given functions."""
        # Debug Mode (views inputs)
        if self.args["--debug"]:
            print(self.doc)
            print("DEBUG:")
            print("sys.argv:")
            print(sys.argv)
            print("docopt:")
            pprint(self.args)
            print("")

        # Quiet Mode Toggle
        if self.is_quiet:
            sys.stdout = self._void

        # func Help
        if self.func and self.func.func_name in self.funcs.keys():
            # func Help
            if self.args["--docstring"]:
                print("\nDocstring for {}:".format(self.func.func_name))
                print(self.func.__doc__)
                exit()

            # func execution
            return self.func(*self.pos_args, **self.opt_args)
        return

    @property
    def func(self):
        """The function object called from the sys.argv."""
        if sys.argv[1] in ("-h", "--help", "--version", "--debug", "--docstring"):  # NOQA
            return None
        a = sys.argv[1].replace("-", "_")
        if a in self.funcs.keys():
            return self.funcs[a]
        #elif a in self.args.keys():
        #    return None
        raise FunctionCallError(
            "function '{}' not found".format(sys.argv[1]))


    @property
    def is_verbose(self):
        """Returns the boolean value of args["--verbose"]."""
        # TODO: expand usefulness or remove
        return self.args["--verbose"]

    @property
    def is_quiet(self):
        """Returns the boolean value of args["--quiet"]."""
        return self.args["--quiet"]

    def _list_funcs(self, module):
        """Generator of functions in current module."""
        for func_name, func in inspect.getmembers(sys.modules[module]):
            if inspect.isfunction(func) and not func_name.startswith("_"):
                if not inspect.ismodule(func):
                    if isinstance(self._all, bool):
                        yield (func_name, func)
                    elif isinstance(self._all, list):
                        if func.func_name in self._all:
                            yield (func_name, func)

    def get_pos_params(self, func):
        # Get argspec for each function
        spec = inspect.getargspec(func)

        # Get optional args
        try:
            # Match optional arg name with value
            optionals = zip(spec.args[-len(spec.defaults):], spec.defaults)
            # Replace '_' to '-' in arg names (but not values)
            optionals = [(o[0].replace("_", "-"), o[1]) for o in optionals]
        except TypeError:
            optionals = [[None, None]]

        # Make string of positional args (replace '_' to '-' in arg names)
        #  and ensure args with defaults are not included
        pos = ["<{}>".format(a.replace("_", "-")) for a in spec.args
               if a.replace("_", "-") not in [o[0] for o in optionals]]
        return pos

    @property
    def pos_args(self):
        if self.func:
            return [self.args[arg] for arg in self.get_pos_params(self.func)]
        return []

    def get_opt_params(self, func):
        # Get argspec for each function
        spec = inspect.getargspec(func)

        # Get optional args
        try:
            # Match optional arg name with value
            optionals = zip(spec.args[-len(spec.defaults):], spec.defaults)
            # Replace '_' to '-' in arg names (but not values)
            optionals = [(o[0].replace("_", "-"), o[1]) for o in optionals]
        except TypeError:
            optionals = [[None, None]]

        # Make string of optional args
        if optionals[0][0]:
            # Doesn't add to template if no args
            for opt in optionals:
                yield ("--{0}".format(opt[0]), opt[1])

    @property
    def opt_args(self):
        if self.func:

            return {
                # Key
                opt[0].replace("--", "").replace("-", "_"):
                    # Value if provided, default from argspec if not
                    (self.args[opt[0]] if self.args[opt[0]] else opt[1])
                for opt in self.get_opt_params(self.func)
                }
        return []

    def _func_usage(self):
        """Generator of usage patterns for available functions."""
        for func_name, func in self._list_funcs(self._module):
            # Usage pattern template
            t = "{name} {func_name}"

            # Get positional parameter names
            pos = " ".join(["{}".format(arg) for arg
                            in self.get_pos_params(func)])

            # Get optional parameters and values
            opt = " ".join(["{0}={1}".format(arg[0], arg[1]) for arg
                            in self.get_opt_params(func)])

            # Format template t
            if pos or opt:
                t += " ["
            if pos:
                t += "{pos}"
            if opt:
                t += " {opt}"
            if "[" in t:
                t += "]"

            # Close bracket and add [options] to end of template and format
            t += " [options]"
            yield t.format(
                name="tools.py",
                func_name=func.func_name.replace("_", "-"),
                pos=pos,
                opt=opt)

    def _make_usage(self):
        return "\n    ".join(self._func_usage())

    @property
    def funcs(self):
        """Dict of function names : objects found in the current module."""
        return dict(self._list_funcs(self._module))
