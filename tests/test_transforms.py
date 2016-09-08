import unittest

from scrape_nordstrom.transforms import add_field, to_float, transform_initial_data

class UtilsTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_add_field(self):
        item = {}
        add_field(item, 'name', ['ddd'])
        assert item['name'] == 'ddd'

        add_field(item, 'dog', 'ddd')
        assert item['dog'] == 'ddd'

        add_field(item, 'cat', [])
        assert item['cat'] == None

    def test_to_float(self):
        val = to_float('234.42')
        assert val == 234.42

        val = to_float('2,234.42')
        assert val == 2234.42

        val = to_float('$2,234.42')
        assert val == 2234.42

    def test_json_transform(self):
        test_str = "React.render(React.createElement(ProductDesktop, {\"initialData\":{\"Model\":{\"StyleModel\":{\"Id\":4180678, \"ApiVersion\":null}}}), document.getElementById( 'main' ));"

        val = transform_initial_data(test_str)
        assert len(val.keys()) > 0
