from setuptools import setup, find_packages

setup(
    name             = 'corpus',
    version          = '0.0.0.1',
    packages         = find_packages(),
    license          = 'MIT',
    url              = 'https://github.com/hicsail/corpus',
    description      = 'Library to display NLP metrics on large corpora over time.',
    long_description = open('README.md').read(),
)

