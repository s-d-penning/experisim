from typing import Type, Dict, Any, Union

import numpy as np
import pandas as pd
import scipy.stats as stats


class ExperimentalUnitModel:
    pass


class LinearExperimentalUnitModel(ExperimentalUnitModel):
    def __init__(self, responses_mean: [[float]]
                 , responses_sd: [[float]]
                 , responses_gradient: [[float]]
                 , responses_gradient_sd: [[float]]):
        pass


class ObservationUnitModel:
    pass


class ExperimentalUnit:
    def __init__(self, observation_units: [ObservationUnitModel]):
        self.observation_units = observation_units


class Experiment:
    pass


class CompleteRandomisedDesign(Experiment):
    def __init__(self
                 , treatments_domain: [[(float, float)]]
                 , treatments_increments: [[int]]
                 , treatments_dp: [[int]]
                 , treatments_measurement_error_sd: [[float]]
                 , treatments_measurement_error_bias: [[float]]):

        treatments_actual_values = self.calculate_treatment_levels(treatments_domain,treatments_increments)
        self.treatments_actual_values = np.asarray(treatments_actual_values)
        actual_treatments_combinations = self.calculate_treatment_combinations(treatments_actual_values)
        self.actual_treatments_combinations = np.asarray(actual_treatments_combinations)
        approximate_treatment_combinations = \
            self.measure_treatment_combinations(actual_treatments_combinations,
                                                treatments_domain,
                                                treatments_dp,
                                                treatments_measurement_error_sd,
                                                treatments_measurement_error_bias)
        self.approximate_treatment_combinations = np.asarray(approximate_treatment_combinations)

    @staticmethod
    def calculate_treatment_levels(treatments_domain: [[(float, float)]],
                                   treatments_increments: [[int]]) -> [[float]]:
        treatments_actual_values = []
        for treatment_index in range(len(treatments_domain)):
            treatment_actual_values = []
            treatment_levels = treatments_increments[treatment_index]
            treatment_domain = treatments_domain[treatment_index]
            treatment_start = treatment_domain[0]
            treatment_end = treatment_domain[1]
            treatment_increment = treatment_end - treatment_start
            for level in treatment_levels:
                treatment_value = treatment_start + level * treatment_increment
                treatment_actual_values.append(treatment_value)
            treatments_actual_values.append(treatment_actual_values)

        return treatments_actual_values

    @staticmethod
    def calculate_treatment_combinations(treatments_values: [[float]],
                                         treatment_combination: [float] = None
                                         ) -> [[float]]:
        all_combinations = []
        if treatment_combination is None:
            treatment_combination = []

        if len(treatments_values) > 1:
            current_treatment_values = treatments_values[:1][0]
            remaining_treatment_values = treatments_values[1:]
            for current_treatment_value in current_treatment_values:
                expanded_treatment_combination = treatment_combination + [current_treatment_value]
                c = CompleteRandomisedDesign.calculate_treatment_combinations(remaining_treatment_values,
                                                                              expanded_treatment_combination)
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

    @staticmethod
    def measure_treatment_combinations(treatments_combinations: [[float]],
                                       treatments_domain: [[float]],
                                       dp: [[int]],
                                       measurement_error_sd: [[float]],
                                       measurement_error_bias: [[float]]
                                       ) -> np.array:

        for treatments_combination in treatments_combinations:
            for treatment_index in range(len(treatments_combination)):
                current_domain = treatments_domain[treatment_index]
                measurement_dp = dp[treatment_index][0]
                measurement_sd = measurement_error_sd[treatment_index][0]
                measurement_error = stats.norm.rvs(loc=0, scale=measurement_sd, size=1)[0]
                measurement_bias = measurement_error_bias[treatment_index][0]
                treatments_combination[treatment_index] = \
                    np.round(treatments_combination[treatment_index] - measurement_bias - measurement_error,
                             measurement_dp)
                # if treatments_combination[treatment_index] < current_domain[0]:
                #     treatments_combination[treatment_index] = current_domain[0]
                # elif treatments_combination[treatment_index] > current_domain[1]:
                #     treatments_combination[treatment_index] = current_domain[1]

        return treatments_combinations

    def run_experiment(self) -> pd.DataFrame:
        raise NotImplementedError
