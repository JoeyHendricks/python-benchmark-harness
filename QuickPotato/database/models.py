# coding=utf-8
from sqlalchemy import MetaData, Table, Column, Integer, Float, String


class RawResultsModels:

    @staticmethod
    def time_spent_model():
        meta = MetaData()
        table = Table(
            "time_spent_statistics", meta,
            Column('ID', Integer, primary_key=True),
            Column('test_id', String(99)),
            Column("test_case_name", String(999)),
            Column('uuid', String(99)),
            Column("name_of_method_under_test", String(999)),
            Column("epoch_datetime", Integer),
            Column("human_datetime", String(99)),
            Column("number_of_calls", String(99)),
            Column("response_time", Float),
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
            Column('ID', Integer, primary_key=True),
            Column('test_id', String(99)),
            Column("test_case_name", String(999)),
            Column('uuid', String(99)),
            Column("name_of_method_under_test", String(999)),
            Column("epoch_datetime", Integer),
            Column("human_datetime", String(99)),
            Column("percentage_of_system_cpu_usage", Float),
            Column("percentage_of_process_cpu_usage", Float),
        )
        return table


class UnitPerformanceTestResultsModels:

    @staticmethod
    def boundaries_test_report_model():
        meta = MetaData()
        table = Table(
            "boundaries_test_report", meta,
            Column('ID', Integer, primary_key=True),
            Column('test_id', String(99)),
            Column("test_case_name", String(999)),
            Column('status', String(99)),
            Column("verification_name", String(999)),
            Column("verification_status", String(99)),
            Column("metric", Float),
            Column("threshold", Float)
        )
        return table

    @staticmethod
    def regression_test_report_model():
        meta = MetaData()
        table = Table(
            "regression_test_report", meta,
            Column('ID', Integer, primary_key=True),
            Column('test_id', String(99)),
            Column("test_case_name", String(999)),
            Column('status', String(99)),
            Column('t_test_status', String(99)),
            Column('t_test_value', Float),
            Column('t_test_critical_value', Float),
            Column('f_test_status', String(99)),
            Column('f_test_value', Float),
            Column('f_test_critical_value', Float)
        )
        return table
