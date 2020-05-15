#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for data analyzing."""

import re
import math
import numpy as np
import statsmodels.api as sm


class Analyze:
    """Analyze module"""

    def __init__(self, data, symbols):
        self.data = data
        self.points = {}
        self.calculations = {}
        self.symbols = symbols

    @staticmethod
    def clear_points(points):
        """Clear points"""
        max_value_title = ''
        max_value = 0
        result = {}
        for symbol_in_params, point in points.items():
            if point > max_value:
                max_value = point
                max_value_title = symbol_in_params
        for symbol_in_params, point in points.items():
            if symbol_in_params != max_value_title and max_value != point:
                result[symbol_in_params] = 0
            else:
                result[symbol_in_params] = 1
        return result

    @staticmethod
    def merge_two_dicts(first_dict, second_dict):
        """Merge dictionaries"""
        result = first_dict.copy()
        result.update(second_dict)
        return result

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
                'params': {"a_coef": a_coef, "b_coef": b_coef},
                'point': 0}

    def limitations(self, key, values):
        """Limitations modeling"""
        result = {}
        result = self.merge_two_dicts(result, self.regression(values))
        if key == 'p_e':
            point = 0
            parts = 1 / len(values)
            for item in values:
                value = self.parse_float(item)
                if value < 8:
                    point += parts
            if result['regression_coef'] > 0:
                point += 0.5
            result[key] = {'points': point}
        if key == 'p_bv':
            point = 0
            parts = 1 / len(values)
            for item in values:
                value = self.parse_float(item)
                if value < 1:
                    point += parts
            if result['regression_coef'] > 0:
                point += 0.5
            result[key] = {'points': point}
        if key == 'p_s':
            point = 0
            parts = 1 / (2 * len(values))
            for item in values:
                value = self.parse_float(item)
                if 2 > value > 1:
                    point += parts
                if value < 1:
                    point += 2 * parts
            if result['regression_coef'] > 0:
                point += 0.5
            result[key] = {'points': point}
        if key == 'ev_ebitda':
            point = 0
            parts = 1 / (2 * len(values))
            for item in values:
                value = self.parse_float(item)
                if 10 > value > 6:
                    point += parts
                if value <= 6:
                    point += 2 * parts
            if result['regression_coef'] > 0:
                point += 0.5
            result[key] = {'points': point}
        if key == 'debt_ebitda':
            point = 0
            parts = 1 / (2 * len(values))
            for item in values:
                value = self.parse_float(item)
                if 6 > value > 3:
                    point += parts
                if value <= 3:
                    point += 2 * parts
            if result['regression_coef'] > 0:
                point += 0.5
            result[key] = {'points': point}

        return result

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

    def liabilities_assets(self, values):
        """Liabilities/Assets"""
        result = []
        counter = 0
        point = 0
        sum_l_a = 0
        parts = 1 / (2 * len(values['market_cap']))
        for item in values['market_cap']:
            debt = self.parse_float(values['debt'][counter])
            precents = debt / self.parse_float(item) * 100
            sum_l_a += precents
            if precents < 50:
                point += 2 * parts
            if 60 >= precents > 50:
                point += parts / 2
            if 70 >= precents > 60:
                point += parts / 3
            if 80 >= precents > 70:
                point += parts / 4
            if 90 >= precents > 80:
                point += parts / 5
            if precents > 90:
                point += parts / 6
            result.append(precents)
            counter = counter + 1
        avg = sum_l_a / counter
        if avg < 50:
            point += 2 * parts
        if 60 >= avg > 50:
            point += parts / 2
        if 70 >= avg > 60:
            point += parts / 3
        if 80 >= avg > 70:
            point += parts / 4
        if 90 >= avg > 80:
            point += parts / 5
        if avg > 90:
            point += parts / 6
        return {'result': result, 'points': point}

    def return_on_sales(self, values):
        """ROS (Return on Sales)"""
        result = []
        counter = 0
        point = 0
        sum_ros = 0
        for item in values['revenue']:
            debt = self.parse_float(values['net_income'][counter])
            precents = debt / self.parse_float(item) * 100
            sum_ros += precents
            if precents > 81:
                point += 0.5
            if 80 >= precents > 61:
                point += 0.25
            if 60 >= precents > 41:
                point += 0.125
            if 40 >= precents > 21:
                point += 0.075
            if 20 >= precents > 0:
                point += 0.0375
            result.append(precents)
            counter = counter + 1
        avg = sum_ros / len(values['revenue'])
        if avg > 81:
            point += 0.5
        if 80 >= avg > 61:
            point += 0.25
        if 60 >= avg > 41:
            point += 0.125
        if 40 >= avg > 21:
            point += 0.075
        if 20 >= avg > 0:
            point += 0.0375
        return {'result': result, 'points': point}

    def return_on_equity(self, values):
        """ROS (Return on Equites)"""
        result = []
        counter = 0
        point = 0
        sum_ros = 0
        for item in values['roe']:
            val = item.replace("%", "")
            if val != '':
                precents = self.parse_float(val)
                sum_ros += precents
                if precents > 81:
                    point += 0.5
                if 80 >= precents > 61:
                    point += 0.25
                if 60 >= precents > 41:
                    point += 0.125
                if 40 >= precents > 21:
                    point += 0.075
                if 20 >= precents > 0:
                    point += 0.0375
                result.append(precents)
                counter = counter + 1
        avg = sum_ros / counter
        if avg > 81:
            point += 0.5
        if 80 >= avg > 61:
            point += 0.25
        if 60 >= avg > 41:
            point += 0.125
        if 40 >= avg > 21:
            point += 0.075
        if 20 >= avg > 0:
            point += 0.0375
        return {'result': result, 'points': point}

    def return_on_assets(self, values):
        """ROS (Return on Assets)"""
        result = []
        counter = 0
        point = 0
        sum_roa = 0
        for item in values['roa']:
            val = item.replace("%", "")
            if val != '':
                precents = self.parse_float(val)
                sum_roa += precents
                if precents > 81:
                    point += 0.5
                if 80 >= precents > 61:
                    point += 0.25
                if 60 >= precents > 41:
                    point += 0.125
                if 40 >= precents > 21:
                    point += 0.075
                if 20 >= precents > 0:
                    point += 0.0375
                result.append(precents)
                counter = counter + 1
        avg = sum_roa / counter
        if avg > 81:
            point += 0.5
        if 80 >= avg > 61:
            point += 0.25
        if 60 >= avg > 41:
            point += 0.125
        if 40 >= avg > 21:
            point += 0.075
        if 20 >= avg > 0:
            point += 0.0375
        return {'result': result, 'points': point}

    def return_ev_ebitda(self, values):
        """Calucalte retrun ev_ebitda"""
        x_axis = []
        y_axis = []
        counter = 0
        for item in values:
            y_axis.append(self.parse_float(item))
            x_axis.append(counter)
            counter = counter + 1
        x_axis, y_axis = np.array(x_axis), np.array(y_axis)

    @staticmethod
    def get_points(title, values):
        """Get points"""
        scores = {}
        coef = {}
        if title == 'market_cap':
            max_market_cap = 0
            max_market_cap_title = ''
            point = 0
            for item in values.items():

                if item[1]['regression_coef'] > 0:
                    point += 0.5
                scores[item[0]] = point
                if item[1]['regression_coef'] > max_market_cap:
                    max_market_cap = item[1]['regression_coef']
                    max_market_cap_title = item[0]
                coef[item[0]] = item[1]['regression_coef']
            scores[max_market_cap_title] = scores[max_market_cap_title] + 0.5

        if title == 'debt':
            min_debt = 0
            min_debt_title = ''
            point = 0
            for item in values.items():

                if item[1]['regression_coef'] < 0:
                    point += 0.5
                scores[item[0]] = point
                if item[1]['regression_coef'] < min_debt:
                    min_debt = item[1]['regression_coef']
                    min_debt_title = item[0]
                coef[item[0]] = item[1]['regression_coef']
            scores[min_debt_title] = scores[min_debt_title] + 0.5

        if title == 'assets':
            max_assets = 0
            max_assets_title = ''
            point = 0
            for item in values.items():

                if item[1]['regression_coef'] > 0:
                    point += 0.5
                scores[item[0]] = point
                if item[1]['regression_coef'] > max_assets:
                    max_assets = item[1]['regression_coef']
                    max_assets_title = item[0]
                coef[item[0]] = item[1]['regression_coef']
            scores[max_assets_title] = scores[max_assets_title] + 0.5

        if title == 'revenue':
            max_revenue = 0
            max_revenue_title = ''
            point = 0
            for item in values.items():

                if item[1]['regression_coef'] > 0:
                    point += 0.5
                scores[item[0]] = point
                if item[1]['regression_coef'] > max_revenue:
                    max_revenue = item[1]['regression_coef']
                    max_revenue_title = item[0]
                coef[item[0]] = item[1]['regression_coef']
            scores[max_revenue_title] = scores[max_revenue_title] + 0.5

        if title == 'net_income':
            max_net_income = 0
            max_net_income_title = ''
            point = 0
            for item in values.items():

                if item[1]['regression_coef'] > 0:
                    point += 0.5
                scores[item[0]] = point
                if item[1]['regression_coef'] > max_net_income:
                    max_net_income = item[1]['regression_coef']
                    max_net_income_title = item[0]
                coef[item[0]] = item[1]['regression_coef']
            if max_net_income_title != '':
                scores[max_net_income_title] = scores[max_net_income_title] + 0.5

        if title == 'l_a':
            for item in values.items():
                point = item[1]['points']
                scores[item[0]] = point

        if title == 'p_e':
            for item in values.items():
                point = item[1][title]['points']
                if item[1]['regression_coef'] > 0:
                    point += 0.5
                scores[item[0]] = point

        if title == 'p_s':
            for item in values.items():
                point = item[1][title]['points']
                if item[1]['regression_coef'] > 0:
                    point += 0.5
                scores[item[0]] = point

        if title == 'p_bv':
            for item in values.items():
                point = item[1][title]['points']
                if item[1]['regression_coef'] > 0:
                    point += 0.5
                scores[item[0]] = point

        if title == 'ros':
            for item in values.items():
                point = item[1]['points']
                scores[item[0]] = point

        if title == 'roe':
            for item in values.items():
                point = item[1]['points']
                scores[item[0]] = point

        if title == 'roa':
            for item in values.items():
                point = item[1]['points']
                scores[item[0]] = point

        if title == 'ev_ebitda':
            for item in values.items():
                point = item[1][title]['points']
                scores[item[0]] = point

        if title == 'debt_ebitda':
            for item in values.items():
                point = item[1][title]['points']
                scores[item[0]] = point

        return scores

    def calculate(self):
        """Make all calculations"""
        self.calculations = {'market_cap_regression': {},
                             'debt_regression': {},
                             'assets_regression': {},
                             'revenue_regression': {},
                             'net_income_regression': {},
                             'p_e_limitations': {},
                             'p_s_limitations': {},
                             'p_bv_limitations': {},
                             'ev_ebitda_limitations': {},
                             'debt_ebitda_limitations': {},
                             'l_a': {},
                             'ros': {},
                             'roe': {},
                             'roa': {},
                             'market_cap_regression_statsmodels': {},
                             'debt_regression_statsmodels': {},
                             'assets_regression_statsmodels': {},
                             'revenue_regression_statsmodels': {},
                             'net_income_regression_statsmodels': {}}
        self.points = {'market_cap': {},
                       'debt': {},
                       'assets': {},
                       'revenue': {},
                       'net_income': {},
                       'p_e': {},
                       'p_s': {},
                       'p_bv': {},
                       'ev_ebitda': {},
                       'debt_ebitda': {}}
        criteria_regression = ['market_cap', 'debt', 'assets', 'revenue', 'net_income']
        criteria = ['p_e', 'p_s', 'p_bv',
                    'ev_ebitda', 'debt_ebitda']
        if self.data:
            for symbol, values in self.data.items():
                for key, data in values['data'].items():
                    if key in criteria_regression:
                        stat_model_title = f"{key}_regression_statsmodels"
                        self.calculations[stat_model_title][symbol] = \
                            self.regression_stat_model(data)
                        title = f"{key}_regression"
                        self.calculations[title][symbol] = self.regression(data)
                    if key in criteria:
                        title = f"{key}_limitations"
                        self.calculations[title][symbol] = self.limitations(key, data)
                self.calculations['l_a'][symbol] = self.liabilities_assets(values['data'])
                self.calculations['ros'][symbol] = self.return_on_sales(values['data'])
                self.calculations['roe'][symbol] = self.return_on_equity(values['data'])
                self.calculations['roa'][symbol] = self.return_on_assets(values['data'])

            for item in self.calculations.items():
                title = item[0].replace("_regression", "").replace("_limitations", "")
                if title in criteria_regression or title in criteria \
                        or title in ['l_a', 'ros', 'roe', 'roa']:
                    self.points[title] = self.get_points(title, item[1])
            final_points = {}
            for index, values in self.points.items():
                final_points[index] = self.clear_points(values)
            total_points = {}
            for symbol in self.symbols:
                total_points[symbol] = 0
                for index, values in final_points.items():
                    for symbol_in_params, point in values.items():
                        if symbol_in_params == symbol:
                            total_points[symbol] += point
            return {'points': self.points, 'total_points': total_points}
