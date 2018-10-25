# -*- coding: utf-8 -*-
"""tools.py -- My tools
Author: Garin Wally, Oct 2018
"""

from os.path import dirname, join
# NOTE: dirname and join would be public if not for __all__
import sys
# NOTE: Modules are ignored
sys.path.insert(0, join(dirname(__file__), ".."))

# NOTE: Classes are ignored
from funcopt import CLI

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
