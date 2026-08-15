import json
import requests
import unittest
from unittest import Mock
from moon import Moon

test_json_file_new = "test_json.json"

test_json_file_full = "test_json_full.json"

class TestTheMoon(unittest.TestCase):

    def test_the_new_moon():
        moon = Mock(age = 20, phasePercentage = 30, imageUrl = "yum.com", json_file=test_json_file_new)
        self.assertEqual(moon)


    def test_the_full_moon():
        moon = Mock(age = 20, phasePercentage = 30, imageUrl = "yum.com", json_file=test_json_file_full)


        


