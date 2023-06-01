import inspect
import unittest

from naming import Naming


class TestClass:
    instance_field: str = "default"

    def __init__(self, v: str = ""):
        self.instance_field = v


class NamingTests(unittest.TestCase):
    def setUp(self):
        self.naming = Naming("~/internal/src/sboothza/dalgen/dictionary.txt",
                             "~/internal/src/sboothza/dalgen/bigworddictionary.txt")

    def testname(self):
        name_value = "Stephen"
        result = self.naming.string_to_name(name_value)
        self.assertEqual(result.lower(), "stephen")
        self.assertEqual(result.upper(), "STEPHEN")
        self.assertEqual(result.pascal(), "Stephen")
        self.assertEqual(result.camel(), "stephen")
        self.assertEqual(result.snake(), "stephen")

    def testcomplex_name(self):
        name_value = "currentemployeerecord"
        result = self.naming.string_to_name(name_value)
        self.assertEqual(result.lower(), "currentemployeerecord")
        self.assertEqual(result.upper(), "CURRENTEMPLOYEERECORD")
        self.assertEqual(result.pascal(), "CurrentEmployeeRecord")
        self.assertEqual(result.camel(), "currentEmployeeRecord")
        self.assertEqual(result.snake(), "current_employee_record")

    def testbigword_name(self):
        name_value = "scaninterestrates"
        result = self.naming.string_to_name(name_value)
        self.assertEqual(result.lower(), "scaninterestrates")
        self.assertEqual(result.upper(), "SCANINTERESTRATES")
        self.assertEqual(result.pascal(), "ScanInterestRates")
        self.assertEqual(result.camel(), "scanInterestRates")
        self.assertEqual(result.snake(), "scan_interest_rates")
        self.assertEqual(result.upper_snake(), "SCAN_INTEREST_RATES")

    def test_types(self):
        a = TestClass("v1")
        b = TestClass("v2")
        self.assertEqual(a.instance_field, "v1")
        self.assertEqual(b.instance_field, "v2")

    def test_sigs(self):
        sig = inspect.getmembers(TestClass)
        a = TestClass("v1")
        sig = inspect.getmembers(a)
        a.other_instance_field = "static1"
        sig = inspect.getmembers(a)


if __name__ == '__main__':
    unittest.main()
