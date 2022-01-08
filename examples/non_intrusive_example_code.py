import math
import random
import numpy as np


class FancyCode:

    SAMPLE_SIZE = 20000

    def __init__(self, use_slow_method=False, use_fast_method=False):
        """
        Used to control_the_speed of the object.
        :param use_slow_method: will slow down the object
        :param use_fast_method:  Will add a method but now slow it down
        """
        self.use_slow_method, self.use_fast_method = use_slow_method, use_fast_method

    @staticmethod
    def slow_method():
        num = 6 ** 6 ** 6
        return len(str(num))

    @staticmethod
    def fast_method():
        num = 6 ** 6 ** 6
        return int(math.log10(num))

    def _generate_fancy_numbers(self):
        """
        Will give back a random fancy number
        """
        for _ in range(0, self.SAMPLE_SIZE):
            yield float(random.random())

    def _create_fancy_population(self) -> list:
        """
        Will create a fancy population.
        :return: returns a list containing the population.
        """
        return [number for number in self._generate_fancy_numbers()]

    def calculate_statistics_about_fancy_population(self):
        """

        :return:
        """
        if self.use_slow_method:
            self.slow_method()

        elif self.use_fast_method:
            self.fast_method()

        return {
            "median": np.median(self._create_fancy_population()),
            "standard_deviation": np.std(self._create_fancy_population()),
            "variance": np.var(self._create_fancy_population())
        }


