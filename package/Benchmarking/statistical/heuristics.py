from scipy.stats import wasserstein_distance, ks_2samp
import pandas as pd
import numpy as np


class StatisticalDistanceTest:
    """
    This class is an algorithm that uses the kolmogorov smirnov statistics
    to define how much distance there is between a baseline and a benchmark
    test execution.

    To interpret how much distance is to much for us we use an heuristic
    to make sense of our statistics to make an best effort estimation
    if we tolerate a change or not.

    This is done by letter ranking the kolmogorov smirnov and Wasserstein
    distance statistic from the S to F (using the Japanese ranking system),
    alternatively a score from 0 to 100 can also be used or the distance
    value itself can also be used to interpret the results and make a quick
    decision whether to accept the change or refuse it.

    Using this approach to rapidly perform an baseline versus benchmark analysis
    we can fit this method into a CI/CD pipeline to be able to do a accurate
    performance analysis in an automated fashion.

    Keep in mind that this approach leans toward being a heuristic method because
    of the unpredictable nature of performance test results it is difficult
    to create a model that will fit a very wide array of test results.

    The models used in this class can there for be consider as a general guideline
    which can be adjusted to fit your own need.
    """
    SEED = 1996
    # The letter rank that interprets the wasserstein & kolmogorov smirnov distance.

    LETTER_RANK_DECISION_MATRIX = [

        {"wasserstein_boundary": 0.030, "kolmogorov_smirnov_boundary": 0.300, "rank": "S"},
        {"wasserstein_boundary": 0.060, "kolmogorov_smirnov_boundary": 0.600, "rank": "A"},
        {"wasserstein_boundary": 0.100, "kolmogorov_smirnov_boundary": 0.700, "rank": "B"},
        {"wasserstein_boundary": 0.125, "kolmogorov_smirnov_boundary": 0.800, "rank": "C"},
        {"wasserstein_boundary": 0.150, "kolmogorov_smirnov_boundary": 1.000, "rank": "D"},
        {"wasserstein_boundary": 0.200, "kolmogorov_smirnov_boundary": 1.200, "rank": "E"},
        {"wasserstein_boundary": 0.250, "kolmogorov_smirnov_boundary": 1.400, "rank": "F"},

    ]

    def __init__(self, population_a: list, population_b: list) -> None:
        """
        Will construct the class and calculate all the required statistics.
        After all of the computation have been completed the following information can then
        be extracted from this class:

        :param population_a: An list of floats of the A population (baseline).
        :param population_b: An list of floats of the B population (benchmark).
        """

        # Building scoring matrix
        self._wasserstein_lowest_boundary = 0.010
        self._kolmogorov_smirnov_lowest_boundary = 0.200
        self._matrix_size = 100
        self._boundary_increment = 0.010
        self.SCORING_MATRIX = self._generate_scoring_matrix()

        # Calculate statistics
        self.sample_size = min([len(population_a), len(population_b)])
        self.sample_a = self._calculate_empirical_cumulative_distribution_function(population_a)
        self.sample_b = self._calculate_empirical_cumulative_distribution_function(population_b)
        self._ws_d_value = self._calculate_wasserstein_distance_statistics()
        self._ks_d_value, self._ks_p_value = self._calculate_kolmogorov_smirnov_distance_statistics()
        self.letter_rank = self._letter_rank_distance_statistics()
        self.score = self._score_distance_statistics()

    @property
    def wasserstein_distance(self) -> float:
        """
        Gives the computed value of distance from sample a versus sample b.
        This value represent how much effort there is required to move the
        distribution of sample a toward b.

        More information about this metric can be found here:

        https://en.wikipedia.org/wiki/Wasserstein_metric

        :return: The wasserstein distance as rounded float
        until the third decimal.
        """
        return self._ws_d_value

    @property
    def kolmogorov_smirnov_distance(self) -> float:
        """
        Computes the absolute distance between 2 distribution representing
        the maximum distance between sample A and B.

        More information about this metric can be found here:

        https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test

        :return: The kolmogorov smirnov distance as rounded float
        until the third decimal.
        """
        return self._ks_d_value

    @property
    def kolmogorov_smirnov_probability(self) -> float:
        """
        Not used in any of the calculation in this heuristic but it might be helpful
        for engineers that also want to perform a official KS-test on their data
        to verify if the change is statistically relevant.

        More info on probability value's:

        https://en.wikipedia.org/wiki/P-value

        :return: The kolmogorov smirnov probability value
        """
        return self._ks_p_value

    @staticmethod
    def normalize_raw_data(raw_data: object) -> list:
        """
        Will normalize a given raw distribution to its maximum.
        :return:
        """
        return (np.array(raw_data) - np.array(raw_data).mean()) / np.array(raw_data).std()

    def _generate_scoring_matrix(self) -> list:
        """

        :return:
        """
        # Building predictive dirichlet scoring matrix using seed 1996
        np.random.seed(self.SEED)
        dirichlet_distribution = np.random.dirichlet(alpha=np.ones(self._matrix_size), size=1)[0]
        dirichlet_distribution.sort()

        # Generating scoring grid
        wst_start_val = self._wasserstein_lowest_boundary
        ks_start_val = self._kolmogorov_smirnov_lowest_boundary
        scoring_matrix = []
        for punishment in dirichlet_distribution:
            scoring_matrix.append(
                {
                    "wasserstein_boundary": wst_start_val,
                    "kolmogorov_smirnov_boundary": ks_start_val,
                    "punishment": punishment
                }
            )
            wst_start_val += self._boundary_increment
            ks_start_val += self._boundary_increment

        return scoring_matrix

    def _calculate_empirical_cumulative_distribution_function(self, population: list) -> object:
        """
        Will calculate the eCDF to find the empirical distribution of our population.
        This function will then create a dataframe which will contain the measure
        and its probability.

        Further more this function also gives the option to filter out the outliers
        on the extreme ends of our new distribution.
        More info about empirical cumulative distribution functions can be found here:

        https://en.wikipedia.org/wiki/Empirical_distribution_function

        :param population: The provided measurements from one collected population.
        :return: The empirical cumulative distribution function (outliers filtered or not filtered)
        """
        normalized_sample = self.normalize_raw_data(population)
        sample = pd.DataFrame(
            {
                'measure': np.sort(normalized_sample),
                'probability': np.arange(len(normalized_sample)) / float(len(normalized_sample)),
            }
        )
        sample = sample[~(sample['probability'] >= 0.99)]
        return sample

    def _calculate_wasserstein_distance_statistics(self) -> float:
        """
        Computes the Wasserstein distance or Kantorovich–Rubinstein metric also known
        as the Earth mover's distance. This metric represents how much effort is needed
        to move the benchmark distribution towards the baseline.

        :return: Will return the Wasserstein metric as a float from a normalized distribution.
        """
        wasserstein = wasserstein_distance(
            self.sample_a["measure"].values,
            self.sample_b["measure"].values
        )
        return round(wasserstein, 3)

    def _calculate_kolmogorov_smirnov_distance_statistics(self) -> tuple:
        """
        Will use the kolmogorov smirnov statistical test to calculate the
        distance between two ECDF distributions. The KS test measures how
        significant the change is between the 2 largest points.

        :return: Gives back the KS-test D-value & the P-Value
        """
        kolmogorov_smirnov_distance, kolmogorov_smirnov_probability = ks_2samp(
            self.sample_a["measure"].values,
            self.sample_b["measure"].values
        )
        return round(kolmogorov_smirnov_distance, 3), kolmogorov_smirnov_probability

    def _determine_population_direction(self) -> str:
        """
        Will determine if the population has increased in latency or
        if the population has decreased in latency.

        This increase or decrease indicated with either a + or - after
        the letter rank.
        :return: A string that is either + or -
        """
        if np.median(self.sample_a["measure"].values) > np.median(self.sample_b["measure"].values):
            return "-"  # slower

        else:
            return "+"  # faster

    def _score_distance_statistics(self) -> float:
        """
        An heuristic that will estimate a score between 0 - 100 using the
        Wasserstein distance and the kolmogorov smirnov distance.
        It determines the distance by using defined boundaries to lower the score
        if they are breached.

        Allowing for an more accurate threshold that can
        be used to decide if the change acceptable or not.

        :return: A score from 0 - 100 which can be interpret by a engineer.
        """
        ks_score = 1
        ws_score = 1
        for boundary in self.SCORING_MATRIX:
            if self._ws_d_value >= boundary["wasserstein_boundary"]:
                ws_score -= boundary["punishment"]

            if self._ks_d_value >= boundary["kolmogorov_smirnov_boundary"]:
                ks_score -= boundary["punishment"]
        return abs(round(float(ks_score + ws_score) / 2 * 100, 2))

    def _letter_rank_distance_statistics(self) -> str:
        """
        An heuristic that will estimate a rank of what the amount of change is
        between our distributions. This rank is based on the Japanese letter
        ranking system the letters can be interpreted the following way:


        |  Rank |        Severity       |             Action              |
        |-------|-----------------------|---------------------------------|
        |   S   | Almost None           | Automated release to production |
        |   A   | Very low              | Automated release to production |
        |   B   | Low                   | Pending impact analysis needed  |
        |   C   | Medium                | Halt create minor defect        |
        |   D   | High                  | Halt create medium defect       |
        |   E   | Very High             | Halt create major defect        |
        |   F   | Significant change    | Halt create Priority defect     |
        |-------|-----------------------|---------------------------------|

        Depending on your situation it is fine to also automatically release
        to production when a B rank is produced as the impact is low.
        If you choose to do that I would recommend to also create a defect
        to document the automated release with an low performance risk.

        :return: The letter rank in the form as string ranging from S to F
        """
        for grade in self.LETTER_RANK_DECISION_MATRIX:
            ks_critical_grade = grade["kolmogorov_smirnov_boundary"]
            wasserstein_critical_grade = grade["wasserstein_boundary"]
            if self._ws_d_value < wasserstein_critical_grade and self._ks_d_value < ks_critical_grade:
                return f"{grade['rank'] + self._determine_population_direction()}"
            else:
                continue
        return f"F{self._determine_population_direction()}"
