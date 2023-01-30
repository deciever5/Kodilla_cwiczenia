import unittest
from prime_factors import prime_factors


class PrimeFactorsTest(unittest.TestCase):
    def test_function_exist(self):
        self.assertTrue(callable(prime_factors))

    def test_input_exist(self):
        self.assertRaises(TypeError, prime_factors(6))

    def test_return_type(self):
        self.assertIsInstance(prime_factors(6), list)

    def test_input_type(self):
        self.assertRaises(ValueError,prime_factors,'abs')

    def test_prime_number_test(self):
        self.assertEqual(prime_factors(7),[7])
        self.assertEqual(prime_factors(13), [13])
        self.assertEqual(prime_factors(19), [19])

    def test_prope_result(self):
        self.assertEqual(prime_factors(32),[2,2,2,2,2])
        self.assertEqual(prime_factors(33), [3,11])
        self.assertEqual(prime_factors(325), [5,5,13])






if __name__ == '__main__':
    unittest.main()
