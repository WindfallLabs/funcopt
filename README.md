# funcopt

Simple, self-documenting commandline interfaces with encapsulated execution logic powered by docopt.  

## Sales Pitch
funcopt handles the execution logic that [docopt](http://docopt.org/) doesn't.  
(e.g. `-q` option sends outputs to `os.devnull`, handles function calls, argument positioning, etc.)  
funcopt is simpler and less verbose than argparse or [click](https://click.palletsprojects.com/en/7.x/).  
(e.g. No decorators or groups; not complicated!)  
funcopt provides function-level help similar to [defopt](https://defopt.readthedocs.io/en/stable/index.html),
but provides access to all public module-level functions by default.  
(e.g. function docstring access via `--docstring` flag)

## Details
funcopt uses `inspect` to create [docopt](http://docopt.org/) docstrings for your
script that are then used create simple commandline interfaces. With docopt, 
he user must write the documentation that exactly matches docopt's requirements
and then the execution logic to match. With funcopt, users write their functions.
That's it.  
All `sys.argv` parameters are passed as strings to the `type_parser` which
converts the value to the appropriate Python types: Integer, Float, Boolean, and None.  
All public functions (those without leading underscores) are accessible by default, and
underscores become dashes (see Example; bp_model -> bp-model).  

# License:
MIT (see LICENSE.txt)

# Contributing:
All contributions should pass all existing tests.  
New features/content must come with and pass the appropriate tests.  
I'm not worried about coverage so long as output strings are as they should be.  

# Usage:
To create a commandline interface for your functions:  
* Import or define your functions  
* Do the `if __name__ == '__main__':` thing  
* Pass the CLI object your filename, current module, version and run!  

# Example:
## tools.py

    # -*- coding: utf-8 -*-
    """tools.py -- My tools
    Author: Garin Wally, Oct 2018
    """

    from os.path import dirname, join
    # NOTE: dirname and join would be public if not for __all__
    import sys
    # NOTE: Modules are ignored

    from funcopt import CLI
    # NOTE: Classes are ignored

    # Import a function from a module as a public function
    from ufda.bps import bp_model

    # Manually limit functions to provide API for
    # Default (True) accesses all functions (i.e. would include dirname and join)
    __all__ = ["bp_model"]
    __version__ = "0.0.1"


    if __name__ == "__main__":
        # Provide the current script name, module name, docstring (optional),
        #  version (optional) and list of functions to include (optional).
        CLI(__file__, __name__, __doc__, __version__, __all__).run()

## Commandline Interface:

    $ python tools.py -h
    tools.py -- My tools
    Author: Garin Wally, Oct 2018

    Usage:
        tools.py bp-model [<db-in> <file-out> --name-flag=garin_wally --flag=False] [options]

    Options:
        -h, --help        Show this help message and exit
        -v, --verbose     Print status messages (WIP)
        -q, --quiet       Write all messages to the void
        --version         Show program's version number and exit
        --debug           Show the docopt dictionary of parameters passed
        --docstring       Shows the docstring for the given function and exit

    $ python tools.py bp-model thing1.db thing2.txt
    ('thing1.db', 'thing2.txt', 'garin_wally', False)
    Analyzing...
    
    $ python tools.py bp-model thing1.db thing2.txt -q
    
    
    $ python tools.py bp-model --docstring
    
    Docstring for bp_model:
    Building Permit Model for UFDA Project.
        Args:
            db_in (str): File path to SQLite database
            file_out (str): File path to ...

