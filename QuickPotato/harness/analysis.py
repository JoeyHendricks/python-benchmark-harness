from QuickPotato.visualization.flame_graphs import FlameGraphGenerator
from QuickPotato.database.crud import DatabaseOperations
from QuickPotato.utilities.html_templates import *
from QuickPotato.utilities.defaults import default_test_case_name
from jinja2 import Template
from datetime import datetime


class FlameGraphs(DatabaseOperations):

    def __init__(self, test_case_name=default_test_case_name, filter_external_libraries=False, filter_builtin=False):
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

    def _collect_test_ids(self, required_amount):
        """

        :return:
        """
        all_available_test_ids = self.select_all_test_ids(
            table=self.performance_statistics_schema(),
            database_name=self.test_case_name
        )
        if required_amount == 2 and len(all_available_test_ids) < 2:
            raise NotImplementedError

        elif required_amount == 1 and len(all_available_test_ids) == 0:
            raise NotImplementedError

        else:
            return all_available_test_ids

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

    def export_flame_graph_comparison(self, path, benchmark_test_id=None, baseline_test_id=None,):
        """

        :param benchmark_test_id:
        :param baseline_test_id:
        :param path:
        :return:
        """
        benchmark_rendered_flame_graphs = []
        baseline_rendered_flame_graphs = []

        # Fetch the last two test-ids from the database (only if in Quick Profiling mode)
        if None in [benchmark_test_id, baseline_test_id] and self.test_case_name == default_test_case_name:
            all_available_test_ids = self._collect_test_ids(required_amount=2)
            benchmark_test_id = all_available_test_ids[-1]
            baseline_test_id = all_available_test_ids[-2]

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

        # Render HTML template
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

    def export_flame_graph(self, path, test_id=None):
        """

        :param test_id:
        :param path:
        :return:
        """
        rendered_flame_graphs = []

        # Fetch the last two test-ids from the database (only if in Quick Profiling mode)
        if test_id is None and self.test_case_name == default_test_case_name:
            all_available_test_ids = self._collect_test_ids(required_amount=2)
            test_id = all_available_test_ids[-1]

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
