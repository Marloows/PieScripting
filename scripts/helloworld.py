"""
	Test Module to check if PYTHONPATH is working properly
"""

import os

import textwrap

print("\n\tHello World!\n")

print('\tCurrent PYTHONPATH:\n')

pypath = os.environ['PYTHONPATH'].split(';')

pypath = "\n".join(pypath)

pypath = textwrap.indent(pypath, 2*'\t')

print(pypath, end=2*"\n")
