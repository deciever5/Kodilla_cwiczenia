def test_prime_factors(self):
    # Test if prime number is returned as a single-element list
    self.assertEqual(prime_factors(13), [13])
    # Test if prime factors are returned in a list
    self.assertEqual(prime_factors(159172), [2, 2, 13, 3061])
    # Test if input is 0 or 1
    self.assertEqual(prime_factors(0), [])
    self.assertEqual(prime_factors(1), [])
    # Test if input is negative number
    self.assertEqual(prime_factors(-159172), [2, 2, 13, 3061])