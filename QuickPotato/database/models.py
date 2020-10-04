from sqlalchemy import MetaData, Table, Column, Integer, Float, String, Boolean


class RawResultsModels(object):

    @staticmethod
    def time_spent_model():
        meta = MetaData()
        table = Table(
            "time_spent_statistics", meta,
            Column('id', Integer, primary_key=True),
            Column('test_id', String(99)),
            Column("test_case_name", String(999)),
            Column('uuid', String(99)),
            Column("name_of_method_under_test", String(999)),
            Column("epoch_timestamp", Integer),
            Column("human_timestamp", String(99)),
            Column("number_of_calls", String(99)),
            Column("overall_response_time", Float),
            Column("total_time", Float),
            Column("total_time_per_call", Float),
            Column("cumulative_time", Float),
            Column("cumulative_time_per_call", Float),
            Column("file", String(999)),
            Column("line_number", Integer),
            Column("function_name", String(999))
        )
        return table

    @staticmethod
    def system_resources_model():
        meta = MetaData()
        table = Table(
            "system_resources_statistics", meta,
            Column('id', Integer, primary_key=True),
            Column('test_id', String(99)),
            Column("test_case_name", String(999)),
            Column('uuid', String(99)),
            Column("name_of_method_under_test", String(999)),
            Column("epoch_timestamp", Integer),
            Column("human_timestamp", String(99)),
            Column("percentage_of_system_cpu_usage", Float),
            Column("percentage_of_process_cpu_usage", Float),
        )
        return table


class UnitPerformanceTestResultModels(object):

    @staticmethod
    def test_report_model():
        meta = MetaData()
        table = Table(
            "test_report", meta,
            Column('id', Integer, primary_key=True),
            Column('test_id', String(99)),
            Column("test_case_name", String(999)),
            Column("epoch_timestamp", Integer),
            Column("human_timestamp", String(99)),
            Column("status", Boolean),
            Column("boundaries_breached", Boolean),
            Column("regression_found", Boolean),
        )
        return table

    @staticmethod
    def boundaries_test_evidence_model():
        meta = MetaData()
        table = Table(
            "boundaries_test_evidence", meta,
            Column('id', Integer, primary_key=True),
            Column('test_id', String(99)),
            Column("test_case_name", String(999)),
            Column("epoch_timestamp", Integer),
            Column("human_timestamp", String(99)),
            Column("verification_name", String(999)),
            Column("status", Boolean),
            Column("value", Float),
            Column("boundary", Float)
        )
        return table

    @staticmethod
    def regression_test_evidence_model():
        meta = MetaData()
        table = Table(
            "regression_test_evidence", meta,
            Column('id', Integer, primary_key=True),
            Column('test_id', String(99)),
            Column("test_case_name", String(999)),
            Column("epoch_timestamp", Integer),
            Column("human_timestamp", String(99)),
            Column("verification_name", String(999)),
            Column("status", Boolean),
            Column("value", Float),
            Column("critical_value", Float)
        )
        return table
