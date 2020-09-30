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
        database_name = self.test_case_name
        payload = self._build_payload()
        self.insert_boundaries_test_evidence(payload, database_name)
        return True


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
        database_name = self.test_case_name
        payload = self._build_payload()
        self.insert_regression_test_evidence(payload, database_name)
        return True
