import unittest
import experisim.experimental_designs as sim


class LinearModelTestCase(unittest.TestCase):
    def test_get_response(self):
        experimental_unit = sim.LinearExperimentalUnitModel(treatments_domain=[[0, 30],
                                                                               [0,  100],
                                                                               [0, 28]]
                                                            , treatments_increments=[[3],
                                                                                     [5],
                                                                                     [4]]
                                                            , treatments_dp=[[2],
                                                                             [2],
                                                                             [2]]
                                                            , treatments_measurement_error_percentage=[[1],
                                                                                                       [2],
                                                                                                       [3]]
                                                            , responses_mean=[[50],
                                                                              [100],
                                                                              [150]]  # The default value
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

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
