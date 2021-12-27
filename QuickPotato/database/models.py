from sqlalchemy import MetaData, Table, Column, Integer, Float, String, Boolean


class StatisticsModels(object):

    @staticmethod
    def c_profiler_statistics_data_model(test_case_name):
        meta = MetaData()
        table = Table(
            test_case_name + "_c_profiler_statistics_data", meta,
            Column('uuid', String(99)),
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


class TestResultModels(object):

    @staticmethod
    def test_report_model(test_case_name):
        meta = MetaData()
        table = Table(
            test_case_name + "_test_report", meta,
            Column('uuid', String(99)),
            Column('test_id', String(99)),
            Column("test_case_name", String(999)),
            Column("epoch_timestamp", Integer),
            Column("human_timestamp", String(99)),
            Column("status", Boolean),
            Column("boundaries_breached", Boolean),
            Column("regression_found", Boolean),
        )
        return table


