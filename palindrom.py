import unittest


def palindrome_check(x):
    """ Checking if a given string or number  is a palindrome """
    return x[::] == x[::-1]


class TestPalindromeCheck(unittest.TestCase):

    def test_string_input(self):
        # Test if the input is a string or number
        self.assertRaises(TypeError, palindrome_check, [123, 321])
        self.assertRaises(TypeError, palindrome_check, [123, 222, 321])
        self.assertRaises(TypeError, palindrome_check, (123, 321))

    def test_not_none_input(self):
        # Test if the input is not None
        self.assertRaises(TypeError, palindrome_check, None)

    def test_case_sensitivity(self):
        # Test if the function is case-insensitive
        self.assertTrue(palindrome_check("kajak"))
        self.assertTrue(palindrome_check("KAJAK"))
        self.assertTrue(palindrome_check("Kajak"))
        self.assertTrue(palindrome_check("rAdAr"))

    def test_palindrome(self):
        # Test if the function correctly determines palindromes
        self.assertTrue(palindrome_check("Słowo"))
        self.assertFalse(palindrome_check("Niepalindrom"))
        self.assertTrue(palindrome_check("Madam"))

    def test_alphanumeric(self):
        # Test that function only considers alphanumeric characters
        self.assertTrue(palindrome_check("A man a plan a canal Panama"))
        self.assertFalse(palindrome_check("A man, a plan, a canal, Panama!"))


if __name__ == '__main__':
    unittest.main()
