import unittest
from convert_to_decimal import convert_to_decimal as ctd


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



if __name__ == '__main__':
    unittest.main()
