from typing import Type, Dict, Any, Union

import numpy as np
import pandas as pd
import scipy.stats as stats


class Combinatorics:
    @staticmethod
    def calculate_combinations(factors_values: [[float]]
                               , factor_combination: [float] = None
                               ) -> [[float]]:
        all_combinations = []
        if factor_combination is None:
            factor_combination = []

        if len(factors_values) > 1:
            current_factor_values = factors_values[:1][0]
            remaining_factor_values = factors_values[1:]
            for current_factor_value in current_factor_values:
                expanded_factor_combination = factor_combination + [current_factor_value]
                c = Combinatorics.calculate_combinations(remaining_factor_values,
                                                         expanded_factor_combination)
                for combination in c:
                    all_combinations.append(combination)
        else:
            c = []
            current_factor_values = factors_values[0]
            for factor_value in current_factor_values:
                combination = factor_combination + [factor_value]
                c.append(combination)
            return c

        return all_combinations


class ObservationUnitModel:
    pass


class ExperimentalUnitModel:
    def __init__(self
                 , observation_units: [ObservationUnitModel]):
        self.observation_units = observation_units


class LinearExperimentalUnitModel(ExperimentalUnitModel):
    def __init__(self
                 , responses_mean: [[float]]
                 , responses_sd: [[float]]
                 , responses_gradient: [[float]]
                 , responses_gradient_sd: [[float]]
                 , observation_units: [ObservationUnitModel]):
        super().__init__(observation_units)


class Experiment:
    @staticmethod
    def calculate_factor_levels(domains: [[(float, float)]],
                                domain_fractions: [[float]]
                                ) -> [[float]]:
        factors_levels = []
        for domain_index in range(len(domains)):
            domain = domains[domain_index]
            domain_width = domain[1] - domain[0]
            fractional_levels = domain_fractions[domain_index]
            factor_levels = []
            for fractional_level in fractional_levels:
                factor_level = domain[0] + fractional_level * domain_width
                factor_levels.append(factor_level)
            factors_levels.append(factor_levels)

        return factors_levels

    @staticmethod
    def calculate_true_values(measured_combinations_values: [[float]],
                              domain_values: [[float]],
                              is_domain_boundaries: [[bool]],
                              dp: [[int]],
                              measurement_error_sd: [[float]],
                              measurement_error_bias: [[float]]
                              ) -> np.array:

        true_combinations_values = []
        for measured_combination in measured_combinations_values:
            true_combination_values = []
            for factor_index in range(len(measured_combination)):
                domain = domain_values[factor_index]
                is_domain_boundary = is_domain_boundaries[factor_index]
                is_left_boundary = is_domain_boundary[0]
                is_right_boundary = is_domain_boundary[1]
                measurement_dp = dp[factor_index][0]
                measurement_sd = measurement_error_sd[factor_index][0]
                measurement_error = stats.norm.rvs(loc=0, scale=measurement_sd, size=1)[0]
                measurement_bias = measurement_error_bias[factor_index][0]

                measured_factor_value = measured_combination[factor_index]
                true_factor_value = measured_factor_value - measurement_bias - measurement_error

                if is_left_boundary:
                    if true_factor_value < domain[0]:
                        true_factor_value = domain[0]
                if is_right_boundary:
                    if true_factor_value > domain[1]:
                        true_factor_value = domain[1]

                true_factor_value = np.round(true_factor_value, measurement_dp)
                true_combination_values.append(true_factor_value)
            true_combinations_values.append(true_combination_values)

        return true_combinations_values


class CompleteRandomisedDesign(Experiment):
    def __init__(self, factor_domain_values: [(float, float)]
                 , factors_domain_boundaries: [bool]
                 , factors_increments: [float]
                 , factors_dp: [int]
                 , factors_measurement_error_sd: [float]
                 , factors_measurement_error_bias: [float]
                 , number_of_replications=1):
        number_of_factors = 1  # > 1 in full factorial designs
        self.true_factors_levels = []

        self.measured_level_values = Experiment.calculate_factor_levels([factor_domain_values]
                                                                        , [factors_increments])
        number_of_levels = len(self.measured_level_values[0])

        self.measured_factors_levels = Combinatorics.calculate_combinations(self.measured_level_values)
        for replication in range(number_of_replications):
            true_factors_levels = Experiment.calculate_true_values(self.measured_factors_levels,
                                                                   [factor_domain_values],
                                                                   [factors_domain_boundaries],
                                                                   [factors_dp],
                                                                   [factors_measurement_error_sd],
                                                                   [factors_measurement_error_bias])
            true_factors_levels = [[(self.measured_factors_levels[row][col], true_factors_levels[row][col])]
                                   for row in range(number_of_levels)
                                   for col in range(number_of_factors)]
            self.true_factors_levels.append(true_factors_levels)

        self.run_sequence = [(replication, level) for replication in range(number_of_replications)
                             for level in range(number_of_levels)]
        np.random.shuffle(self.run_sequence)

    def run_experiment(self) -> pd.DataFrame:
        raise NotImplementedError
