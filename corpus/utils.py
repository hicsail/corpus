import os
import sys
import shutil

from nltk.stem.snowball import SnowballStemmer
from gensim import corpora


def _fail(msg: str):
    """
    Generic fail method for debugging.
    """

    print(msg)
    sys.exit()


def build_keys(keys: list):
    """
    Build list of keyword tuples.
    """

    return [tuple(k.split()) for k in keys]


def num_dict(alist: list, keywords: [list, None]=None, nested: [int, None]=0):
    """
    Build empty dictionary with integers at leaf entries.
    alist: year_list or author_list
    """

    results = {}

    for item in alist:

        if nested == 0:
            results[item] = 0

        else:
            results[item] = {}
            results[item]['TOTAL'] = 0

            for keyword in keywords:
                results[item][keyword] = 0

    return results


def simple_dict(alist: list):
    """
    Build simple dict of dicts.
    """

    results = {}

    for item in alist:
        results[item] = {}

    return results


def list_dict(alist: list, keywords: [list, None] = None, nested: [None, int] = 0):
    """
    Build empty dictionary with lists at leaf entries.
    alist: year_list or author_list
    """

    results = {}

    for item in alist:

        if nested == 0:
            results[item] = []

        else:
            results[item] = {}

            for keyword in keywords:
                results[item]['TOTAL'] = []
                results[item][keyword] = []

    return results


def gensim_dict(alist: list):
    """
    Build empty dictionary with gensim Dictionary objects at leaf entries.
    alist: year_list or author_list
    """

    results = {}

    for item in alist:
        results[item] = corpora.Dictionary()

    return results


def determine_year(year: int, year_list: list):
    """
    Given a year and list of year periods,
    return which period that year falls into.
    """

    for i in (range(len(year_list[:-1]))):

        if year_list[i] <= year < year_list[i + 1]:
            return year_list[i]

    raise Exception("{} is not in range".format(year))


def stem(word: str, language: [str, None] = 'english'):
    """
    Returns input word and its stem.
    """

    try:
        s = SnowballStemmer(language.lower())
    except ValueError:
        raise Exception("{} is not supported, please enter a valid language.".format(language))

    stemmed = s.stem(word.lower())

    return '{0}: {1}'.format(word, stemmed)


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
        raise Exception("Specify an output directory.\n")
