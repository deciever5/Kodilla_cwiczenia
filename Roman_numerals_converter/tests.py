import unittest
from convert_to_decimal import convert_to_decimal as ctd
from convert_to_roman import  convert_to_roman as ctr


class ConvertToDecimalTest(unittest.TestCase):
    def test_function_exists(self):
        self.assertTrue(callable(ctd))

    def test_input_exists(self):
        self.assertRaises(TypeError, ctd)

    def test_return_type(self):
        self.assertEqual(type(ctd('X')), int)

    def test_input_type(self):
        self.assertRaises(ValueError, ctd, 10)

    def test_simple_conversion(self):
        self.assertEqual(ctd('X'), 10)
        self.assertEqual(ctd('L'), 50)
        self.assertEqual(ctd('C'), 100)

    def test_adv_conversion(self):
        self.assertEqual(ctd('XLV'), 45)
        self.assertEqual(ctd('CMMLVIII'), 1958)
        self.assertEqual(ctd('CDXXXII'), 432)


class ConvertToRomanTest(unittest.TestCase):
    def test_input_type(self):
        self.assertRaises(ValueError, ctr,'abc')

    def test_input_value(self):
        self.assertRaises(ValueError, ctr,-10)

    def test_return_type(self):
        self.assertEqual(type(ctr(10)), str)

    def test_conversion(self):
        self.assertEqual(ctr(10), 'X')
        self.assertEqual(ctr(4), 'IV')
        self.assertEqual(ctr(50), 'L')
        self.assertEqual(ctr(90), 'XC')
        self.assertEqual(ctr(100), 'C')
        self.assertEqual(ctr(400), 'CD')
        self.assertEqual(ctr(900), 'CM')
        self.assertEqual(ctr(1000), 'M')

if __name__ == '__main__':
    unittest.main()
