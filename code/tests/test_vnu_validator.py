import unittest
from vnu_validator import VnuTest


class MyTest(VnuTest):
    """docstring for MyTest"""
    def test_my(self):
        self.vnu_test_dir('./tests/data', lambda x: False, lambda x: False)


def test_main():
    unittest.main()


test_main()
