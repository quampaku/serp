#!/usr/bin/env python
"""Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import argparse
import os
import subprocess
from typing import List
import unittest

SOURCE_CODE = ['services', 'controllers', 'models', 'system']
TEST_CODE = ['tests']
ALL_CODE = SOURCE_CODE + TEST_CODE


def arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Run linter, static type checker, tests'
    )

    subparsers = parser.add_subparsers(dest='func', help='sub-commands')

    typechecker_cmd_parser = subparsers.add_parser('typecheck')
    typechecker_cmd_parser.add_argument(
        '-c', '--checker',
        default='mypy',
        help='specify static type checker, default: %(default)s'
    )
    typechecker_cmd_parser.add_argument(
        'paths',
        nargs='*',
        default=ALL_CODE,
        help='directories and files to chek'
    )

    lint_cmd_parser = subparsers.add_parser('lint')
    lint_cmd_parser.add_argument(
        '-l', '--linter',
        default='flake8',
        help='specitfy linter, default: %(default)s'
    )
    lint_cmd_parser.add_argument(
        'paths',
        nargs='*',
        default=ALL_CODE,
        help='directories and files to check'
    )

    test_cmd_parser = subparsers.add_parser('test')
    test_cmd_parser.add_argument(
        '--suite',
        choices=['all', 'unit', 'integration'],
        default='all',
        type=str,
        help='test suite to run, default: %(default)s'
    )
    test_cmd_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='turn on verbose output'
    )

    return parser


def run_checker(checker: str, paths: List[str]) -> None:
    if len(paths) != 0:
        subprocess.call([checker] + paths)


def run_tests(suite_name: str, verbose: bool) -> None:
    test_suites = {
        'all': 'tests',
        'unit': 'tests/unit',
        'integration': 'tests/integration'
    }   
    suite = test_suites.get(suite_name, 'tests')

    verbosity = 2 if verbose else 1

    test_suite = unittest.TestLoader().discover(suite, pattern='*_test.py')
    unittest.TextTestRunner(verbosity=verbosity).run(test_suite)


def main(args=None) -> None:
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    parser = arg_parser()
    args = parser.parse_args(args)

    actions = {
        'typecheck': lambda: run_checker(args.checker, args.paths),
        'lint': lambda: run_checker(args.linter, args.paths),
        'test': lambda: run_tests(args.suite, args.verbose)
    }

    actions.get(args.func, parser.print_help)()


if __name__ == "__main__":
    main()
