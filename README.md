<!-- LOGO -->
<p align="center">
  <img src="https://github.com/JoeyHendricks/QuickPotato/blob/master/media/banner-wide-with-text.jpg"/>
</p>

<!-- TAG LINE -->
<h3 align="center">Get your code of the couch by stressing it on the bench</h3>
<p align="center">
    <a href="https://www.linkedin.com/in/joey-hendricks/">Contact me</a> -
    <a href="https://github.com/JoeyHendricks/QuickPotato/issues">Report Bug or Request Feature</a> -
    <a href="https://github.com/JoeyHendricks/QuickPotato/discussions">Discussions</a> -
    <a href="https://github.com/JoeyHendricks/QuickPotato/wiki">Documentation</a>
</p>

<!-- CONTENT -->
## PyBench in a nutshell

QuickPotato is a Python library that aims to make it easier to rapidly profile your software and produce powerful 
code visualizations that enables you to quickly investigate where potential performance bottlenecks are hidden.

Also, QuickPotato is trying to provide you with a path to add an automated performance testing angle to 
your regular unit tests or test-driven development test cases allowing you to test your code early in the 
development life cycle in a simple, reliable, and fast way.

## Installation

Installation is easy using [pip](https://pip.pypa.io/en/stable/) or clone the source code straight from GitHub.
```bash
pip install PyBench
```

> currently not yet deployed on pypi

## Getting Started

```Python
from PyBench import micro_benchmark as mb
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

# Get a letter rank how changes compare to the previous run.
letter_rank = mb.distance_statistics.letter_rank  # > A+
```

## Visualize that pesky bottleneck

<!-- Visualization Animation -->
<p align="center">
  <img src="https://github.com/JoeyHendricks/QuickPotato/blob/master/media/gifs/code_visualzation_animation.gif?raw=true"/>
</p>

Visualization are an excellent way to find out why your code slowdown or isn't working the way you would expect.
PyBench offers out of the box the following visualizations, so you don't need to worry how to get your eyes on that 
pesky bottleneck:

- Flame Graphs
- Code Heat Maps
- Bar charts
- Scatter plots (Coming soon)
- Line Graphs (Coming soon)

Want to visualize the data yourself or share the data in a common format, no problem Pybench has you covered. 
You can export your benchmarks in the following formats through the benchmark API:

- CSV
- JSON (Coming soon)

> Check out the docs for more information how to visualize or export your measurements.

## Learn more about PyBench

Want to learn more about PyBench then I would recommend read the documentation, 
or to check my older conference recordings about Pybench:

- 11/07/2020: [Don’t lose your mind over slow code check your performance sanity.](https://www.linkedin.com/pulse/dont-lose-your-mind-over-slow-code-check-performance-sanity-joey/) 
- 08/10/2020: [My recording about PyBench @NeotysPAC 2020.](https://www.youtube.com/watch?v=AWlhalEywEw) 
- 15/12/2020: [Interview about PyBench @TestGuild 2020.)](https://testguild.com/podcast/performance/p56-joey/)
- 12/01/2020: [An article I wrote for Neotys about my @NeotysPAC 2020 presentation.](https://www.neotys.com/blog/neotyspac-performance-testing-unit-level-joey-hendricks/)

> PyBench was formerly known as QuickPotato and has been renamed to better reflect its purpose.