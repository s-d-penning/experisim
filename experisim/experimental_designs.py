from typing import Type, Dict, Any, Union

import numpy as np
import pandas as pd
import scipy.stats as stats


class ExperimentalUnitModel:
    pass


# class LinearExperimentalUnitModel(ExperimentalUnitModel):
#     # responses: Union[Union[dict[Any, Any], dict], Any]
#
#     def __init__(self, treatments_domain: [[(float, float)]]
#                  , treatments_levels: [[int]]
#                  , treatments_dp: [[int]]
#                  , treatments_measurement_error_percentage: [[float]]
#                  , responses_mean: [[float]], responses_sd: [[float]]
#                  , responses_gradient: [[float]]
#                  , responses_gradient_sd: [[float]]):
#
#         self.vectorised_norm = np.vectorize(stats.norm.rvs)
#
#         self.treatments_dp = np.asarray(treatments_dp)
#         self.response_dimension = len(responses_mean)
#         self.time = 0
#
#         self.responses_mean = np.asarray(responses_mean)
#         self.responses_mean_sd = np.asarray(responses_sd)
#
#         self.responses_gradient = np.asarray(responses_gradient)
#         self.responses_gradient_sd = np.asarray(responses_gradient_sd)
#
#         self.treatments_domain = np.asarray(treatments_domain)
#         self.levels_lcm = np.lcm.reduce(treatments_levels)[0]
#         self.treatments_levels = np.asarray([[self.levels_lcm, self.levels_lcm / x[0]] for x in treatments_levels])
#         self.treatments_measurement_error_percentage = np.asarray(treatments_measurement_error_percentage)
#
#         self.treatments_actual_values = np.asarray(
#             [[(point // repeats) * (stop - start) / (points / repeats) + start for point in range(int(points) + 1)]
#              for ([start, stop], [points, repeats]) in zip(self.treatments_domain, self.treatments_levels)])
#
#         self.treatments_error = np.asarray(
#             [stats.norm.rvs(loc=0, scale=percentage * float(stop - start) / 100.0, size=int(factor_level)+1)
#              for ([factor_level, repeats], [start, stop], [percentage])
#              in zip(self.treatments_levels, self.treatments_domain, self.treatments_measurement_error_percentage)])
#
#         self.treatments_measured_values = np.asarray([error + mean for (error, mean)
#                                                       in zip(self.treatments_error, self.treatments_actual_values)])
#
#         for [[dp], [low, high], values] in zip(self.treatments_dp, self.treatments_domain, self.treatments_measured_values):
#             for index in range(len(values)):
#                 if values[index] < low:
#                     values[index] = low
#                 elif values[index] > high:
#                     values[index] = high
#
#                 values[index] = round(values[index], dp)
#
#         self.condensed_treatment_levels = {}
#         keys = [[self.treatments_actual_values[row, col] for row in range(np.shape(self.treatments_actual_values)[0])] for col in range(np.shape(self.treatments_actual_values)[1])]
#         values = [[self.treatments_measured_values[row, col] for row in range(np.shape(self.treatments_actual_values)[0])] for col in range(np.shape(self.treatments_actual_values)[1])]
#         for k, v in zip(keys, values):
#             self.condensed_treatment_levels[tuple(k)] = tuple(v)
#
#         self.treatment_map = {}
#
#         x = 0
#
#         def get_combinations(rows=0, cols=0, start_col=0, start_row=0) -> [[]]:
#             result = [[]]
#             for col in range(start_col, cols):
#                 new_row = []
#                 for row in range(start_row, rows):
#                     new_row.append((row, col))
#             return result
#
#     def get_treatments(self):
#         pass
#
#     def get_responses(self, time: float, replicate_id: int):
#         if self.time < time:
#             self.time = time
#         else:
#             raise ValueError("Time stamp occurred in the past")
#
#         responses_gradient_error = self.vectorised_norm(scale=self.responses_gradient_sd)
#         responses_gradient = self.responses_gradient + responses_gradient_error
#
#         responses_error = self.vectorised_norm(scale=self.responses_mean_sd)
#         responses_means = np.transpose(np.asmatrix(self.responses_mean + responses_error))
#
#         # for
#         response = responses_gradient * self.treatments_measured_values + responses_means + 0 * time
#         self.responses[(time, replicate_id)] = response
#
#         return response


class LinearExperimentalUnitModel(ExperimentalUnitModel):
    # responses: Union[Union[dict[Any, Any], dict], Any]

    def __init__(self, treatments_domain: [[(float, float)]]
                 , treatments_increments: [[int]]
                 , treatments_dp: [[int]]
                 , treatments_measurement_error_percentage: [[float]]
                 , responses_mean: [[float]], responses_sd: [[float]]
                 , responses_gradient: [[float]]
                 , responses_gradient_sd: [[float]]):

        treatments_actual_values = []
        for treatment_index in range(len(treatments_domain)):
            treatment_actual_values = []
            treatment_levels = treatments_increments[treatment_index][0]
            treatment_domain = treatments_domain[treatment_index]
            treatment_start = treatment_domain[0]
            treatment_end = treatment_domain[1]
            treatment_increment = (treatment_end-treatment_start)/float(treatment_levels)
            for level in range(treatment_levels+1):
                treatment_value = treatment_start + level*treatment_increment
                treatment_actual_values.append(treatment_value)
            treatments_actual_values.append(treatment_actual_values)

        self.all_treatment_combinations = self.create_combinations(treatments_actual_values)

    def create_combinations(self, treatments_values: [[float]], treatment_combination: [float] = None):
        all_combinations = []
        if treatment_combination is None:
            treatment_combination = []

        if len(treatments_values) > 1:
            current_treatment_values = treatments_values[:1][0]
            remaining_treatment_values = treatments_values[1:]
            for current_treatment_value in current_treatment_values:
                expanded_treatment_combination = treatment_combination + [current_treatment_value]
                c = self.create_combinations(remaining_treatment_values, expanded_treatment_combination)
                for combination in c:
                    all_combinations.append(combination)
        else:
            c = []
            current_treatment_values = treatments_values[0]
            for treatment_value in current_treatment_values:
                combination = treatment_combination + [treatment_value]
                c.append(combination)
            return c

        return all_combinations


class ObservationUnitModel:
    pass


class ExperimentalUnit:
    def __init__(self, observation_units: [ObservationUnitModel]):
        pass

    pass


class Experiment:
    pass


class CompleteRandomisedDesign(Experiment):
    def __init__(self, response_models: [LinearExperimentalUnitModel], replications: [int]):
        self.models = response_models

    def run_experiment(self) -> pd.DataFrame:
        raise NotImplementedError
