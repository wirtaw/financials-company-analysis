#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for data scrapping."""

import os.path
from os import path
import json
import re
from requests import get
from bs4 import BeautifulSoup


class Scrapper:
    """Scrapper module"""

    def __init__(self, markets, filename):
        self.endpoints = {
            "https://smart-lab.ru/": [
                'q/usa/',
                'q/shares/'
            ]
        }
        self.filename = filename
        self.markets = markets
        self.list_symbols = []

    @staticmethod
    def json_validator(data):
        """Validate json"""
        try:
            json.loads(data)
            return True
        except ValueError as error:
            print("invalid json: %s" % error)
            return False

    @staticmethod
    def get_request(query, url):
        """Make request to page"""
        moz = 'Mozilla/5.0 (Windows NT 6.1)'
        apple = 'AppleWebKit/537.36 (KHTML, like Gecko)'
        chrome = 'Chrome/41.0.2228.0'
        safari = 'Safari/537.36'
        application_html = 'application/xhtml+xml'
        application_xml = 'application/xml;q=0.9'
        image = 'application/xml;q=0.9'
        headers = {
            'Accept': f"text/html,{application_html},"
                      f"{application_xml},{image}",
            'Accept-Encoding': "gzip, deflate, br",
            'User-Agent': f"{moz} {apple} {chrome} {safari}",
            'Referer': f"{url}{query}",
        }

        res = get(f"{url}{query}", headers=headers)
        data = ''
        if res.status_code == 200:
            data = res.text
        return data

    def read_filename(self):
        """Get file with symbols"""
        res = None
        if path.isfile(self.filename):
            with open(self.filename) as file_stream:
                for json_obj in file_stream:
                    res = json.loads(json_obj)

        return res

    @staticmethod
    def map_row(columns):
        """Mapping table rows"""
        res = {
            "fundamental_analysis": False
        }

        number = 1
        for column in columns:
            forum_link = \
                column.find("a", href=re.compile('forum'))
            portfolio_action = \
                column.find("span", class_=re.compile('portfolio_action'))
            fundamental_analysis = \
                column.find("a", class_=re.compile('charticon2'))

            if forum_link:
                res["name"] = forum_link.text
                number = number + 1

            if portfolio_action:
                res["symbol"] = portfolio_action.get('symbol')
                number = number + 1

            if fundamental_analysis:
                res["fundamental_analysis"] = True

        if number > 2:
            return res
        else:
            return None

    @staticmethod
    def map_row_financial(columns):
        """Mapping table financial rows"""
        res = []

        number = 1
        for column in columns:
            if column.text and column.get('class') is None:
                res.append(column.text.strip())
                number = number + 1
        if number > 2:
            return res
        else:
            return None

    def parse_table(self, table):
        """Parse table"""
        res = []

        rows = table[0].find_all('tr')
        if len(rows) > 1:
            for row in rows:
                columns = row.find_all('td')
                if columns and len(columns) > 1:
                    item = self.map_row(columns)
                    if item is not None:
                        res.append(item)

        return res

    def parse_body(self, html):
        """Parse page body"""
        res = []

        soup = BeautifulSoup(html, features="html.parser")
        trades_table = soup.find_all(id='usa_shares')
        trades_table_class = soup\
            .find_all("table", class_=re.compile('trades'))

        if trades_table:
            res = self.parse_table(trades_table)
        else:
            if trades_table_class:
                res = self.parse_table(trades_table_class)

        return res

    def parse_table_by_criteria(self, table):
        """Parse financial table"""
        res = {}
        criteria = ['market_cap', 'debt', 'assets', 'revenue', 'net_income']

        rows = table[0].find_all('tr')
        if len(rows) > 1:
            for row in rows:
                field = row.get('field')
                class_name = row.get('class')
                columns = row.find_all('td')
                if field in criteria \
                        and columns \
                        and len(columns) > 1\
                        or class_name == 'header_row':
                    item = self.map_row_financial(columns)
                    if item is not None:
                        res[field] = item

        return res

    def parse_body_financial(self, html):
        """Parse page financial body"""
        res = []

        soup = BeautifulSoup(html, features="html.parser")
        financial_table = soup\
            .find_all("table", class_=re.compile('financials'))

        if financial_table:
            res = self.parse_table_by_criteria(financial_table)

        return res

    def get_symbols(self):
        """Get stock symbols scrapping process"""
        bulk = self.read_filename()
        if bulk is None:
            data_to_save = {'data': []}
            for url, values in self.endpoints.items():
                for query in values:
                    response_body = self.get_request(query, url)
                    stock_list = []
                    if response_body != '':
                        stock_list = self.parse_body(response_body)
                    data_to_save['data'] = data_to_save['data'] + stock_list
            self.list_symbols = data_to_save
            if self.json_validator(json.dumps(data_to_save)):
                data_file = open(self.filename, "w")
                data_file.write(json.dumps(data_to_save))
                data_file.close()
        else:
            self.list_symbols = bulk

    def get_fundamental_analysis(self, symbol):
        if self.list_symbols and symbol:
            query = ''
            print(f"symbol {symbol}")
            for item in self.list_symbols['data']:
                if item['symbol'] and item['symbol'] == symbol \
                        and item['fundamental_analysis']:
                    print(item)
                    query_symbol = f"{item['symbol']}"
                    if item['symbol'].find('.') != -1:
                        symbols_list = item['symbol'].split('.')
                        query_symbol = symbols_list[1]

                    query = query + f"/q/{query_symbol}/f/y/"
            if query:
                for url in self.endpoints.items():
                    response_body = self.get_request(query, url[0])
                    if response_body != '':
                        financials_info = \
                            self.parse_body_financial(response_body)
                        print(response_body)
