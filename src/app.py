#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

from __future__ import print_function

__author__ = "Vladimir Poplavskij"
__copyright__ = "Copyright 2020, Vladimir Poplavskij"
__credits__ = ["C D", "A B"]
__license__ = "Apache 2.0"
__version__ = "1.0.1"
__maintainer__ = "Vladimir Poplavskij"
__email__ = "float45@gmail.com"
__status__ = "Development"

import os
import sys
import argparse
from logzero import logger

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)

# pylint: disable=wrong-import-position

import scrapping
import analysis

# pylint: enable=wrong-import-position


def log(function):
    """Handy logging decorator."""

    def inner(*args, **kwargs):
        """Inter method."""
        logger.debug(function)
        function(*args, **kwargs)

    return inner


class Application:
    """Main application"""

    def __init__(self):
        self.message = 'Welcome to the Investment analyse app!'
        self.markets = []
        self.symbols = []

    def set_message(self, message):
        """Welcome message."""
        self.message = message

    @log
    def print_message(self):
        """Function description."""
        print(self.message)

    def set_markets(self, markets=None):
        """Set list of the markets divided by comma.
        Default (["Nasdaq", "Dow Jones & Company", "Standard & Poor's",
        "EURO STOXX 50", "OMX Vilnius", "MICEX"])"""
        if markets and isinstance(markets, str):
            if markets.find(',') != -1:
                market_list = markets.split(',')
                for item in market_list:
                    self.markets.append(item.strip())
            else:
                self.markets.append(markets)
        else:
            self.markets = ["Nasdaq", "Dow Jones & Company",
                            "Standard & Poor's", "EURO STOXX 50",
                            "OMX Vilnius", "MICEX"]

    def set_symbols(self, symbols=None):
        """Set list of the stock symbols divided by comma.
        Default ([])"""
        if symbols and isinstance(symbols, str):
            if symbols.find(',') != -1:
                symbols_list = symbols.split(',')
                for item in symbols_list:
                    self.symbols.append(item.strip())
            else:
                self.symbols.append(symbols)
        else:
            self.symbols = []


def main(args):
    """ Main entry point of the app """
    app = Application()
    if args and args.markets:
        app.set_markets(args.markets)
    if args and args.symbols:
        app.set_symbols(args.symbols)
    app.print_message()

    if args and app.markets:
        file_path = './../'

        scrapper = scrapping.Scrapper(app.markets)
        scrapper.get_symbols(f"{file_path}data/stocks.json")

        if len(app.symbols) > 0:
            companies = {}
            for symbol in app.symbols:
                file_name = f"{file_path}data/{symbol}_financials.json"
                companies[symbol] =\
                    scrapper.get_fundamental_analysis(symbol,
                                                      file_name)
            print(companies)
            analysis_companies = analysis.Analyze(companies, app.symbols)
            result = analysis_companies.calculate()
            print(result)

    logger.info(args)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()

    # Optional argument flag which defaults to False
    PARSER.add_argument("-f", "--flag", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    PARSER.add_argument("-n", "--name", action="store", dest="name")
    PARSER.add_argument("-m", "--markets", action="store", dest="markets")
    PARSER.add_argument("-s", "--symbols", action="store", dest="symbols")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    PARSER.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    PARSER.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    MYARGS = PARSER.parse_args()
    main(MYARGS)
