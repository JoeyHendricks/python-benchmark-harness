from QuickPotato.statistical.data import Statistics


class Metrics(object):

    def __init__(self):

        self.metric_average = None
        self.metric_allowed_max_outlier = None
        self.metric_allowed_min_outlier = None
        self.metric_percentile_5th = None
        self.metric_percentile_10th = None
        self.metric_percentile_15th = None
        self.metric_percentile_20th = None
        self.metric_percentile_25th = None
        self.metric_percentile_30th = None
        self.metric_percentile_35th = None
        self.metric_percentile_40th = None
        self.metric_percentile_45th = None
        self.metric_percentile_50th = None
        self.metric_percentile_55th = None
        self.metric_percentile_60th = None
        self.metric_percentile_65th = None
        self.metric_percentile_70th = None
        self.metric_percentile_75th = None
        self.metric_percentile_80th = None
        self.metric_percentile_85th = None
        self.metric_percentile_90th = None
        self.metric_percentile_95th = None

    def _collect_measurements(self, test_id, database_name):
        """

        Parameters
        ----------
        test_id
        database_name

        Returns
        -------

        """
        statistics = Statistics(test_id, database_name)
        self.metric_average = statistics.average_response_time
        self.metric_allowed_max_outlier = statistics.maximum_outlier_in_response_times
        self.metric_allowed_min_outlier = statistics.minimum_outlier_in_response_times
        self.metric_percentile_5th = statistics.percentile_5th
        self.metric_percentile_10th = statistics.percentile_10th
        self.metric_percentile_15th = statistics.percentile_15th
        self.metric_percentile_20th = statistics.percentile_20th
        self.metric_percentile_25th = statistics.percentile_25th
        self.metric_percentile_30th = statistics.percentile_30th
        self.metric_percentile_35th = statistics.percentile_35th
        self.metric_percentile_40th = statistics.percentile_40th
        self.metric_percentile_45th = statistics.percentile_45th
        self.metric_percentile_50th = statistics.percentile_50th
        self.metric_percentile_55th = statistics.percentile_55th
        self.metric_percentile_60th = statistics.percentile_60th
        self.metric_percentile_65th = statistics.percentile_65th
        self.metric_percentile_70th = statistics.percentile_70th
        self.metric_percentile_75th = statistics.percentile_75th
        self.metric_percentile_80th = statistics.percentile_80th
        self.metric_percentile_85th = statistics.percentile_85th
        self.metric_percentile_90th = statistics.percentile_90th
        self.metric_percentile_95th = statistics.percentile_95th
        return True

    @property
    def threshold_measurements(self):
        return {
            "metric_average": self.metric_average,
            "metric_allowed_max_outlier": self.metric_allowed_max_outlier,
            "metric_allowed_min_outlier": self.metric_allowed_min_outlier,
            "metric_percentile_5th": self.metric_percentile_5th,
            "metric_percentile_10th": self.metric_percentile_10th,
            "metric_percentile_15th": self.metric_percentile_15th,
            "metric_percentile_20th": self.metric_percentile_20th,
            "metric_percentile_25th": self.metric_percentile_25th,
            "metric_percentile_30th": self.metric_percentile_30th,
            "metric_percentile_35th": self.metric_percentile_35th,
            "metric_percentile_40th": self.metric_percentile_40th,
            "metric_percentile_45th": self.metric_percentile_45th,
            "metric_percentile_50th": self.metric_percentile_50th,
            "metric_percentile_55th": self.metric_percentile_55th,
            "metric_percentile_60th": self.metric_percentile_60th,
            "metric_percentile_65th": self.metric_percentile_65th,
            "metric_percentile_70th": self.metric_percentile_70th,
            "metric_percentile_75th": self.metric_percentile_75th,
            "metric_percentile_80th": self.metric_percentile_80th,
            "metric_percentile_85th": self.metric_percentile_85th,
            "metric_percentile_90th": self.metric_percentile_90th,
            "metric_percentile_95th": self.metric_percentile_95th,

        }
