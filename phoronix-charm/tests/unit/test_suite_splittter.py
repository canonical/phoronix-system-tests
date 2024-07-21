import unittest

from suite_splitter import split_suite


class TestSplitSuite(unittest.TestCase):
    def test_split(self):
        split_suite("foobar", 4)
        pass
