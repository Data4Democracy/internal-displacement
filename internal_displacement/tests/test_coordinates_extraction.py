from unittest import TestCase
from internal_displacement.pipeline import get_coordinates_mapzen

class TestCoordinatesExtraction(TestCase):
	
	def test_get_coordinates_mapzen(self):
	    res = get_coordinates_mapzen(country="Austria")
	    self.assertEqual(res['coordinates'], "14.143702,47.522617")
	    res = get_coordinates_mapzen("Austria") # a city
	    self.assertEqual(res['coordinates'], "-93.33167,16.43083")
	    self.assertEqual(res['flag'], "multiple-results")
	    res = get_coordinates_mapzen("Vienna")
	    self.assertEqual(res['coordinates'], "16.37208,48.20849")
	    self.assertEqual(res['flag'], "multiple-results")
	    res = get_coordinates_mapzen(city="Vienna", country="Austria")
	    self.assertEqual(res['coordinates'], "16.37208,48.20849")
	    self.assertEqual(res['flag'], "single-result")
	    res = get_coordinates_mapzen(city="Vienna", country="United States")
	    self.assertEqual(res['coordinates'], "-77.260053,38.898599")
	    res = get_coordinates_mapzen(city="Vienna", subdivision="Maryland", country="United States")
	    self.assertEqual(res['coordinates'], "-75.833966,38.483475")
	    self.assertEqual(res['flag'], "single-result")
	    res = get_coordinates_mapzen("Vienna", hints=['Turkey','Indonesia', 'Austria', 'France'])
	    self.assertEqual(res['coordinates'], "16.37208,48.20849")
	    self.assertEqual(res['flag'], "multiple-results")
	    res = get_coordinates_mapzen("Vienna", hints=['Turkey','Germany', 'Australia', 'United States'])
	    self.assertEqual(res['coordinates'], "-77.260053,38.898599")
	    self.assertEqual(res['flag'], "multiple-results")
	    res = get_coordinates_mapzen("Vienna", hints=['Turkey','Germany', 'Australia', 'United States', 'Georgia'])
	    self.assertEqual(res['coordinates'], "-83.79545,32.09156")
	    self.assertEqual(res['flag'], "multiple-results")