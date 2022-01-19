from .._utilities.exceptions import UnableToGenerateVisualizations, UnableToExportVisualization
from .._database.collection import Crud
from datetime import datetime
import plotly.graph_objects as go
import pandas as pd
import os


class BarChart(Crud):

    def __init__(self, test_case_name: str, database_connection_url: str, test_ids=None, order_by="latency") -> None:
        """

        :param test_case_name:
        :param database_connection_url:
        :param test_ids:
        :param order_by:
        """
        super(BarChart, self).__init__()

        # Sorting out the test-id's
        self.test_case_name = test_case_name
        self.database_name = database_connection_url
        self._order_by = order_by
        if test_ids is None or type(test_ids) is not list:
            raise UnableToGenerateVisualizations()

        else:
            self.list_of_test_ids = test_ids

        # Gathering relevant performance metrics
        self.statistics = {}
        for tid in self.list_of_test_ids:
            self.statistics[tid] = self.select_benchmark_call_stack_by_test_id(
                url=database_connection_url,
                tcn=test_case_name,
                test_id=tid
            )

        self.json = self.generate_json()

    def generate_json(self) -> list:
        """

        :return:
        """
        payload = []
        for tid in self.list_of_test_ids:
            for row in self.statistics[tid]:

                if row['parent_function_name'] == row['sample_id']:
                    method_signature = row['child_function_name']

                else:
                    method_signature = f"{row['parent_function_name']}/{row['child_function_name']}"

                payload.append(
                    {
                        "sample_id": row['sample_id'],
                        "test_id": tid,
                        "method_signature": method_signature,
                        "latency": row['cumulative_time']
                    }
                )
        return sorted(payload, key=lambda k: k[self._order_by], reverse=True)

    def render_html(self) -> str:
        """

        :return:
        """
        df = pd.DataFrame(self.json)
        fig = go.Figure()
        fig.update_layout(
            title="<span style='font-size: 22px;'>Benchmarking Method Performance Bar Chart</span>",
            template="ggplot2",
            xaxis=dict(title_text="Test-id's"),
            yaxis=dict(title_text="Time spent in seconds"),
            barmode="stack",
            font=dict(
                size=12,
            )
        )
        for method_signature in df.method_signature.unique():
            plot_df = df[df.method_signature == method_signature]
            fig.add_trace(
                go.Bar(
                    x=[plot_df.test_id, plot_df.sample_id],
                    y=plot_df.latency,
                    name=method_signature,
                    meta=[method_signature],
                    hovertemplate='<br>Test-ID: %{x[0]}</b>'
                    '<br>Sample-ID: %{x[1]}</b>'
                    '<br>method name: %{meta[0]}</b>' +
                    '<br>Time Spent %{y}</b>' +
                    '<extra></extra>'
                ),
            )
        return fig.to_html(config={"displaylogo": False})

    def export(self, path: str) -> None:
        """
        Export the bar chart as a HTML report on disk.
        :param path: The path on disk where the file needs to be written.
                     Example: C:\\temp\\
        """
        if os.path.isdir(path):
            name = f"BarChart-{self.test_case_name}-{datetime.now().timestamp()}"
            with open(f"{path}{name}.html", 'a') as file:
                file.write(self.render_html())
        else:
            raise UnableToExportVisualization()
