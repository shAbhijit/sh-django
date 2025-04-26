# Sample test

from django.test import SimpleTestCase

from app import calc  # noqa


class CalcTests(SimpleTestCase):
    """Test the calculator functions."""

    def test_add_numbers(self):
        """Test adding two numbers together."""
        res = calc.add(5, 6)
        self.assertEqual(res, 11)

    def test_subtract_numbers(self):
        """Test subtracting two numbers."""
        res = calc.subtract(10, 5)
        self.assertEqual(res, 5)

    # def test_home_page(self):
    #     """
    #     Test the home page
    #     """
    #     client = APIClient()
    #     response = client.get('/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "Welcome to the home page")
