<!-- LOGO -->
<p align="center">
  <img src="https://github.com/JoeyHendricks/python-micro-benchmarks/blob/master/media/images/banner-wide-with-text.jpeg?raw=true"/>
</p>
<!-- TAG LINE -->
<h3 align="center">Get your code of the couch by stressing it on the bench</h3>
<p align="center">
    <a href="https://www.linkedin.com/in/joey-hendricks/">Contact me</a> -
    <a href="https://github.com/JoeyHendricks/python-micro-benchmarks/issues">Report Bug or Request Feature</a> -
    <a href="https://github.com/JoeyHendricks/python-micro-benchmarks/discussions">Discussions</a> -
    <a href="https://github.com/JoeyHendricks/python-micro-benchmarks/wiki">Documentation</a>
</p>

<!-- CONTENT -->
## The project in a nutshell

Python-micro-benchmark is a library that aids in creating [micro to macro performance benchmarks](https://link.springer.com/referenceworkentry/10.1007%2F978-3-319-77525-8_111#:~:text=Definitions,operations%2C%20bandwidth%2C%20or%20latency.) for 
your code to find and visualize performance bottlenecks in your implementation in a flexible way.

With an emphasis on automation and visualizations, this library can integrate your benchmark 
within a unit test framework allowing you to test your code early in the development life cycle 
and letting you render an assortment of visualizations to get the drop on a pesky performance 
problem in your code.

## Installation

Installation is easy using [pip](https://pip.pypa.io/en/stable/) or clone the source code straight from GitHub.
```bash
pip install python-micro-benchmarks
```

## Getting Started

Getting started is straightforward after installing the package you can import the micro benchmarking object and **define a 
benchmark name** after that you can use the **run()** method to execute your benchmark on your creation and see 
if it is performing as expected.

Below you can find a simple example:

```Python
from Benchmarking import micro_benchmark as mb
from tests.stubs import FancyCode as Fc

# Give your benchmark a name
mb.test_case_name = "quick_start"

# Define you benchmark
mb.run(
    method=Fc().fast_method,  # <-- Make sure you don't call the method
    arguments=[],
    iteration=100,
    pacing=0,
    processes=2
)

# Get a letter rank how your changes compare to a previous benchmark.
letter_rank = mb.regression.letter_rank  # > A+
```

> Check out the [documentation](https://github.com/JoeyHendricks/python-micro-benchmarks/wiki) for more help to get started.

## Visualize that pesky bottleneck

<!-- Visualization Animation -->
<p align="center">
  <img src="https://github.com/JoeyHendricks/python-micro-benchmarks/blob/master/media/gifs/code_visualzation_animation.gif?raw=true"/>
</p>

Visualization are an excellent way to find out why your code slowdown or isn't working the way you would expect.
python-micro-benchmarks offers out of the box the following visualizations, so you don't need to worry how to get your eyes on that 
pesky bottleneck:

- Flame Graphs
- Code Heat Maps
- Bar charts
- Scatter plots (Coming soon)
- Line Graphs (Coming soon)

Want to visualize the data yourself or share the data in a common format, no problem python-micro-benchmarks has you covered. 
You can export your benchmarks in the following formats through the benchmark API:

- CSV
- JSON (Coming soon)

> Check out the docs for more information how to visualize or export your measurements.

# Detecting regression between benchmarks

This project has the ability to detect an interesting performance regression using 
[statistical methods](https://en.wikipedia.org/wiki/Statistical_distance) allowing 
that a code change can be ranked with a score from 0 to 100, or a letter 
[Japanese letter rank ranging from F to S](https://en.wikipedia.org/wiki/Academic_grading_in_Japan).

These ranking metrics allow users of this framework to quickly asses how much the performance of their code has
regressed after introducing a code change.In the below animation you can see the ranking metrics at work measuring 
the distance between two [CDF](https://en.wikipedia.org/wiki/Cumulative_distribution_function) and ranking it 
using a letter rank:

<!-- Letter rank Animation -->
<p align="center">
  <img src="https://github.com/JoeyHendricks/python-micro-benchmarks/blob/master/media/gifs/letter_ranking_simulation.gif?raw=true"/>
</p>

> More information about the math behind this method and how this works can be found 
> [here](https://github.com/JoeyHendricks/automated-performance-test-result-analysis)
> or within the [documentation](https://github.com/JoeyHendricks/python-micro-benchmarks/wiki).

## Learn more about the project

Want to learn more about python-micro-benchmarks then I would recommend read the documentation, 
or to check my older conference recordings about python-micro-benchmarks:

- 11/07/2020: [Don’t lose your mind over slow code check your performance sanity.](https://www.linkedin.com/pulse/dont-lose-your-mind-over-slow-code-check-performance-sanity-joey/) 
- 08/10/2020: [My recording about python-micro-benchmarks @NeotysPAC 2020.](https://www.youtube.com/watch?v=AWlhalEywEw) 
- 15/12/2020: [Interview about python-micro-benchmarks @TestGuild 2020.)](https://testguild.com/podcast/performance/p56-joey/)
- 12/01/2020: [An article I wrote for Neotys about my @NeotysPAC 2020 presentation.](https://www.neotys.com/blog/neotyspac-performance-testing-unit-level-joey-hendricks/)

> python-micro-benchmarks was formerly known as QuickPotato and has been renamed to better reflect its purpose.