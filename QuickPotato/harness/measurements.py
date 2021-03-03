from QuickPotato.statistical.data import RawData


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
        raw_data = RawData(test_id, database_name)
        self.metric_average = raw_data.average_response_time
        self.metric_allowed_max_outlier = raw_data.maximum_outlier_in_response_times
        self.metric_allowed_min_outlier = raw_data.minimum_outlier_in_response_times
        self.metric_percentile_5th = raw_data.percentile_5th
        self.metric_percentile_10th = raw_data.percentile_10th
        self.metric_percentile_15th = raw_data.percentile_15th
        self.metric_percentile_20th = raw_data.percentile_20th
        self.metric_percentile_25th = raw_data.percentile_25th
        self.metric_percentile_30th = raw_data.percentile_30th
        self.metric_percentile_35th = raw_data.percentile_35th
        self.metric_percentile_40th = raw_data.percentile_40th
        self.metric_percentile_45th = raw_data.percentile_45th
        self.metric_percentile_50th = raw_data.percentile_50th
        self.metric_percentile_55th = raw_data.percentile_55th
        self.metric_percentile_60th = raw_data.percentile_60th
        self.metric_percentile_65th = raw_data.percentile_65th
        self.metric_percentile_70th = raw_data.percentile_70th
        self.metric_percentile_75th = raw_data.percentile_75th
        self.metric_percentile_80th = raw_data.percentile_80th
        self.metric_percentile_85th = raw_data.percentile_85th
        self.metric_percentile_90th = raw_data.percentile_90th
        self.metric_percentile_95th = raw_data.percentile_95th
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
