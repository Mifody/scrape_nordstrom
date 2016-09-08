import unittest

from scrape_nordstrom.utils import xcontains

class UtilsTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_xcontains(self):
        val = xcontains('span', 'a-class')
        assert val == "//span[contains(@class, 'a-class')]/text()"

        val = xcontains('a', 'ddd', 'href()')
        assert val == "//a[contains(@class, 'ddd')]/href()"
