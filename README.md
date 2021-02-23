<!-- LOGO -->
<p align="center">
  <img src="https://github.com/JoeyHendricks/python-unit-level-performance-testing/blob/master/images/banner-with-text.png?raw=true"/>
</p>

<!-- TAG LINE -->
<h3 align="center">Profile and test to gain insights into the performance of your beautiful Python code</h3>
<p align="center">
    <a href="https://github.com/JoeyHendricks/CouchPotato">View Demo</a> -
    <a href="https://github.com/JoeyHendricks/CouchPotato/issues">Report Bug</a> -
    <a href="https://github.com/JoeyHendricks/CouchPotato/issues">Request Feature</a>
</p>

<!-- BADGES -->
<div align="center">
<a href="https://github.com/JoeyHendricks/CouchPotato/graphs/contributors"><img src="https://img.shields.io/github/contributors/JoeyHendricks/CouchPotato?style=for-the-badge"></a>
<a href="https://github.com/JoeyHendricks/CouchPotato/network/members"><img src="https://img.shields.io/github/forks/JoeyHendricks/CouchPotato?style=for-the-badge"></a>
<a href="https://github.com/JoeyHendricks/CouchPotato/stargazers"><img src="https://img.shields.io/github/stars/JoeyHendricks/CouchPotato?style=for-the-badge"></a>
<a href="https://github.com/JoeyHendricks/CouchPotato/issues"><img src="https://img.shields.io/github/issues/JoeyHendricks/CouchPotato?style=for-the-badge"></a>
<a href="https://github.com/JoeyHendricks/CouchPotato/blob/master/LICENSE.md"><img src="https://img.shields.io/github/license/JoeyHendricks/CouchPotato?style=for-the-badge"></a>
<a href="https://www.linkedin.com/in/joey-hendricks/"><img src="https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555"></a>
</div>
<br>

<!-- TABLE OF CONTENTS -->
<details open="open" >
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#CouchPotato-in-a-nutshell">CouchPotato in a nutshell</a>
    </li>
    <li>
        <a>Getting Started</a>
        <ul>
            <li><a href="#Installation">Installation</a></li>
            <li><a href="#Options-you-can-configure">Options</a></li>
        </ul>
    </li>
    <li><a href="#Generating-visualizations">Generating visualizations</a></li>
    <li>
      <a>Test-driven performance testing</a>
      <ul>
        <li><a href="#Boundary-testing">Boundary testing</a></li>
        <li><a href="#Regression-testing">Regression testing</a></li>
      </ul>
    </li>
    <li><a href="#Learn-more-about-CouchPotato">Learn more about CouchPotato</a></li>
  </ol>
</details>

<!-- CONTENT -->
## CouchPotato in a nutshell

CouchPotato is a Python library that aims to make it easier to rapidly profile your software and produce powerful 
code visualizations that enables you to quickly investigate where potential performance bottlenecks are hidden.

Also, CouchPotato is trying to provide you with a path to add an automated performance testing angle to 
your regular unit tests or test-driven development test cases allowing you to test your code early in the 
development life cycle in a simple, reliable, and fast way.

## Installation

Install using [pip](https://pip.pypa.io/en/stable/) or download the source code from GitHub.
```bash
pip install CouchPotato
```
> Do note that CouchPotato hasn't released (yet) on the Python Package Index
> Please just grab the source code or the latest release from GitHub for now :).

## Options you can configure

CouchPotato comes equipped with some options you can configure to make sure CouchPotato fits your needs.
Below you can find a list of all basic options:

```python
from CouchPotato.configuration.management import options

# Profiling Settings
options.enable_intrusive_profiling = True 
options.enable_system_resource_collection = True

# Results Storage
options.connection_url = None  # <-- None will use SQlite and store results in Temp directory
options.enable_database_echo = False

# Storage Maintenance 
options.enable_auto_clean_up_old_test_results = True
options.maximum_number_saved_test_results = 10

```
> States of options are saved in a static yaml options file.  
> That is why settings can be defined just once or changed on the fly.

