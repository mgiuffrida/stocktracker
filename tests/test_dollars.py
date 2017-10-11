#!/usr/bin/env python2

"""
Tests for dollars module.
"""

from decimal import Decimal as D
import unittest

from stocktracker import dollars

# from .context import dollars


class TestDollars(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(dollars.parse('10.50'), D('10.50'))
        self.assertEqual(dollars.parse('1234.99'), D('1234.99'))
        self.assertEqual(dollars.parse('1,234.99'), D('1234.99'))
        self.assertEqual(dollars.parse('$42.85'), D('42.85'))
        self.assertEqual(dollars.parse('(42.85)'), D('-42.85'))
        self.assertEqual(dollars.parse('-42.85'), D('-42.85'))
        self.assertEqual(dollars.parse('-$42.85'), D('-42.85'))
        self.assertEqual(dollars.parse('$(42.85)'), D('-42.85'))

    def test_to_str(self):
        self.assertEqual(dollars.to_str(D('10.50')), '$10.50')
        self.assertEqual(dollars.to_str(D('1234.99')), '$1234.99')
        self.assertEqual(dollars.to_str(D('1.2345')), '$1.23')
        self.assertEqual(dollars.to_str(D('1234.5678')), '$1234.57')
        self.assertEqual(dollars.to_str(D('-1.2345')), '$(1.23)')
        self.assertEqual(dollars.to_str(D('-1234.5678')), '$(1234.57)')

    def test_round_decimal(self):
        self.assertEqual(str(dollars.round_decimal(D('1.5678'))), '1.57')
        self.assertEqual(str(dollars.round_decimal(D('1.5678'), 0)), '2')
        self.assertEqual(str(dollars.round_decimal(D('1.5678'), 1)), '1.6')
        self.assertEqual(str(dollars.round_decimal(D('1.5678'), 4)), '1.5678')
        self.assertEqual(str(dollars.round_decimal(D('1.49'), 0)), '1')
        self.assertEqual(str(dollars.round_decimal(D('1.5'), 0)), '2')
        self.assertEqual(str(dollars.round_decimal(D('-1.49'), 0)), '-1')
        self.assertEqual(str(dollars.round_decimal(D('-1.5'), 0)), '-2')
        self.assertEqual(str(dollars.round_decimal(D('.049'))), '0.05')

        self.assertEqual(str(dollars.round_decimal(D('.05'))), '0.05')
        self.assertEqual(str(dollars.round_decimal(D('-.049'))), '-0.05')
        self.assertEqual(str(dollars.round_decimal(D('-.05'))), '-0.05')

    def test_remove_trailing_zeros(self):
        self.assertEqual(str(dollars.remove_trailing_zeros(D('2.2500'))),
                         '2.25')
        self.assertEqual(str(dollars.remove_trailing_zeros(D('-2.2500'))),
                         '-2.25')
        self.assertEqual(str(dollars.remove_trailing_zeros(D('22500'))),
                         '22500')
        self.assertEqual(str(dollars.remove_trailing_zeros(D('-22500'))),
                         '-22500')
        self.assertEqual(str(dollars.remove_trailing_zeros(D('225'))), '225')
        self.assertEqual(str(dollars.remove_trailing_zeros(D('-225'))), '-225')

    def test_precise_division(self):
        self.assertEqual(str(dollars.precise_division(D('6'), D('2'))), '3')
        self.assertEqual(str(dollars.precise_division(D('7'), D('2'))), '3.5')
        self.assertEqual(str(dollars.precise_division(D('7.0'), D('2'))),
                         '3.5')
        self.assertEqual(str(dollars.precise_division(D('2.48'), D('1.24'))),
                         '2')
        self.assertEqual(str(dollars.precise_division(D('2.48'), D('1.23'))),
                         '2.02')
        self.assertEqual(str(dollars.precise_division(D('351'), D('121'))),
                         '2.9')
        self.assertEqual(str(dollars.precise_division(D('345'), D('120'))),
                         '2.875')
        self.assertEqual(str(dollars.precise_division(D('2.5555'),
                                                      D('.0666'))), '38.371')
        self.assertEqual(str(dollars.precise_division(D('129.0540'),
                                                      D('2.5555'))), '50.5005')
        self.assertEqual(str(dollars.precise_division(D('2.7456'), D('2'))),
                         '1.3728')
        self.assertEqual(str(dollars.precise_division(D('.7456'), D('2'))),
                         '0.3728')
        self.assertEqual(str(dollars.precise_division(D('2'),
                                                      D('1.13848332'))), '2')

    def test_increment_last_place(self):
        self.assertEqual(str(dollars.increment_last_place(D('1'))), '2')
        self.assertEqual(str(dollars.increment_last_place(D('-1'))), '-2')
        self.assertEqual(str(dollars.increment_last_place(D('1.0'))), '1.1')
        self.assertEqual(str(dollars.increment_last_place(D('-1.0'))), '-1.1')
        self.assertEqual(str(dollars.increment_last_place(D('1.1'))), '1.2')
        self.assertEqual(str(dollars.increment_last_place(D('-1.1'))), '-1.2')
        self.assertEqual(str(dollars.increment_last_place(D('199'))), '200')
        self.assertEqual(str(dollars.increment_last_place(D('-199'))), '-200')
        self.assertEqual(str(dollars.increment_last_place(D('99'))), '100')
        self.assertEqual(str(dollars.increment_last_place(D('-99'))), '-100')
        self.assertEqual(str(dollars.increment_last_place(D('909.9'))),
                         '910.0')
        self.assertEqual(str(dollars.increment_last_place(D('-909.9'))),
                         '-910.0')
        self.assertEqual(str(dollars.increment_last_place(D('0'))), '1')
        self.assertEqual(str(dollars.increment_last_place(D('-0'))), '-1')
        self.assertEqual(str(dollars.increment_last_place(D('0.0'))), '0.1')
        self.assertEqual(str(dollars.increment_last_place(D('-0.0'))), '-0.1')

    def test_decrement_last_place(self):
        self.assertEqual(str(dollars.decrement_last_place(D('2.1'))), '2.0')
        self.assertEqual(str(dollars.decrement_last_place(D('-2.1'))), '-2.0')
        self.assertEqual(str(dollars.decrement_last_place(D('2.0'))), '1.9')
        self.assertEqual(str(dollars.decrement_last_place(D('-2.0'))), '-1.9')
        self.assertEqual(str(dollars.decrement_last_place(D('2.00'))), '1.99')
        self.assertEqual(str(dollars.decrement_last_place(D('-2.00'))),
                         '-1.99')
        self.assertEqual(str(dollars.decrement_last_place(D('10.00'))), '9.99')
        self.assertEqual(str(dollars.decrement_last_place(D('-10.00'))),
                         '-9.99')
        self.assertEqual(str(dollars.decrement_last_place(D('300.00'))),
                         '299.99')
        self.assertEqual(str(dollars.decrement_last_place(D('-300.00'))),
                         '-299.99')
        self.assertEqual(str(dollars.decrement_last_place(D('-0'))), '1')
        self.assertEqual(str(dollars.decrement_last_place(D('0'))), '-1')
        self.assertEqual(str(dollars.decrement_last_place(D('-0.0'))), '0.1')
        self.assertEqual(str(dollars.decrement_last_place(D('0.0'))), '-0.1')

        # Sanity check: increment_last_place and decrement_last_place should
        # return different numbers.
        self.assertNotEqual(str(dollars.increment_last_place(D('0.0'))),
                            str(dollars.decrement_last_place(D('0.0'))))
        self.assertNotEqual(str(dollars.increment_last_place(D('-0.0'))),
                            str(dollars.decrement_last_place(D('-0.0'))))

    def compare_fixed_transaction(self, num_shares, price, total, fees,
                                  expected_num_shares, expected_price,
                                  expected_total, expected_fees):
        result = dollars.fix_up_transaction(
            num_shares=D(num_shares),
            price=D(price),
            total=D(total),
            fees=None if fees is None else D(fees))
        self.assertEqual(str(result['num_shares']), expected_num_shares)
        self.assertEqual(str(result['price']), expected_price)
        self.assertEqual(str(result['total']), expected_total)
        self.assertEqual(str(result['fees']), expected_fees)

    def test_fix_up_transaction(self):
        self.compare_fixed_transaction(
            '2.00', '4.00', '8.01', None,
            '2.00', '4.005', '8.01', '0')
        self.compare_fixed_transaction(
            '2.00', '4.00', '8.99', None,
            '2.00', '4.00', '8.99', '0.99')
        self.compare_fixed_transaction(
            '1.23', '5.432', '6.71', None,
            '1.23', '5.455', '6.71', '0')
        self.compare_fixed_transaction(
            '1.23', '5.432', '6.71', '0',
            '1.23', '5.455', '6.71', '0')
