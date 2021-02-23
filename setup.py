from setuptools import setup

setup(
    name='CouchPotato',
    version='0.2',
    packages=[
        'CouchPotato',
        'CouchPotato.harness',
        'CouchPotato.database',
        'CouchPotato.profiling',
        'CouchPotato.utilities',
        'CouchPotato.statistical',
        'CouchPotato.configuration',
        'CouchPotato.analysis'
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
