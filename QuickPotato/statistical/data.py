from QuickPotato.database.crud import DatabaseOperations
import numpy as np


class RawData(DatabaseOperations):

    def __init__(self, test_id, database_name):
        super(RawData, self).__init__()

        self.test_id = test_id
        self.database_name = database_name
        self._response_times = self.select_end_to_end_response_times(self.database_name, self.test_id)
        self._cumulative_time_spent = self.select_cumulative_time(self.database_name, self.test_id)
    
    def response_times(self):
        """

        Returns
        -------

        """
        return self._response_times

    def normalized_response_times(self):
        """

        Returns
        -------

        """
        measurements = np.array(self._response_times)
        return measurements[abs(measurements - np.mean(measurements)) < 2 * np.std(measurements)]

    def cumulative_time_spent(self):
        """

        Returns
        -------

        """
        return self._cumulative_time_spent

    def average_response_time(self):
        """

        Returns
        -------

        """
        return sum(self._response_times) / len(self._response_times)

    def maximum_outlier_in_response_times(self):
        """

        Returns
        -------

        """
        return max(self._response_times)

    def minimum_outlier_in_response_times(self):
        """

        Returns
        -------

        """
        return min(self._response_times)

    def percentile_5th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 5)

    def percentile_10th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 10)

    def percentile_15th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 15)

    def percentile_20th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 20)

    def percentile_25th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 25)

    def percentile_30th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 30)

    def percentile_35th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 35)

    def percentile_40th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 40)

    def percentile_45th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 45)

    def percentile_50th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 50)

    def percentile_55th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 55)

    def percentile_60th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 60)

    def percentile_65th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 65)

    def percentile_70th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 70)

    def percentile_75th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 75)

    def percentile_80th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 80)

    def percentile_85th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 85)

    def percentile_90th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 90)

    def percentile_95th(self):
        """

        Returns
        -------

        """
        return np.percentile(np.array(self._response_times), 95)
