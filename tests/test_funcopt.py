# -*- coding: utf-8 -*-

import os
import sys
import unittest
from subprocess import Popen, PIPE
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import funcopt


expected_h = """tools.py -- My tools
Author: Garin Wally, Oct 2018

Usage:
    tools.py bp-model [<db-in> <file-out> --name-opt=A --flag=False] [options]

Options:
    -h, --help        Show this help message and exit
    -v, --verbose     Print status messages (WIP)
    -q, --quiet       Write all messages to the void
    --version         Show program's version number and exit
    --debug           Show the docopt dictionary of parameters passed
    --docstring       Shows the docstring for the given function and exit"""


expected_debug = """tools.py -- My tools
Author: Garin Wally, Oct 2018

Usage:
    tools.py bp-model [<db-in> <file-out> --name-opt=A --flag=False] [options]

Options:
    -h, --help        Show this help message and exit
    -v, --verbose     Print status messages (WIP)
    -q, --quiet       Write all messages to the void
    --version         Show program's version number and exit
    --debug           Show the docopt dictionary of parameters passed
    --docstring       Shows the docstring for the given function and exit

DEBUG:
sys.argv:
['tests/tools.py', 'bp-model', 'thing1.db', 'thing2.txt', '--flag=True', '--debug']
docopt:
{'--debug': True,
 '--docstring': False,
 '--flag': True,
 '--help': False,
 '--name-opt': None,
 '--quiet': False,
 '--verbose': False,
 '--version': False,
 '<db-in>': 'thing1.db',
 '<file-out>': 'thing2.txt',
 'bp-model': True}

('thing1.db', 'thing2.txt', 'A', True)
Analyzing..."""


class TestUtils(unittest.TestCase):
    def type_parser_test(self):
        self.assertEqual(funcopt.type_parser("A"), "A")
        self.assertEqual(funcopt.type_parser("1"), 1)
        self.assertEqual(funcopt.type_parser("1.0"), 1.0)
        self.assertEqual(funcopt.type_parser("True"), True)
        self.assertEqual(funcopt.type_parser("False"), False)
        self.assertEqual(funcopt.type_parser("None"), None)
        self.assertEqual(funcopt.type_parser(None), None)
        self.assertEqual(funcopt.type_parser(""), "")
    def type_parse_dict(self):
        d = {"number": "100", "float": "1.0", "str": "funcopt",
             "bool": "True", "None": "None", "same": False}
        expected = {"number": 100, "float": 1.0, "str": "funcopt",
                    "bool": True, "None": None, "same": False}
        for k, v in d:
            d[k] = funcopt.type_parser(v)
        self.assertDictEqual(d, expected)


class TestOptions(unittest.TestCase):
    def help_test(self):
        p = Popen(
            "python tests/tools.py -h",
            stdout=PIPE).communicate()[0]
        self.assertEqual(
            p.replace("\r", "").strip(),
            expected_h)

    def version_test(self):
        p = Popen(
            "python tests/tools.py --version",
            stdout=PIPE).communicate()[0]
        self.assertEqual(
            p.replace("\r", "").strip(),
            "0.0.1")
    '''
    def not_found_error_test(self):
        self.assertRaises(
            os.system("python tools.py __repr__ value"),
            funcopt.FunctionCallError)
        self.assertRaises(
            os.system("python tools.py doesnt-exist value"),
            funcopt.FunctionCallError)
    '''

    def bp_help_test(self):
        p = Popen(
            "python tests/tools.py bp-model --docstring",
            stdout=PIPE).communicate()[0]
        self.assertEqual(
            p.replace("\r", "").strip(),
            ("Docstring for bp_model:\nBuilding Permit Model.\n"
             "    Args:\n"
             "        db_in (str): File path to SQLite database\n"
             "        file_out (str): File path to ...\n"
             "        name_opt (str): A string\n"
             "        flag (bool): a flag (default False)")
            )

    def bp_test(self):
        p = Popen(
            "python tests/tools.py bp-model thing1.db thing2.txt --flag=False",
            stdout=PIPE).communicate()[0]
        self.assertEqual(
            p.replace("\r", "").strip(),
            ("('thing1.db', 'thing2.txt', 'A', False)\n"
             "Analyzing...")
            )

    def bp_test_kw(self):
        p = Popen(
            "python tests/tools.py bp-model thing1.db thing2.txt --flag=True",
            stdout=PIPE).communicate()[0]
        self.assertEqual(
            p.replace("\r", "").strip(),
            ("('thing1.db', 'thing2.txt', 'A', True)\n"
             "Analyzing...")
            )

    def bp_test_debug(self):
        p = Popen(
            "python tests/tools.py bp-model thing1.db thing2.txt --flag=True --debug",
            stdout=PIPE).communicate()[0]
        self.assertEqual(
            p.replace("\r", "").strip(),
            expected_debug
            )

    def quiet_bp_test(self):
        p = Popen("python tests/tools.py bp-model thing1 thing2 -q",
                  stdout=PIPE).communicate()[0]
        self.assertEqual(p, "")
