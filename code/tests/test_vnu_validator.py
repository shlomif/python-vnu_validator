import unittest
from vnu_validator import VnuTest


class MyTest(VnuTest):
    """docstring for MyTest"""
    def test_my(self):
        self.vnu_test_dir('./tests/data', lambda x: False, lambda x: False)
        self.assertTrue(True, "for tests count")


def mytest_main():
    unittest.main()


if __name__ == "__main__":
    mytest_main()
