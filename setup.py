from setuptools import setup

setup(
    name='QuickPotato',
    version='0.2',
    packages=[
        'QuickPotato',
        'QuickPotato.harness',
        'QuickPotato.database',
        'QuickPotato.profiling',
        'QuickPotato.utilities',
        'QuickPotato.statistical',
        'QuickPotato.configuration',
        'QuickPotato.analysis'
    ],
    install_requires=[
        'numpy',
        'SQLAlchemy-Utils',
        'scipy',
        'SQLAlchemy',
        'PyMySQL',
        'psutil',
        'pandas',
        'PyYAML',
        'Jinja2'
    ],
    url='https://github.com/JoeyHendricks/QuickPotato',
    license='MIT',
    author='Joey Hendricks',
    author_email='joey.hendricks20@icloud.com',
    description='The framework that enables Python developers to include performance validation into their tests',
    python_requires='>=3.7'
)
