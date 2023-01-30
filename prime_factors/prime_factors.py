import unittest


def prime_factors(number):
    return []


class PrimeFactorsTest(unittest.TestCase):
    def test_function_exist(self):
        self.assertTrue(callable(prime_factors))

    def test_input_exist(self):
        self.assertRaises(TypeError, prime_factors(6))

    def test_return_as_list(self):
        self.assertEqual(type(prime_factors(6)),list)


if __name__ == '__main__':
    unittest.main()
