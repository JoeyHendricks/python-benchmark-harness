from setuptools import setup
from Benchmarking import __version__

setup(
    name='Benchmarking',
    version=str(__version__),
    packages=[
        'Benchmarking',
        'Benchmarking.profiling',
        'Benchmarking._database',
        'Benchmarking.profiling',
        'Benchmarking._utilities',
        'Benchmarking.statistical',
        'Benchmarking._configuration'
    ],
    install_requires=[
        'numpy',
        'SQLAlchemy-Utils',
        'scipy',
        'SQLAlchemy',
        'pandas',
        'PyYAML',
        'Jinja2'
    ],
    url='https://github.com/JoeyHendricks/python-benchmarks',
    license='MIT',
    author='Joey Hendricks',
    author_email='joey.hendricks20@icloud.com',
    description='A micro/macro benchmark framework for the Python programming '
                'language that helps with optimizing your software.',
    python_requires='>=3.8'
)
