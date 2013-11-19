#!/usr/bin/python
# -*- coding: utf-8 -*-
"""fry.tests.runtime module.

Author: Jan Milík <milikjan@fit.cvut.cz>
"""


import unittest
import cStringIO as StringIO

from pymlab import config


class ConfigTestCase(unittest.TestCase):
	def test_load_python_00(self):
		cfg = config.Config()
		cfg.load_python("""
port = 5

bus = [
]
		""")

	def test_load_python_01(self):
		cfg = config.Config()
		cfg.load_python("""
port = 5

bus = [
	{ "type": "mag01", "address": 0x68 }
]
		""")

	def test_load_python_02(self):
		cfg = config.Config()
		cfg.load_python("""
port = 5

bus = [
	{ "type": "i2chub", "address": 0x70, "children": [ {"type": "mag01", "channel": 0}, {"type": "mag01", "channel": 1}, ] },
	{ "type": "mag01", "address": 0x68 }
]
		""")


def main():
    unittest.main()


if __name__ == "__main__":
    main()
