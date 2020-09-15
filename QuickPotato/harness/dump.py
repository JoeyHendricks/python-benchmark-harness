from QuickPotato.database.actions import DatabaseActions
from datetime import datetime
import tempfile

DATABASE_ACTIONS = DatabaseActions()


def export_time_spent_statistics_to_csv(test_case_name, test_id, delimiter=",", path=None):
    """

    :return:
    """
    dataframe = DATABASE_ACTIONS.select_all_stacks(database_name=test_case_name, test_id=test_id)
    if path is None:
        path = tempfile.gettempdir() + "\\" if '\\' in tempfile.gettempdir() else "/"
        print(f"Saving export to {path}")

    if len(dataframe) > 0:
        dataframe.to_csv(
            path_or_buf=f"{path}raw_export_of_{test_id}_{str(datetime.now().timestamp())}.csv",
            sep=delimiter,
            index=False
        )
    else:
        raise NotImplementedError
