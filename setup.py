from setuptools import setup

setup(
    name='QuickPotato',
    version='0.1',
    packages=['QuickPotato', 'QuickPotato.harness', 'QuickPotato.inspect', 'QuickPotato.database',
              'QuickPotato.utilities', 'QuickPotato.statistics', 'QuickPotato.configuration'],
    url='https://github.com/JoeyHendricks/python-unit-level-performance-testing',
    license='MIT',
    author='Joey Hendricks',
    author_email='joey.hendricks20@icloud.com',
    description='The framework that enables Python developers to include performance validation into their unit tests',
    install_requires=['numpy', 'SQLAlchemy-Utils', 'scipy', 'SQLAlchemy', 'PyMySQL', 'psutil', 'pandas', 'PyYAML']
)
