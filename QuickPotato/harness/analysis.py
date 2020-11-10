from QuickPotato.visualization.flame_graphs import FlameGraphGenerator
from QuickPotato.database.crud import DatabaseOperations
from QuickPotato.utilities.html_templates import *
from jinja2 import Template
from datetime import datetime


class FlameGraphs(DatabaseOperations):

    def __init__(self, test_case_name, filter_external_libraries=False, filter_builtin=False):
        super(FlameGraphs, self).__init__()

        self.test_case_name = test_case_name
        self.filter_external_libraries = filter_external_libraries
        self.filter_builtin = filter_builtin

    def _generate_flame_graph(self, sample_id):
        """

        :param sample_id:
        :return:
        """
        return FlameGraphGenerator(
            self.test_case_name,
            sample_id,
            self.filter_external_libraries,
            self.filter_builtin
        ).svg_flame_graph

    def _write_html_to_file(self, html, path):
        """

        :param html:
        :param path:
        :return:
        """
        name = f"{self.test_case_name}-{datetime.now().timestamp()}"
        with open(f"{path}{name}.html", 'a') as file:
            file.write(html)

    def _collect_benchmark_and_baseline_flame_graphs(self, benchmark_meta_data, baseline_meta_data):
        """

        :param benchmark_meta_data:
        :param baseline_meta_data:
        :return:
        """
        rendered_benchmark_flame_graphs = []
        rendered_baseline_flame_graphs = []

        for benchmark_data, baseline_data in zip(benchmark_meta_data, baseline_meta_data):

            # collect benchmark and baseline flame graph
            benchmark_flame_graph = self._generate_flame_graph(benchmark_data["sample_id"])
            baseline_flame_graph = self._generate_flame_graph(baseline_data["sample_id"])

            # Add flame graphs to their lists
            rendered_benchmark_flame_graphs.append(benchmark_flame_graph)
            rendered_baseline_flame_graphs.append(baseline_flame_graph)

        return rendered_benchmark_flame_graphs, rendered_baseline_flame_graphs

    def export_flame_graph_comparison(self, benchmark_test_id, baseline_test_id, path):
        """

        :param benchmark_test_id:
        :param baseline_test_id:
        :param path:
        :return:
        """
        benchmark_rendered_flame_graphs = []
        baseline_rendered_flame_graphs = []

        # Collecting benchmark and baseline meta data (Sample ID, Name, Response time and timestamps)
        benchmark_meta_data = self.select_all_meta_data(self.test_case_name, benchmark_test_id)
        baseline_meta_data = self.select_all_meta_data(self.test_case_name, baseline_test_id)

        # Render flame graphs
        for benchmark_data, baseline_data in zip(benchmark_meta_data, baseline_meta_data):

            # collect benchmark and baseline flame graph
            benchmark_flame_graph = self._generate_flame_graph(benchmark_data["sample_id"])
            baseline_flame_graph = self._generate_flame_graph(baseline_data["sample_id"])

            # Add flame graphs to lists
            benchmark_rendered_flame_graphs.append(benchmark_flame_graph)
            baseline_rendered_flame_graphs.append(baseline_flame_graph)

        # Render HTML template using jinja2
        template = Template(html_template_flame_graph_comparison)
        html = template.render(
            benchmark_test_id=benchmark_test_id,
            baseline_test_id=baseline_test_id,
            benchmark_meta_data=benchmark_meta_data,
            baseline_meta_data=baseline_meta_data,
            zipped_benchmark_data=zip(benchmark_meta_data, benchmark_rendered_flame_graphs),
            zipped_baseline_data=zip(baseline_meta_data, baseline_rendered_flame_graphs)
        )
        self._write_html_to_file(html, path)

    def export_flame_graph(self, test_id, path):
        """

        :param test_id:
        :param path:
        :return:
        """
        rendered_flame_graphs = []

        # Collecting test id meta data (Sample ID, Name, Response time and timestamps)
        meta_data = self.select_all_meta_data(self.test_case_name, test_id)

        # Render flame graphs
        for data in meta_data:
            rendered_flame_graphs.append(self._generate_flame_graph(data["sample_id"]))

        # Render HTML template using jinja2
        template = Template(html_template_single_flame_graph)
        html = template.render(
            test_id=test_id,
            meta_data=meta_data,
            zipped_data=zip(meta_data, rendered_flame_graphs)
        )
        self._write_html_to_file(html, path)
