# coding=utf-8
"""
InaSAFE Disaster risk assessment tool developed by AusAid and World Bank
- **Impact function Test Cases.**

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
__author__ = 'akbargumbira@gmail.com'
__date__ = '11/12/2015'
__copyright__ = ('Copyright 2012, Australia Indonesia Facility for '
                 'Disaster Reduction')

import unittest

from safe.impact_functions.impact_function_manager import ImpactFunctionManager
from safe.impact_functions.generic.classified_polygon_population\
    .impact_function import ClassifiedPolygonHazardPopulationFunction
from safe.test.utilities import test_data_path
from safe.storage.core import read_layer


class TestClassifiedPolygonPopulationFunction(unittest.TestCase):
    """Test for Classified Polygon on Population Impact Function."""

    def setUp(self):
        registry = ImpactFunctionManager().registry
        registry.clear()
        registry.register(ClassifiedPolygonHazardPopulationFunction)

    def test_run(self):
        """TestClassifiedPolygonPopulationFunction: Test running the IF."""
        generic_polygon_path = test_data_path(
            'hazard', 'classified_generic_polygon.shp')
        population_path = test_data_path(
            'exposure', 'pop_binary_raster_20_20.asc')

        generic_polygon_layer = read_layer(generic_polygon_path)
        population_layer = read_layer(population_path)

        impact_function = ClassifiedPolygonHazardPopulationFunction.instance()
        impact_function.hazard = generic_polygon_layer
        impact_function.exposure = population_layer
        impact_function.parameters['hazard zone attribute'] = 'h_zone'
        impact_function.run()
        impact_layer = impact_function.impact
        # Check the question
        expected_question = ('In each of the hazard zones how many people '
                             'might be impacted.')
        message = 'The question should be %s, but it returns %s' % (
            expected_question, impact_function.question)
        self.assertEqual(expected_question, impact_function.question, message)
        # Count by hand
        impact = {
            'Low Hazard Zone': 0,
            'Medium Hazard Zone': 132.0,
            'High Hazard Zone': 49.0,
        }
        impact_features = impact_layer.get_data()
        for i in range(len(impact_features)):
            impact_feature = impact_features[i]
            hazard_zone = impact_feature.get('h_zone')
            expected = impact[hazard_zone]
            result = impact_feature['population']
            message = 'Expecting %s, but it returns %s' % (expected, result)
            self.assertEqual(expected, result, message)

    def test_filter(self):
        """TestClassifiedPolygonPopulationFunction: Test filtering IF"""
        hazard_keywords = {
            'category': 'hazard',
            'subcategory': 'earthquake',
            'unit': 'classes',
            'layer_type': 'vector',
            'data_type': 'polygon'
        }

        exposure_keywords = {
            'category': 'exposure',
            'subcategory': 'population',
            'layer_type': 'raster',
            'data_type': 'continuous',
            'unit': 'people_per_pixel'
        }

        impact_functions = ImpactFunctionManager().filter_by_keywords(
            hazard_keywords, exposure_keywords)
        message = 'There should be 1 impact function, but there are: %s' % \
                  len(impact_functions)
        self.assertEqual(1, len(impact_functions), message)

        retrieved_if = impact_functions[0].metadata().as_dict()['id']
        expected = ImpactFunctionManager().get_function_id(
            ClassifiedPolygonHazardPopulationFunction)
        message = 'Expecting %s, but getting %s instead' % (
            expected, retrieved_if)
        self.assertEqual(expected, retrieved_if, message)
