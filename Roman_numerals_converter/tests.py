import unittest
from convert_to_decimal import convert_to_decimal as ctd


class ConvertToDecimalTest(unittest.TestCase):
    def test_function_exists(self):
        self.assertTrue(callable(ctd))


if __name__ == '__main__':
    unittest.main()
