#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for data analyzing."""

import numpy as np
import statsmodels.api as sm
import re
import math


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
            number_to_validate = \
                number_to_validate.replace(",", ".")
            if re.match(r'^-?\d+(?:\.\d+)?$', '32.2') is not None:
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

        element_number = len(y_axis)
        sum_x_axis = np.sum(x_axis)
        sum_y_axis = np.sum(y_axis)
        sum_multiply_axis = np.sum(np.multiply(x_axis, y_axis))
        sum_power_x_axis = np.sum(np.power(x_axis, 2))
        sum_power_y_axis = np.sum(np.power(y_axis, 2))

        top_b_coef = (element_number * sum_multiply_axis - sum_x_axis * sum_y_axis)
        bottom_b_coef = (element_number * sum_power_x_axis - np.power(sum_x_axis, 2))
        b_coef = top_b_coef / bottom_b_coef
        top_a_coef = (sum_y_axis - b_coef * sum_x_axis)
        a_coef = top_a_coef / element_number

        x_middle = sum_x_axis / element_number
        y_middle = sum_y_axis / element_number
        xy_middle = sum_multiply_axis / element_number

        s_power_x = sum_power_x_axis / element_number - math.pow(x_middle, 2)
        s_power_y = sum_power_y_axis / element_number - math.pow(y_middle, 2)

        s_sqrt_x = math.sqrt(s_power_x)
        s_sqrt_y = math.sqrt(s_power_y)

        rsquared_top = xy_middle - x_middle * y_middle
        rsquared_bottom = s_sqrt_x * s_sqrt_y
        rsquared = rsquared_top / rsquared_bottom

        regression_coef = rsquared * s_sqrt_y / s_sqrt_x
        regression_adj = (rsquared * ((-1) * x_middle / s_sqrt_x)) * s_sqrt_y + y_middle

        return {'rsquared': rsquared,
                'regression_coef': regression_coef,
                'regression_adj': regression_adj,
                'params': {"a_coef": a_coef, "b_coef": b_coef}}

    def regression_stat_model(self, values):
        """Regression with regression_stat_model modeling"""
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

    @staticmethod
    def get_points(title, values):
        """Get points"""
        scores = {}
        coef = {}
        if title == 'market_cap':
            max_market_cap = 0
            max_market_cap_title = ''
            for item in values.items():
                point = 0
                if item[1]['regression_coef'] > 0:
                    point += 0.5
                scores[item[0]] = point
                if item[1]['regression_coef'] > max_market_cap:
                    max_market_cap = item[1]['regression_coef']
                    max_market_cap_title = item[0]
                coef[item[0]] = item[1]['regression_coef']
            scores[max_market_cap_title] = scores[max_market_cap_title] + 0.5

        if title == 'debt':
            min_market_cap = 0
            min_market_cap_title = ''
            for item in values.items():
                point = 0
                if item[1]['regression_coef'] < 0:
                    point += 0.5
                scores[item[0]] = point
                if item[1]['regression_coef'] < min_market_cap:
                    min_market_cap = item[1]['regression_coef']
                    min_market_cap_title = item[0]
                coef[item[0]] = item[1]['regression_coef']
            scores[min_market_cap_title] = scores[min_market_cap_title] + 0.5

        if title == 'assets':
            max_market_cap = 0
            max_market_cap_title = ''
            for item in values.items():
                point = 0
                if item[1]['regression_coef'] > 0:
                    point += 0.5
                scores[item[0]] = point
                if item[1]['regression_coef'] > max_market_cap:
                    max_market_cap = item[1]['regression_coef']
                    max_market_cap_title = item[0]
                coef[item[0]] = item[1]['regression_coef']
            scores[max_market_cap_title] = scores[max_market_cap_title] + 0.5

        if title == 'revenue':
            max_market_cap = 0
            max_market_cap_title = ''
            for item in values.items():
                point = 0
                if item[1]['regression_coef'] > 0:
                    point += 0.5
                scores[item[0]] = point
                if item[1]['regression_coef'] > max_market_cap:
                    max_market_cap = item[1]['regression_coef']
                    max_market_cap_title = item[0]
                coef[item[0]] = item[1]['regression_coef']
            scores[max_market_cap_title] = scores[max_market_cap_title] + 0.5

        if title == 'net_income':
            max_market_cap = 0
            max_market_cap_title = ''
            for item in values.items():
                point = 0
                if item[1]['regression_coef'] > 0:
                    point += 0.5
                scores[item[0]] = point
                if item[1]['regression_coef'] > max_market_cap:
                    max_market_cap = item[1]['regression_coef']
                    max_market_cap_title = item[0]
                coef[item[0]] = item[1]['regression_coef']
            scores[max_market_cap_title] = scores[max_market_cap_title] + 0.5
        print(coef)
        print(scores)

        return scores

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
                             'debt_ebitda_regression': {},
                             'market_cap_regression_statsmodels': {},
                             'debt_regression_statsmodels': {},
                             'assets_regression_statsmodels': {},
                             'revenue_regression_statsmodels': {},
                             'net_income_regression_statsmodels': {},
                             'p_e_regression_statsmodels': {},
                             'p_s_regression_statsmodels': {},
                             'p_bv_regression_statsmodels': {},
                             'ev_ebitda_regression_statsmodels': {},
                             'debt_ebitda_regression_statsmodels': {}
                             }
        self.points = {'market_cap': {},
                             'debt': {},
                             'assets': {},
                             'revenue': {},
                             'net_income': {},
                             'p_e': {},
                             'p_s': {},
                             'p_bv': {},
                             'ev_ebitda': {},
                             'debt_ebitda': {}
                             }
        criteria = ['market_cap', 'debt', 'assets', 'revenue',
                    'net_income', 'p_e', 'p_s', 'p_bv', 'ev_ebitda',
                    'debt_ebitda']
        if self.data:
            for symbol, values in self.data.items():
                for key, data in values['data'].items():
                    if key in criteria:
                        stat_model_title = f"{key}_regression_statsmodels"
                        self.calculations[stat_model_title][symbol] = self.regression_stat_model(data)
                        title = f"{key}_regression"
                        self.calculations[title][symbol] = self.regression(data)
            for item in self.calculations.items():
                title = item[0].replace("_regression", "")
                self.points[title] = self.get_points(title, item[1])
            total = {}
            for symbol, values in self.data.items():
                total[symbol] = 0
                # for key, data in self.points.items():
                    # for sym, point in data.items():
                        # total[sym] = total[sym] + point
            # self.points['total'] = total
            print(self.points)