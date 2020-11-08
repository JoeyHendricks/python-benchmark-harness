from QuickPotato.visualization.flame_graphs import FlameGraph
from QuickPotato.database.crud import DatabaseOperations
from QuickPotato.utilities.html_templates import html_test_report
from jinja2 import Template
from datetime import datetime


class CompareFlameGraphs(DatabaseOperations):

    def __init__(self, test_case_name, benchmark_test_id, baseline_test_id,
                 filter_external_libraries=False, filter_builtin=False):
        super(CompareFlameGraphs, self).__init__()

        if benchmark_test_id == baseline_test_id:
            raise NotImplementedError

        self.test_case_name = test_case_name
        self.benchmark_test_id = benchmark_test_id
        self.baseline_test_id = baseline_test_id
        self.filter_external_libraries = filter_external_libraries
        self.filter_builtin = filter_builtin

        self.benchmark_meta_data = self.select_all_meta_data(self.test_case_name, benchmark_test_id)
        self.baseline_meta_data = self.select_all_meta_data(self.test_case_name, baseline_test_id)
        self.benchmark_flame_graphs, self.baseline_flame_graphs = self._collect_all_flame_graphs()

    def _generate_flame_graphs(self, sid_benchmark, sid_baseline):
        """

        :param sid_benchmark:
        :param sid_baseline:
        :return:
        """
        benchmark = FlameGraph(
            self.test_case_name,
            sid_benchmark,
            self.filter_external_libraries,
            self.filter_builtin
        )
        baseline = FlameGraph(
            self.test_case_name,
            sid_baseline,
            self.filter_external_libraries,
            self.filter_builtin
        )
        return benchmark.svg_flame_graph, baseline.svg_flame_graph

    def _collect_all_flame_graphs(self):
        """

        :return:
        """
        rendered_benchmark_flame_graphs = []
        rendered_baseline_flame_graphs = []

        for bench, base in zip(self.benchmark_meta_data, self.baseline_meta_data):
            bench_flame_graph, base_flame_graph = self._generate_flame_graphs(bench["sample_id"], base["sample_id"])
            rendered_benchmark_flame_graphs.append(bench_flame_graph)
            rendered_baseline_flame_graphs.append(base_flame_graph)

        return rendered_benchmark_flame_graphs, rendered_baseline_flame_graphs

    def export_html_flame_graphs_test_report(self, path):
        """

        :return:
        """
        name = f"{self.test_case_name}-{self.benchmark_test_id}Vs{self.baseline_test_id}-{datetime.now().timestamp()}"
        with open(f"{path}{name}.html", 'a') as file:
            file.write(self.html_flame_graphs_test_report)
        return True

    @property
    def html_flame_graphs_test_report(self):
        """

        :return:
        """
        template = Template(html_test_report)
        html = template.render(
            benchmark_test_id=self.benchmark_test_id,
            baseline_test_id=self.baseline_test_id,
            benchmark_meta_data=self.benchmark_meta_data,
            baseline_meta_data=self.baseline_meta_data,
            zipped_benchmark_data=zip(self.benchmark_meta_data, self.benchmark_flame_graphs),
            zipped_baseline_data=zip(self.baseline_meta_data, self.baseline_flame_graphs)
        )
        return html


text = CompareFlameGraphs(
    test_case_name="upt_of_complex_functions",
    benchmark_test_id="YWM50MMZU9SM",
    baseline_test_id="92COVFWCYFVA",
    filter_external_libraries=False,
    filter_builtin=False
).export_html_flame_graphs_test_report(path="C:\\Temp\\")
