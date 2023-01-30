import unittest
import prime_factors as pf


class PrimeFactorsTest(unittest.TestCase):
    def test_function_exist(self):
        self.assertTrue(callable(pf.prime_factors))

    def test_input_exist(self):
        self.assertRaises(TypeError, pf.prime_factors(6))

    def test_return_as_list(self):
        self.assertEqual(type(pf.prime_factors(6)), list)

    def test_prime_number_test(self):
        self.assertEqual(pf.prime_factors(7),[7])
        self.assertEqual(pf.prime_factors(13), [13])
        self.assertEqual(pf.prime_factors(19), [19])



if __name__ == '__main__':
    unittest.main()
