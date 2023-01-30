import unittest
from convert_to_decimal import convert_to_decimal as ctd


class ConvertToDecimalTest(unittest.TestCase):
    def test_function_exists(self):
        self.assertTrue(callable(ctd))

    def test_input_exists(self):
        self.assertRaises(TypeError, ctd)



if __name__ == '__main__':
    unittest.main()
