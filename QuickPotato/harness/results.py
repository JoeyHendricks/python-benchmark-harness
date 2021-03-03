from QuickPotato.database.queries import Crud


class BoundariesTestEvidence(Crud):

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

    def save(self):
        """
        Will insert the test results into the database.

        Returns
        -------
        Will return True on success
        """
        payload = {
            "test_id": self.test_id,
            "test_case_name": self.test_case_name,
            "epoch_timestamp": self.epoch_timestamp,
            "human_timestamp": self.human_timestamp,
            "verification_name": self.verification_name,
            "status": self.status,
            "value": self.value,
            "boundary": self.boundary
        }
        return self.insert_boundaries_test_evidence(self.test_case_name, payload)


class RegressionTestEvidence(Crud):

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

    def save_test_evidence(self):
        """
        Will insert the test results into the database.

        Returns
        -------
        Will return True on success
        """
        payload = {
            "test_id": self.test_id,
            "test_case_name": self.test_case_name,
            "epoch_timestamp": self.epoch_timestamp,
            "human_timestamp": self.human_timestamp,
            "verification_name": self.verification_name,
            "status": self.status,
            "value": self.value,
            "critical_value": self.critical_value
        }
        return self.insert_regression_test_evidence(self.test_case_name, payload)


class TestReport(Crud):

    def __init__(self):
        super(TestReport, self).__init__()

        self.test_id = None
        self.test_case_name = None
        self.epoch_timestamp = None
        self.human_timestamp = None
        self.status = None
        self.boundaries_breached = None
        self.regression_found = None

    def save(self):
        """
        Will insert the test results into the database.

        Returns
        -------
        Will return True on success
        """
        payload = {
            "test_id": self.test_id,
            "test_case_name": self.test_case_name,
            "epoch_timestamp": self.epoch_timestamp,
            "human_timestamp": self.human_timestamp,
            "status": self.status,
            "boundaries_breached": self.boundaries_breached,
            "regression_found": self.regression_found
        }
        if self.check_if_test_id_exists_in_test_report(self.test_case_name, self.test_id):

            # Update existing test results
            return self.update_results_in_test_report(self.test_case_name, self.test_id, payload)

        else:

            # Insert new test results
            return self.insert_results_into_test_report(self.test_case_name, payload)
