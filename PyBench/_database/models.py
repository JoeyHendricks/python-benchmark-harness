from sqlalchemy import MetaData, Table, Column, Integer, Float, String, Boolean


class TableModels(object):

    @staticmethod
    def c_profiler_statistics_data_model(test_case_name: str):
        """

        :param test_case_name:
        :return:
        """
        meta = MetaData()
        table = Table(
            test_case_name + "_c_profiler_statistics_data", meta,
            Column("uuid", String(99)),
            Column("test_id", Float),
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

    @staticmethod
    def boundary_test_report_model(test_case_name: str):
        """

        :param test_case_name:
        :return:
        """
        meta = MetaData()
        table = Table(
            test_case_name + "_boundary_test_report", meta,
            Column("uuid", String(99)),
            Column("test_id", Float),
            Column("boundary_name", String(99)),
            Column("value", Float),
            Column("minimum_boundary", Float),
            Column("maximum_boundary", Float),
            Column("minimum_verification_results", Boolean),
            Column("maximum_verification_results", Boolean)
        )
        return table

    @staticmethod
    def compare_test_report_model(test_case_name: str):
        """

        :param test_case_name:
        :return:
        """
        meta = MetaData()
        table = Table(
            test_case_name + "_boundary_test_report", meta,
            Column("uuid", String(99)),
            Column("test_id", Float),
            Column("critical_letter_rank", String(5)),
            Column("observed_letter_rank", String(5)),
            Column("critical_score", Float),
            Column("observed_score", Float),
            Column("letter_rank_comparison_result", Boolean),
            Column("score_comparison_result", Boolean)
        )
        return table

