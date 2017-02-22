from unittest import TestCase
from internal_displacement.report import Report

class TestReport(TestCase):


    def setUp(self):
        pass
    def tearDown(self):
        pass


    def test_equality(self):
       test_report_1 = Report(["Some Place"],["Yesterday"],"destroyed","house",12,"Yesterday 12 houses were destroyed.")
       test_report_2 = Report(["Some Place"],["Yesterday"],"destroyed","house",12,"Yesterday 12 houses were destroyed.")
       test_report_3 = Report(["Some Place"],["Yesterday"],"destroyed","house",13,"Yesterday 13 houses were destroyed.")
       self.assertEqual(test_report_1,test_report_2)
       self.assertNotEqual(test_report_1,test_report_3)