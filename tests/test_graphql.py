import unittest
from replapi import get_data


class TestJSONMethods(unittest.TestCase):


    def test_setup_replit_class(self):
        '''Tests that we create an instance of the class without raising any exceptions'''
        r = get_data.ReplIt('reagentx', 10)
        return True



    def test_query(self):
        '''Tests that the query accesses the proper variables'''
        r = get_data.ReplIt('reagentx', number_to_retreive=10)
        self.assertEqual(len(r.data), 10)


    def test_get_urls(self):
        '''Tests that the get_urls() method returns the proper number of URLS and that they match the expected form'''
        r = get_data.ReplIt('reagentx', number_to_retreive=10)
        urls = r.get_urls()
        self.assertEqual(len(urls), 10)
        for url in urls:
            self.assertEqual(url[:11], '/@reagentx/')


if __name__ == "__main__":
    unittest.main()
