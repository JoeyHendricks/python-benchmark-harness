from plotly.subplots import make_subplots
import plotly.graph_objects as go
import os


class ScatterPlot:

    def __init__(self, scenario, rank, score, change):
        """
        will build a scatter plot image
        :param scenario:
        :param rank:
        :param change:
        """
        self.scenario = scenario
        self.rank = rank
        self.score = score
        self.change = change

    def _render_figure(self):
        """
        Will render the data into a figure.
        :return:
        """
        figure = make_subplots(rows=1, cols=2)
        figure.add_trace(
            go.Scatter(x=self.scenario.benchmark_x, y=self.scenario.benchmark_y,
                       mode='markers', name="benchmark"
                       ),
            row=1,
            col=1
        )

        figure.add_trace(
            go.Scatter(x=self.scenario.baseline_x, y=self.scenario.baseline_y,
                       mode='markers', name="baseline"
                       ),
            row=1,
            col=2,
        )
        figure.update_layout(
            height=800, width=1200,
            title_text=f"Benchmark Vs Baseline, scored: <b>{self.score}</b>",
        )
        figure.update_yaxes(type="log", range=[-2.5, 2.5], title_text="Response Time in Seconds (logarithmic scale)")
        figure.update_xaxes(title_text="Epoch Time Stamps")
        return figure

    def show(self) -> None:
        """
        Will display the image in your default browser.
        """
        figure = self._render_figure()
        figure.show()

    def save_frame(self, folder: str, filename: str, image_format=".png") -> None:
        """
        Saving image using the orca engine the default
        kaleido engine was not working for me.
        :param image_format : The format of the image
        :param folder: target folder on disk
        :param filename: the file name;
        """
        figure = self._render_figure()
        if not os.path.exists(folder):
            os.mkdir(folder)

        figure.write_image(
            file=f"{str(folder)}\\{str(filename)}{str(image_format)}",
            format=image_format.strip("."),
            engine="orca"
        )
