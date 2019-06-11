import os
import shutil

from nltk.stem.snowball import SnowballStemmer
from gensim import corpora


def _fail(msg: str):
    """
    Generic fail method for debugging.
    """

    print(msg)
    os._exit(1)


def build_keys(keys: list):
    """
    Build list of keyword tuples.
    """

    return [tuple(k.split()) for k in keys]


def num_dict(year_list: list, keywords: [list, None]=None, nested: [int, None]=0):
    """
    Build empty dictionary with integers at leaf entries.
    """

    results = {}

    for year in year_list:

        if nested == 0:
            results[year] = 0

        elif nested == 1:
            results[year] = {}
            results[year]['TOTAL'] = 0
            for keyword in keywords:
                results[year][keyword] = 0

        else:
            _fail('Shouldn\'t be able to get here.')

    return results


def list_dict(year_list: list, keywords: [list, None]=None, nested: [None, int]=0):
    """
    Build empty dictionary with lists at leaf entries.
    """

    results = {}

    for year in year_list:

        if nested == 0:
            results[year] = []

        elif nested == 1:
            results[year] = {}
            for keyword in keywords:
                results[year]['TOTAL'] = []
                results[year][keyword] = []

        else:
            _fail('Shouldn\'t be able to get here.')

    return results


def gensim_dict(year_list: list):
    """
    Build empty dictionary with gensim Dictionary objects at leaf entries.
    """

    results = {}

    for year in year_list:
        results[year] = corpora.Dictionary()

    return results


def determine_year(year: int, year_list: list):
    """
    Given a year and list of year periods,
    return which period that year falls into.
    """

    for i in (range(len(year_list[:-1]))):

        if year_list[i] <= year < year_list[i + 1]:
            return year_list[i]

    _fail("{} is not in range".format(year))


def stem(word: str, language: [str, None] = 'english'):
    """
    Returns input word and its stem.
    """

    try:
        s = SnowballStemmer(language.lower())
    except ValueError:
        _fail("{} is not supported, please enter a valid language.".format(language))

    stemmed = s.stem(word.lower())

    return '{0}: {1}'.format(word, stemmed)


# TODO: ask user if they want to overwrite directory or add to it, if it exists
def build_out(out_dir: str):
    """
    Build output directory, overwrite if it exists.
    """

    if out_dir is not None:
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        else:
            shutil.rmtree(out_dir)
            os.mkdir(out_dir)
    else:
        _fail("Please specify output directory.")