## Generating visualizations

Under the hood, CouchPotato uses C-profile to measure the speed of your code. These results might not always 
be easy to understand and would require some digging to find out where a potential performance problem is hiding.
To effortlessly generate a flame graph from your code do the following:

```python
from CouchPotato.configuration.management import options
from CouchPotato.statistical.visualizations import FlameGraph
from CouchPotato.profiling.intrusive import performance_critical  # <-- Import the decorator

options.enable_intrusive_profiling = True  # <-- Make sure that intrusive profiling is enabled


@performance_critical  # <-- Make sure you attach the decorator.
def i_am_a_slow_function():
    num = 6 ** 6 ** 6
    return len(str(num))


# Generate Flame Graph
FlameGraph().export(path="C:\\Temp\\")
```
> It is possible to reduce the amount of noise with a parameter in the flame graph class.

Below an example of a flame graph generated by CouchPotato **(Code that was used can be found under 
the folder demo in example_code.py)**:

[![Example of a simple flame graph](/images/fancy-code-flame-graph.png "flame graph simple")](
https://raw.githubusercontent.com/JoeyHendricks/python-unit-level-performance-testing/95132b0a0ebd61f57deb7ec2197d01e5c0d4829f/images/fancy_code_flame_graph.svg)

> If you are unfamiliar with Flame Graphs you can best read about them on [Brendan Greg's website](http://www.brendangregg.com/flamegraphs.html).

How to interpret the Flame Graphs generated by CouchPotato:

- Each box is a function in the stack
- The y-axis shows the stack depth the top box shows what was on the CPU.
- The x-axis **does not show time** but spans the population and is ordered alphabetically.
- The width of the box show how long it was on-CPU or was part of an parent function that was on-CPU.

## Boundary testing

Within CouchPotato, it is possible to create a performance test that validates if your code breaches any 
defined boundary or not. An example of this sort of test can be found in the snippet below:

```python
from CouchPotato.profiling.intrusive import unit_performance_test as upt
from example.example_code import fast_method

# Define test case name
upt.test_case_name = "test_performance"

# Establish performance boundaries
upt.max_and_min_boundary_for_average = {"max": 1, "min": 0.001}

# Execute method under test
for _ in range(0, 10):
    fast_method()

# Analyse profiled results will output True if boundaries are not breached otherwise False
results = upt.verify_benchmark_against_set_boundaries
```

## Regression testing

It is also possible to verify that there is no regression between the current benchmark and a previous baseline.
The method for creating such a test can also be found in the snippet below:

```python
from CouchPotato.profiling.intrusive import unit_performance_test as upt
from example.example_code import fast_method

# Define test case name
upt.test_case_name = "test_performance"

# Execute method under test
for _ in range(0, 10):
    fast_method()

# Analyse results for change True if there is no change otherwise False
results = upt.verify_benchmark_against_previous_baseline
```

## Learn more about CouchPotato

If you want to learn more about test driven performance testing and want to 
see how this project reached its current state? 
Then I would encourage you to check out the following resources:

- 11/07/2020: [Don’t lose your mind over slow code check your performance sanity.(English)](https://www.linkedin.com/pulse/dont-lose-your-mind-over-slow-code-check-performance-sanity-joey/) 
- 08/10/2020: [My recording about QuickPotato @NeotysPAC 2020. (English)](https://www.youtube.com/watch?v=AWlhalEywEw) 
- 15/12/2020: [Interview about CouchPotato @TestGuild 2020. (English)](https://testguild.com/podcast/performance/p56-joey/)
- 12/01/2020: [An article I wrote for Neotys about my @NeotysPAC 2020 presentation. (English)](https://www.neotys.com/blog/neotyspac-performance-testing-unit-level-joey-hendricks/)
