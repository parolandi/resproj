
import unittest
import common.diagnostics as testme


class TestDiagnostics(unittest.TestCase):


    def test_get_date_and_time(self):
        print(testme.get_date_and_time())
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()