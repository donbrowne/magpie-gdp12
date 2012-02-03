import unittest
import urllib2

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.msg = urllib2.urlopen(urllib2.Request("http://127.0.0.1:8000")).read()
        self.expected_msg = "Hello, world. Welcome to Magpie."

    def test_hello(self):
        self.assertTrue(self.msg == self.expected_msg)

if __name__ == '__main__':
    unittest.main()
