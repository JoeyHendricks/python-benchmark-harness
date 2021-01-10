from sqlalchemy import MetaData, Table, Column, Integer, Float, String, Boolean


class RawStatisticsSchemas(object):

    @staticmethod
    def performance_statistics_schema():
        meta = MetaData()
        table = Table(
            "performance_statistics", meta,
            Column('id', Integer, primary_key=True),
            Column('test_id', String(99)),
            Column("test_case_name", String(999)),
            Column('sample_id', String(99)),
            Column("name_of_method_under_test", String(999)),
            Column("epoch_timestamp", Integer),
            Column("human_timestamp", String(99)),
            Column("child_path", String(999)),
            Column("child_line_number", Integer),
            Column("child_function_name", String(999)),
            Column("parent_path", String(999)),
            Column("parent_line_number", Integer),
            Column("parent_function_name", String(999)),
            Column("number_of_calls", String(99)),
            Column("total_time", Float),
            Column("cumulative_time", Float),
            Column("total_response_time", Float),
        )
        return table


class UnitPerformanceTestResultSchemas(object):

    @staticmethod
    def test_report_schema():
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
    def boundaries_test_evidence_schema():
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
    def regression_test_evidence_schema():
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
