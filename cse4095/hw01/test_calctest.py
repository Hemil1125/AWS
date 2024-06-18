"""This is a unittest."""
import unittest
from pythoncalc import add, subtract, multiply, divide


class TestCalculator(unittest.TestCase):
    '''Demonstrates tests'''

    def test_add(self):
        '''Demonstrates add'''
        result = add(5, 3)
        self.assertEqual(result, 8.0)

    def test_subtract(self):
        '''Demonstrates sub'''
        result = subtract(5, 3)
        self.assertEqual(result, 2.0)

    def test_multiply(self):
        '''Demonstrates mult'''
        result = multiply(5, 3)
        self.assertEqual(result, 15.0)

    def test_divide(self):
        '''Demonstrates div'''
        result = divide(6, 3)
        self.assertEqual(result, 2.0)

    def test_divide_by_zero(self):
        '''Demonstrates /0'''
        with self.assertRaises(ZeroDivisionError):
            divide(5, 0)

if __name__ == "__main__":
    unittest.main()
