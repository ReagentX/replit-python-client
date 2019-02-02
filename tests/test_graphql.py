import unittest
from replapi import get_data


class TestJSONMethods(unittest.TestCase):


    def test_setup_replit_class(self):
        r = get_data.ReplIt('reagentx', 10)
        return True



    def test_query(self):
        r = get_data.ReplIt('reagentx', number_to_retreive=10)
        self.assertEqual(len(r.data), 10)


    def test_get_urls(self):
        r = get_data.ReplIt('reagentx', number_to_retreive=10)
        urls = r.get_urls()
        self.assertEqual(len(urls), 10)


if __name__ == "__main__":
    unittest.main()