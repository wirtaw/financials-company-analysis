#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

import unittest
import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))
sys.path.insert(0, PROJECT_DIR)
from src.app import Application
from src.app import main


class MyTestCase(unittest.TestCase):
    """Class documentation goes here."""

    def test_default_greeting_set(self):
        """Test documentation goes here."""
        input = "SDF"
        app = Application()
        app.set_message(input)
        self.assertEqual(app.message, input)
        main(sys.argv[1:])

    def test_wrong_markets_set(self):
        """Wrong markets"""
        app = Application()
        app.set_markets('')
        self.assertEqual(app.markets, ["Nasdaq", "Dow Jones & Company",
                                       "Standard & Poor's", "EURO STOXX 50",
                                       "OMX Vilnius", "MICEX"])
        main(sys.argv[1:])

    def test_empty_markets_set(self):
        """Empty markets"""
        app = Application()
        app.set_markets()
        self.assertEqual(app.markets, ["Nasdaq", "Dow Jones & Company",
                                       "Standard & Poor's", "EURO STOXX 50",
                                       "OMX Vilnius", "MICEX"])
        main(sys.argv[1:])

    def test_DWJ_markets_set(self):
        """Set one market"""
        app = Application()
        app.set_markets('Dow Jones & Company')
        self.assertEqual(app.markets, ['Dow Jones & Company'])
        main(sys.argv[1:])

    def test_list_markets_set(self):
        """Set list country"""
        input = 'Nasdaq, Dow Jones & Company, MICEX'
        app = Application()
        app.set_markets(input)
        self.assertEqual(app.markets, ['Nasdaq', 'Dow Jones & Company', 'MICEX'])
        main(sys.argv[1:])

    def test_wrong_symbols_set(self):
        """Wrong symbols"""
        app = Application()
        app.set_symbols('')
        self.assertEqual(app.symbols, [])
        main(sys.argv[1:])

    def test_empty_symbols_set(self):
        """Empty symbols"""
        app = Application()
        app.set_symbols()
        self.assertEqual(app.symbols, [])
        main(sys.argv[1:])

    def test_DWJ_symbols_set(self):
        """Set one symbols"""
        app = Application()
        app.set_symbols('NYSE:DDD')
        self.assertEqual(app.symbols, ['NYSE:DDD'])
        main(sys.argv[1:])

    def test_list_symbols_set(self):
        """Set list country"""
        input = 'NYSE:DDD, NYSE:FDX'
        app = Application()
        app.set_symbols(input)
        self.assertEqual(app.symbols, ['NYSE:DDD', 'NYSE:FDX'])
        main(sys.argv[1:])


if __name__ == '__main__':
    unittest.main()
