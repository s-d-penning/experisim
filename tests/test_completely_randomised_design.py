import math
import numpy as np
import unittest
import experisim.experimental_designs as sim


class LinearModelTestCase(unittest.TestCase):
    def test_get_response(self):
        experimental_unit = sim.LinearExperimentalUnitModel(responses_mean=[[50],
                                                                            [100],
                                                                            [150]]
                                                            , responses_sd=[[10],
                                                                            [5],
                                                                            [15]]
                                                            , responses_gradient=[[0.1, 0.0, 0.0],
                                                                                  [0.0, 0.2, 0.0],
                                                                                  [0.0, 0.0, 0.3]]
                                                            , responses_gradient_sd=[[0.001, 0.000, 0.000],
                                                                                     [0.000, 0.001, 0.000],
                                                                                     [0.000, 0.000, 0.001]])

        # treatments = experimental_unit.get_treatments()
        #
        # responses = experimental_unit.get_responses(time=1.0, replicate_id=0)
        self.assertEqual(True, True)


class CombinatoricsTestCase(unittest.TestCase):
    def test_calculate_levels(self):
        domain_values = [[0.0, 100.0],
                         [0.0, 100.0],
                         [0.0, 100.0]]
        fractional_domain_levels = [[0.0, 0.5, 1.0],
                                    [0.0, 0.25, 0.5, 1.0],
                                    [0.0, 0.25, 0.5, 1.0]]
        domain_levels = sim.Combinatorics.calculate_levels(domain_values, fractional_domain_levels)
        for level_index in range(len(fractional_domain_levels)):
            fractional_levels_count = len(fractional_domain_levels[level_index])
            domain_levels_count = len(domain_levels[level_index])
            self.assertEqual(fractional_levels_count, domain_levels_count)

    def test_combinations(self):
        domain_levels = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
        combinations = sim.Combinatorics.calculate_combinations(domain_levels)
        combinations_count = math.prod([len(combination) for combination in combinations])

        self.assertEqual(len([combination for combination in combinations]),
                         math.prod([len(domain_level) for domain_level in domain_levels]))

        domain_levels = [['a1', 'a2', 'a3'], ['b1', 'b2', 'b3'], ['c1', 'c2', 'c3']]
        combinations = sim.Combinatorics.calculate_combinations(domain_levels)
        combinations_count = len([combination for combination in combinations])

        self.assertEqual(len([combination for combination in combinations]),
                         math.prod([len(domain_level) for domain_level in domain_levels]))

    def test_calculate_true_combinations(self):
        factors_domain_values = [[0.0, 100.0],
                                 [0.0, 100.0],
                                 [0.0, 100.0]]
        factors_domain_boundaries = [[True, False],
                                     [False, False],
                                     [True, True]]
        factors_increments = [[0.0, 0.5, 1.0],
                              [0.0, 0.25, 0.5, 1.0],
                              [0.0, 0.25, 0.5, 1.0]]
        factors_dp = [[2],
                      [2],
                      [2]]
        factors_measurement_error_sd = [[0.1],
                                        [0.1],
                                        [1.0]]
        factors_measurement_error_bias = [[0.0],
                                          [1.0],
                                          [0.0]]

        stated_factors_level_values = sim.Combinatorics.calculate_levels(factors_domain_values, factors_increments)
        stated_factors_combinations = sim.Combinatorics.calculate_combinations(stated_factors_level_values)
        true_factors_combinations = sim.Combinatorics.calculate_true_combinations(stated_factors_combinations,
                                                                                  factors_domain_values,
                                                                                  factors_domain_boundaries,
                                                                                  factors_dp,
                                                                                  factors_measurement_error_sd,
                                                                                  factors_measurement_error_bias)
        # TODO: Add real test conditions here
        self.assertEqual(len(stated_factors_combinations), len(true_factors_combinations))


class CompleteRandomisedDesignTestCase(unittest.TestCase):
    def test_single_factor_combinations(self):
        factors_domain_values = [0.0, 100.0]
        factors_domain_boundaries = [True, False]
        factors_increments = [0.0, 0.25, 0.5, 1.0]
        factors_dp = [2]
        factors_measurement_error_sd = [0.1]
        factors_measurement_error_bias = [0.0]
        design = sim.CompleteRandomisedDesign(factor_domain_values=factors_domain_values
                                              , factors_domain_boundaries=factors_domain_boundaries
                                              , factors_increments=factors_increments
                                              , factors_dp=factors_dp
                                              , factors_measurement_error_sd=factors_measurement_error_sd
                                              , factors_measurement_error_bias=factors_measurement_error_bias)

        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
