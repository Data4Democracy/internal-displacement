from unittest import TestCase
from internal_displacement.extracted_report import *

class TestExtractedReport(TestCase):
	
	def test_convert_quantity(self):
		self.assertEqual(convert_quantity("twelve"), 12)
		self.assertEqual(convert_quantity("seventy five"), 75)
		self.assertEqual(convert_quantity("3 hundred"), 300)
		self.assertEqual(convert_quantity("twelve hundred"), 1200)
		self.assertEqual(convert_quantity("seven million"), 7000000)
		self.assertEqual(convert_quantity("twelve thousand three hundred four"), 12304)
		self.assertEqual(convert_quantity("32 thousand"), 32000)
		self.assertEqual(convert_quantity(["one", "million"]), 1000000)