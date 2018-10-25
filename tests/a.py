

import inspect
import sys


tdoc = """
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


def _list_funcs(module):
    """Generator of functions in current module."""
    for func_name, func_obj in inspect.getmembers(sys.modules[module]):
        if inspect.isfunction(func_obj) and not func_name.startswith("_"):
            if not inspect.ismodule(func_obj):
                yield (func_name, func_obj)


def bp_model(db_in, file_out, name_flag="g_wally", flag=True):
    """Building Permit Model for UFDA Project.
    Args:
        db_in (str): File path to SQLite database
        file_out (str): File path to ...
    """
    print((db_in, file_out))
    print("Analyzing...")
    return


def get_pos_params(func):
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
    #if pos:
    #    pos = ("[" + pos + "]").replace("_", "-")
    return pos


def pos_args(func):
    return [d[arg] for arg in get_pos_params(func)]



def get_opt_params(func):
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


def opt_args(func):
    return {opt[0].replace("--", "").replace("-", "_"): d[opt[0]]
            for opt in get_opt_params(func)}


d = {
     "<db-in>": "in.db",
     "<file-out>": "out.txt",
     "--flag": True,
     "--name-flag": "amy_wally",
     "<other>": "otherval"}

#bp_model(*pos_args(bp_model), **opt_args(bp_model))


def func_usage():
    """Generator of usage patterns for available functions."""
    for func_name, func in _list_funcs(__name__):
        # Usage pattern template
        t = "{name} {func_name}"

        # Get positional parameter names
        pos = " ".join(["{}".format(arg) for arg in get_pos_params(func)])

        # Get optional parameters and values
        opt = " ".join(["{0}={1}".format(arg[0], arg[1]) for arg
                        in get_opt_params(func)])

        # Format template t
        if pos or opt:
            t += " ["
        if pos:
            t += "{pos}"
        if opt:
            t += " {opt}"
        if "[" in t:
            t += "]"

        # Add [options] to end of template and format
        t += " [options]"
        yield t.format(
            name="tools.py",
            func_name=func.func_name.replace("_", "-"),
            pos=pos,
            opt=opt)

print(tdoc.format(usage="\n    ".join(func_usage())))

