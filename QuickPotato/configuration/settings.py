

class Boundaries(object):

    def __init__(self):
        self.max_and_min_boundary_for_average = {"max": None, "min": None}
        self.max_and_min_boundary_for_largest_outlier = {"max": None, "min": None}
        self.max_and_min_boundary_for_percentile_5th = {"max": None, "min": None}
        self.max_and_min_boundary_for_percentile_10th = {"max": None, "min": None}
        self.max_and_min_boundary_for_percentile_15th = {"max": None, "min": None}
        self.max_and_min_boundary_for_percentile_20th = {"max": None, "min": None}
        self.max_and_min_boundary_for_percentile_25th = {"max": None, "min": None}
        self.max_and_min_boundary_for_percentile_30th = {"max": None, "min": None}
        self.max_and_min_boundary_for_percentile_35th = {"max": None, "min": None}
        self.max_and_min_boundary_for_percentile_40th = {"max": None, "min": None}
        self.max_and_min_boundary_for_percentile_45th = {"max": None, "min": None}
        self.max_and_min_boundary_for_percentile_50th = {"max": None, "min": None}
        self.max_and_min_boundary_for_percentile_55th = {"max": None, "min": None}
        self.max_and_min_boundary_for_percentile_60th = {"max": None, "min": None}
        self.max_and_min_boundary_for_percentile_65th = {"max": None, "min": None}
        self.max_and_min_boundary_for_percentile_70th = {"max": None, "min": None}
        self.max_and_min_boundary_for_percentile_75th = {"max": None, "min": None}
        self.max_and_min_boundary_for_percentile_80th = {"max": None, "min": None}
        self.max_and_min_boundary_for_percentile_85th = {"max": None, "min": None}
        self.max_and_min_boundary_for_percentile_90th = {"max": None, "min": None}
        self.max_and_min_boundary_for_percentile_95th = {"max": None, "min": None}

    @property
    def boundary_policy(self):
        return {
            "max_and_min_boundary_for_average": self.max_and_min_boundary_for_average,
            "max_and_min_boundary_for_largest_outlier": self.max_and_min_boundary_for_largest_outlier,
            "max_and_min_boundary_for_percentile_5th": self.max_and_min_boundary_for_percentile_5th,
            "max_and_min_boundary_for_percentile_10th": self.max_and_min_boundary_for_percentile_10th,
            "max_and_min_boundary_for_percentile_15th": self.max_and_min_boundary_for_percentile_15th,
            "max_and_min_boundary_for_percentile_20th": self.max_and_min_boundary_for_percentile_20th,
            "max_and_min_boundary_for_percentile_25th": self.max_and_min_boundary_for_percentile_25th,
            "max_and_min_boundary_for_percentile_30th": self.max_and_min_boundary_for_percentile_30th,
            "max_and_min_boundary_for_percentile_35th": self.max_and_min_boundary_for_percentile_35th,
            "max_and_min_boundary_for_percentile_40th": self.max_and_min_boundary_for_percentile_40th,
            "max_and_min_boundary_for_percentile_45th": self.max_and_min_boundary_for_percentile_45th,
            "max_and_min_boundary_for_percentile_50th": self.max_and_min_boundary_for_percentile_50th,
            "max_and_min_boundary_for_percentile_55th": self.max_and_min_boundary_for_percentile_55th,
            "max_and_min_boundary_for_percentile_60th": self.max_and_min_boundary_for_percentile_60th,
            "max_and_min_boundary_for_percentile_65th": self.max_and_min_boundary_for_percentile_65th,
            "max_and_min_boundary_for_percentile_70th": self.max_and_min_boundary_for_percentile_70th,
            "max_and_min_boundary_for_percentile_75th": self.max_and_min_boundary_for_percentile_75th,
            "max_and_min_boundary_for_percentile_80th": self.max_and_min_boundary_for_percentile_80th,
            "max_and_min_boundary_for_percentile_85th": self.max_and_min_boundary_for_percentile_85th,
            "max_and_min_boundary_for_percentile_90th": self.max_and_min_boundary_for_percentile_90th,
            "max_and_min_boundary_for_percentile_95th": self.max_and_min_boundary_for_percentile_95th,
        }

    @boundary_policy.setter
    def boundary_policy(self, new_policy):
        self.__dict__.update(new_policy)


class RegressionSettings(object):

    def __init__(self):
        self.run_t_test = True

    @property
    def regression_settings_policy(self):
        return {
            "run_t_test": self.run_t_test
        }

    @regression_settings_policy.setter
    def regression_settings_policy(self, new_policy):
        self.__dict__.update(new_policy)
