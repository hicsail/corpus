from setuptools import setup

setup(
    name             = 'corpus',
    version          = '0.0.0.1',
    install_requires = ['gensim', 'nltk', 'matplotlib', 'numpy', 'scipy', 'statsmodels'],
    license          = 'MIT',
    url              = 'https://github.com/hicsail/corpus',
    description      = 'Library to display NLP metrics on large corpora over time.'
)

