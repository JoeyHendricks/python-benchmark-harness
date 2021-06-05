from setuptools import setup

setup(
    name='QuickPotato',
    version='1.0.1',
    packages=[
        'QuickPotato',
        'QuickPotato.harness',
        'QuickPotato.database',
        'QuickPotato.profiling',
        'QuickPotato.utilities',
        'QuickPotato.statistical',
        'QuickPotato.configuration'
    ],
    install_requires=[
        'numpy',
        'SQLAlchemy-Utils',
        'scipy',
        'SQLAlchemy',
        'PyMySQL',
        'pandas',
        'PyYAML',
        'Jinja2'
    ],
    url='https://github.com/JoeyHendricks/QuickPotato',
    license='MIT',
    author='Joey Hendricks',
    author_email='joey.hendricks20@icloud.com',
    description='Making performance testing within Python easy and understandable.',
    python_requires='>=3.7'
)
