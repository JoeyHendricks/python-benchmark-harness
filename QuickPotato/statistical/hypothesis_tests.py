import numpy as np
from decimal import Decimal
from scipy import stats

# Silence Divided by zero warnings
np.seterr(divide='ignore')


class TTest:

    def __init__(self, baseline_measurements: list, benchmark_measurements: list) -> None:
        super(TTest, self).__init__()

        # Baseline calculations
        self.baseline_measurements = np.array(baseline_measurements)
        self.baseline_mean = np.mean(self.baseline_measurements)
        self.baseline_variance = np.var(self.baseline_measurements)
        self.baseline_number_of_samples = self.baseline_measurements.size

        # Benchmark calculations
        self.benchmark_measurements = np.array(benchmark_measurements)
        self.benchmark_mean = np.mean(self.benchmark_measurements)
        self.benchmark_variance = np.var(self.benchmark_measurements)
        self.benchmark_number_of_samples = self.benchmark_measurements.size

        # Information for test evidence report
        self.status = self._run_t_test()
        self.value = float(self.t_value)
        self.critical_value = float(self.critical_t_value)

    @property
    def results(self) -> bool:
        """

        Returns
        -------

        """
        return self.status

    @property
    def t_value(self) -> float:
        """

        Returns
        -------

        """
        if self._verify_both_arrays_for_zeros() is False:
            # both arrays contain zero's, calculation not possible.
            return 0

        signal = Decimal(self.benchmark_mean - self.baseline_mean)
        noise = Decimal((self.baseline_variance / self.baseline_number_of_samples) +
                        (self.benchmark_variance / self.benchmark_number_of_samples)).sqrt()

        if abs(signal / noise) == float("inf"):
            raise NotImplementedError

        else:
            return abs(signal / noise)

    @property
    def critical_t_value(self) -> float:
        """

        Returns
        -------

        """
        return stats.t.ppf(q=1-.05/2, df=self.baseline_number_of_samples-2)

    def _verify_both_arrays_for_zeros(self) -> bool:
        """

        Returns
        -------

        """
        if sum(self.baseline_measurements) == 0 and sum(self.benchmark_measurements) == 0:
            # There is no change both sums are equal to each other.
            return False

        else:
            # There is change valid input for T-test.
            return True

    def _run_t_test(self) -> bool:
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
