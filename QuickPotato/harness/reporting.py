from QuickPotato.database.actions import DatabaseActions


class BoundariesTestReport(DatabaseActions):

    def __init__(self):
        super(BoundariesTestReport, self).__init__()

        self.test_id = None
        self.test_case_name = None
        self.status = None
        self.verification_name = None
        self.verification_status = None
        self.metric = None
        self.threshold = None

    def _build_payload(self):
        """

        Returns
        -------

        """
        payload = {}
        for key, value in zip(self.__dict__.keys(), self.__dict__.values()):
            if value is not None:
                payload[key] = value

        return payload

    def save(self):
        """
        Will insert the test results into the database.

        Returns
        -------
        Will return True on success
        """
        table = self.boundaries_test_report_model()
        database_name = self.test_case_name
        payload = self._build_payload()

        if self.check_if_test_id_exists_in_test_report(self.test_id, table, database_name):
            self.update_boundaries_test_report(payload, self.test_id, database_name)

        else:
            self.insert_boundaries_test_report(payload, database_name)

        return True


class RegressionTestReport(DatabaseActions):

    def __init__(self):
        super(RegressionTestReport, self).__init__()

        self.test_id = None
        self.test_case_name = None
        self.status = None
        self.t_test_status = None
        self.t_test_value = None
        self.t_test_critical_value = None
        self.f_test_status = None
        self.f_test_value = None
        self.f_test_critical_value = None

    def _build_payload(self):
        """

        Returns
        -------

        """
        payload = {}
        for key, value in zip(self.__dict__.keys(), self.__dict__.values()):
            if value is not None:
                payload[key] = value

        return payload

    def save(self):
        """
        Will insert the test results into the database.

        Returns
        -------
        Will return True on success
        """
        table = self.regression_test_report_model()
        database_name = self.test_case_name
        payload = self._build_payload()

        if self.check_if_test_id_exists_in_test_report(self.test_id, table, database_name):
            self.update_regression_test_report(payload, self.test_id, database_name)

        else:
            self.insert_regression_test_report(payload, database_name)

        return True
