#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for data analyzing."""

import numpy as np
import statsmodels.api as sm


class Analyze:
    """Analyze module"""

    def __init__(self, data):
        self.data = data
        self.points = {}
        self.calculations = {}

    @staticmethod
    def parse_float(number_to_validate):
        """Parse float number"""
        result = 0.0
        if number_to_validate \
                and isinstance(number_to_validate, str):
            number_to_validate = \
                number_to_validate.replace(" ", "")
            if number_to_validate.isnumeric():
                result = float(number_to_validate)
        else:
            if number_to_validate \
                    and isinstance(number_to_validate, float):
                result = number_to_validate
        return result

    def regression(self, values):
        """Regression modeling"""
        x_axis = []
        y_axis = []
        counter = 0
        for item in values:
            y_axis.append(self.parse_float(item))
            x_axis.append(counter)
            counter = counter + 1
        x_axis, y_axis = np.array(x_axis), np.array(y_axis)
        x_axis = sm.add_constant(x_axis)
        model = sm.OLS(y_axis, x_axis)
        results = model.fit()
        return {'rsquared': results.rsquared,
                'rsquared_adj': results.rsquared_adj,
                'params': results.params}

    def calculate(self):
        """Make all calculations"""
        self.calculations = {'market_cap_regression': {},
                             'debt_regression': {},
                             'assets_regression': {},
                             'revenue_regression': {},
                             'net_income_regression': {},
                             'p_e_regression': {},
                             'p_s_regression': {},
                             'p_bv_regression': {},
                             'ev_ebitda_regression': {},
                             'debt_ebitda_regression': {}}
        criteria = ['market_cap', 'debt', 'assets', 'revenue',
                    'net_income', 'p_e', 'p_s', 'p_bv', 'ev_ebitda',
                    'debt_ebitda']
        if self.data:
            for symbol, values in self.data.items():
                for key, data in values.items():
                    if key in criteria:
                        self.calculations[f"{key}_regression"][symbol] = \
                            self.regression(data)
