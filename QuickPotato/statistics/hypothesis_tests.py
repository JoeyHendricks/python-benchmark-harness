from QuickPotato.utilities.decorators import *
import numpy as np
from math import sqrt
from decimal import *
from scipy import stats

# Silence Divided by zero warnings
np.seterr(divide='ignore')


class TTest:

    def __init__(self, test_id, test_case_name, baseline_measurements, benchmark_measurements):

        # meta data
        self.test_id = test_id
        self.test_case_name = test_case_name

        # baseline calculations
        self.baseline_measurements = np.array(baseline_measurements)
        self.baseline_mean = np.mean(self.baseline_measurements)
        self.baseline_variance = np.var(self.baseline_measurements)
        self.baseline_number_of_samples = self.baseline_measurements.size

        # benchmark calculations
        self.benchmark_measurements = np.array(benchmark_measurements)
        self.benchmark_mean = np.mean(self.benchmark_measurements)
        self.benchmark_variance = np.var(self.benchmark_measurements)
        self.benchmark_number_of_samples = self.benchmark_measurements.size

    @property
    def results(self):
        """

        Returns
        -------

        """
        return self.run_t_test()

    @property
    def t_value(self):
        """

        Returns
        -------

        """
        signal = Decimal(self.benchmark_mean - self.baseline_mean)
        noise = Decimal((self.baseline_variance / self.baseline_number_of_samples) +
                        (self.benchmark_variance / self.benchmark_number_of_samples)).sqrt()

        if abs(signal / noise) == float("inf"):
            raise NotImplementedError

        else:
            return abs(signal / noise)

    @property
    def critical_t_value(self):
        """

        Returns
        -------

        """
        return stats.t.ppf(q=1-.05/2, df=self.baseline_number_of_samples-2)

    @save_evidence_test_report
    def run_t_test(self):
        """

        Returns
        -------

        """
        if self.t_value > self.critical_t_value:
            # We can reject the null hypothesis
            # the test is slower or faster than the baseline
            return False
        else:
            # We can NOT reject the null hypothesis
            # the test is NOT slower or faster than the baseline
            return True


class FTest:

    def __init__(self, test_id, test_case_name, baseline_measurements, benchmark_measurements):

        # meta data
        self.test_id = test_id
        self.test_case_name = test_case_name

        # baseline calculations
        self.baseline_measurements = np.array(baseline_measurements)
        self.baseline_variance = 0.0 if sum(self.baseline_measurements) == 0 else np.var(self.baseline_measurements)
        self.baseline_number_of_samples = self.baseline_measurements.size

        # benchmark calculations
        self.benchmark_measurements = np.array(benchmark_measurements)
        self.benchmark_variance = 0.0 if sum(self.benchmark_measurements) == 0 else np.var(self.benchmark_measurements)
        self.benchmark_number_of_samples = self.benchmark_measurements.size

    @property
    def results(self):
        return self.run_f_test()

    @property
    def f_value(self):
        """

        Returns
        -------

        """
        if self.baseline_variance == 0 and self.benchmark_variance == 0:
            # It is possible that both numbers are zero
            # and that a double scalar  error is thrown
            return 0

        elif abs(self.baseline_variance / self.benchmark_variance) == float("inf"):
            raise NotImplementedError

        else:
            return abs(self.baseline_variance / self.benchmark_variance)

    @property
    def critical_f_value(self):
        """

        Returns
        -------

        """
        return stats.f.ppf(q=1-0.05, dfn=self.benchmark_number_of_samples - 1,
                           dfd=self.benchmark_number_of_samples - 1)

    @save_evidence_test_report
    def run_f_test(self):
        """

        Returns
        -------

        """
        if self.f_value > self.critical_f_value:
            # We can reject the null hypothesis
            # the test is slower or faster than the baseline
            return False
        else:
            # We can NOT reject the null hypothesis
            # the test is NOT slower or faster than the baseline
            return True
