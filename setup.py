from setuptools import setup

setup(
    name='python-benchmark-harness',
    version='1.0.3',
    packages=[
        'Benchmarking',
        'Benchmarking._database',
        'Benchmarking.profiling',
        'Benchmarking._templates',
        'Benchmarking._utilities',
        'Benchmarking.statistical',
        'Benchmarking._configuration',
        'Benchmarking.visualizations'
    ],
    install_requires=[
        'SQLAlchemy',
        'SQLAlchemy-Utils',
        'setuptools',
        'numpy',
        'pandas',
        'Jinja2',
        'scipy',
        'PyYAML',
        'plotly'
    ],
    package_dir={'': 'package'},
    url='https://github.com/JoeyHendricks/python-benchmarks',
    license='MIT',
    author='Joey Hendricks',
    author_email='joey.hendricks20@icloud.com',
    description='A micro/macro benchmark framework for the Python '
                'programming language that helps with optimizing your software.'
)
