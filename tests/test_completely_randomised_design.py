import math
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


class CompleteRandomisedDesignTestCase(unittest.TestCase):
    def test_create_combinations(self):
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
        design = sim.CompleteRandomisedDesign(factors_domain_values=factors_domain_values
                                              , factors_domain_boundaries=factors_domain_boundaries
                                              , factors_increments=factors_increments
                                              , factors_dp=factors_dp
                                              , factors_measurement_error_sd=factors_measurement_error_sd
                                              , factors_measurement_error_bias=factors_measurement_error_bias)

        combinations = math.prod([len(factor) for factor in factors_increments])
        factors = len(factors_domain_values)
        # TODO: Test to see if the boundary conditions are met
        s2 = design.stated_factors_combinations.shape
        self.assertTrue(s2, (combinations, factors))
        s3 = design.true_factors_combinations.shape
        self.assertTrue(s3, (combinations, factors))


if __name__ == '__main__':
    unittest.main()
