from QuickPotato.database.actions import DatabaseActions


class BoundariesTestEvidence(DatabaseActions):

    def __init__(self):
        super(BoundariesTestEvidence, self).__init__()

        self.test_id = None
        self.test_case_name = None
        self.epoch_timestamp = None
        self.human_timestamp = None
        self.verification_name = None
        self.status = None
        self.value = None
        self.boundary = None

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
        payload = self._build_payload()
        return self.insert_boundaries_test_evidence(self.test_case_name, payload)


class RegressionTestEvidence(DatabaseActions):

    def __init__(self):
        super(RegressionTestEvidence, self).__init__()

        self.test_id = None
        self.test_case_name = None
        self.epoch_timestamp = None
        self.human_timestamp = None
        self.verification_name = None
        self.status = None
        self.value = None
        self.critical_value = None

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

    def save_test_evidence(self):
        """
        Will insert the test results into the database.

        Returns
        -------
        Will return True on success
        """
        payload = self._build_payload()
        return self.insert_regression_test_evidence(self.test_case_name, payload)


class TestReport(DatabaseActions):

    def __init__(self):
        super(TestReport, self).__init__()

        self.test_id = None
        self.test_case_name = None
        self.epoch_timestamp = None
        self.human_timestamp = None
        self.status = None
        self.boundaries_breached = None
        self.regression_found = None

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
        payload = self._build_payload()
        if self.check_if_test_id_exists_in_test_report(self.test_case_name, self.test_id):

            # Update existing test results
            return self.update_results_in_test_report(self.test_case_name, self.test_id, payload)

        else:

            # Insert new test results
            return self.insert_results_into_test_report(self.test_case_name, payload)
